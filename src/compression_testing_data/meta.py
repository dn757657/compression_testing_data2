import logging

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from .models.base import Base
from .models.samples import *
from .models.acquisition_settings import *
from .models.reconstruction_settings import *
from .models.testing import *

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


conn_str = 'postgresql://myuser:mypassword@localhost:5432/compression_testing'
try:
    engine = create_engine(conn_str)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
except OperationalError:
    Session = None
    logging.info("Could not connect to DB!")