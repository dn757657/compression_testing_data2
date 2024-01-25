from .models.base import Base

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .models.samples import *
from .models.acquisition_settings import *
from .models.reconstruction_settings import *
from .models.testing import *


conn_str = 'postgresql://myuser:mypassword@localhost:5432/compression_testing'
engine = create_engine(conn_str)
Base.metadata.bind = engine
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
