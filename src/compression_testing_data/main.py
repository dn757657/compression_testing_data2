import sqlalchemy.orm
import logging

from models.reconstruction_settings import ProcessingModels
from src.compression_testing_data.models.acquisition_settings import AcquisitionModels
from models.testing import CompressionTrial
from meta import Session

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
        settings_list = [f"{key}={value}" for key, value in settings_dict.items()
                         if key != 'id' and key != 'created_at']  # Exclude the 'id' column

    return settings_list


def parse_gphoto_config_for_sql(config_output):
    settings = {}
    lines = config_output.split("\n")
    current_setting = None
    is_readonly = False

    for line in lines:
        if line.startswith("/main"):
            current_setting = line.split(" : ")[0].split("/")[-1]
            is_readonly = False  # Reset readonly flag for new setting
        elif 'Readonly: 1' in line:
            is_readonly = True
        elif line.strip().startswith("Current:") and not is_readonly:
            current_value = line.split(":")[1].strip()
            settings[current_setting] = current_value

    return settings


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


def run_trial():
    # initialization phase

    return


def main():

    # TODO when generating new trial
    #   check for all possible entries in foreign keys for trial or object settings
    #   since the camera table is not required to be a unique set of settings there
    #   will be perhaps duplicate sets, therefore a trial coulx exist
    #   - or does this not apply since frames cant be remade, frames from a trial are what they are
    #   - the sample is gone, and woudl require a new trial to replicate - sorta

    # TODO when entering a new entry in the database ensure that the file exists per the base directory
    #  file make sure it exists - might be a pain if strictly enforced but might save headache?

    session = Session()
    # session.add(Print(
    #     name='new_print',
    #     filament_name='VarioShore',
    #     printer_model='Mk3s+',
    #     printer_settings_file='some_settings.ini',
    #     stl_file='my.stl'
    # ))
    # session.commit()
    #
    # session.add(Sample(
    #     height=19.5,
    #     print_id=1
    # ))
    # session.commit()

    session.add(CompressionTrial(
        sample_id=1
    ))
    session.commit()

    gen_input_jsons(models=AcquisitionModels + ProcessingModels)


if __name__ == '__main__':
    main()