from models.base import Base
import models.samples
import models.acquisition_settings
import models.testing
import models.reconstruction_settings

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

CONN_STR = 'postgresql://myuser:mypassword@localhost:5432/compression_testing'
ENGINE = create_engine(CONN_STR)
Base.metadata.bind = ENGINE
Base.metadata.create_all(ENGINE)
Session = sessionmaker(bind=ENGINE)