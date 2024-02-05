import sqlalchemy.orm
import logging
import uuid

from sqlalchemy import select

from .models.reconstruction_settings import ProcessingModels
from .models.acquisition_settings import AcquisitionModels
from .models.samples import Print, Sample
from .models.testing import CompressionTrial, CompressionStep
from .meta import Session

BASE_DIR = ""
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def parse_sql_gphoto_config_for_gphoto(camera_setting: sqlalchemy.orm.Query):

    settings_list = list()
    if camera_setting:
        settings_dict = {column.name: getattr(camera_setting, column.name)
                         for column in camera_setting.__table__.columns
                         if getattr(camera_setting, column.name) is not None}

        # Convert to the desired list format
        settings_list = parse_cam_config_dict_for_gphoto(dict_config=settings_dict)
    return settings_list


def parse_cam_config_dict_for_gphoto(dict_config: dict()):
    settings_list = [f"{key}={value}" for key, value in dict_config.items()
                    if key != 'id' and key != 'created_at']  # Exclude the 'id' column
    return settings_list


def parse_gphoto_config_for_sql(config_output):
    settings = {}
    is_readonly = False

    for setting, value in config_output.items():
        print(f"Setting: {setting}, Value{value}")

        setting_name = setting.split("/")[-1]

        lines = value.split("\n")
        for line in lines:
            if 'Readonly: 1' in line:
                is_readonly = True
            elif line.strip().startswith("Current:") and not is_readonly:
                current_value = line.split(":")[1].strip()
                settings[setting_name] = current_value
                print(f"Result: {setting_name}: {current_value}")

    return settings


def add_steps(
        session: Session,
        trial_id,
):
    stmt = select(CompressionTrial).where(CompressionTrial.id == trial_id)
    slct = session.execute(stmt)

    trials = slct.scalars().all()
    if len(trials) > 1:
        logging.info("found too many trials")
        return
    else:
        trial = trials[0]

    strain = 1
    while strain > trial.strain_limit:
        new_step = CompressionStep()

        step_name = uuid.uuid4()

        new_step.name = step_name
        new_step.strain_target = strain
        new_step.compression_trial_id = trial_id

        session.add(new_step)
        print(f"{step_name}: {strain}")

        strain -= trial.strain_delta_target

    return session


def test_trial():
    session = Session()

    # clear tables to simulate starting from scratch
    models = [Print, Sample, CompressionTrial]
    for model in models:
        session.query(model).delete()
    session.commit()

    session = add_test_print(session=session)
    session.commit()
    print_id = session.query(Print).first().id

    session = add_test_sample(session=session, print_id=print_id)
    session.commit()
    sample_id = session.query(Sample).first().id

    session = add_test_trial(session=session, sample_id=sample_id)
    session.commit()

    trial_id = session.query(CompressionTrial).first().id
    session = add_steps(session=session, trial_id=trial_id)
    session.commit()

    session.close()
    pass

def gen_input_jsons(models):
    """
    generate some json files to show the structure of user settings from the DB
    colors one doesnt work right now because it doesnt have defaults basically
        still shows the structure of a color setting
    :return:
    """

    session = Session()

    import json
    for model in models:
        try:
            # q = session.query(model).first()
            q = session.get_one(model, ident=1)
        except sqlalchemy.orm.exc.NoResultFound:
            session.add(model())
            session.commit()
            q = session.get_one(model, ident=1)
            # q = session.query(model).first()
        q = q.__dict__
        remove_keys = list()
        [remove_keys.append(key) for key in q.keys() if any(substring in key for substring in ['_sa_instance_state', 'id', '__len__', 'created_at'])]
        all(map(q.pop, remove_keys))

        with open(f"{model.__tablename__}.json", 'w') as f:
            try:
                json.dump(q, f, indent=4)
            except TypeError:
                logging.info(f"{model.__tablename__} SQL Table Cannot be Serialized")


    pass


def add_test_print(session: Session):
    """
    only define non default entries for testing
    :param session:
    :return:
    """
    session.add(Print(
        name='new_print',
        filament_name='VarioShore',
        printer_model='Mk3s+',
        printer_settings_file='some_settings.ini',
        stl_file='my.stl'
    ))
    return session


def add_test_sample(session: Session, print_id: int):
    """
    only define non default entries for testing
    :param session:
    :return:
    """
    session.add(Sample(
        print_id=print_id
    ))
    return session


def add_test_trial(session: Session, sample_id: int):
    session.add(CompressionTrial(
        sample_id=sample_id
    ))
    return session


def main():
    pass

if __name__ == '__main__':
    main()