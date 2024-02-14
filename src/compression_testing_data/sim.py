from compression_testing_data.meta import get_session
from compression_testing_data.models.samples import Sample, Print
from compression_testing_data.models.testing import CompressionTrial


def add_test_print(session):
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


def add_test_sample(session, print_id: int):
    """
    only define non default entries for testing
    :param session:
    :return:
    """
    session.add(Sample(
        print_id=print_id
    ))
    return session


def add_test_trial(session, sample_id: int):
    session.add(CompressionTrial(
        sample_id=sample_id
    ))
    return session