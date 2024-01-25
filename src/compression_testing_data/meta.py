from models.base import Base

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

CONN_STR = 'postgresql://myuser:mypassword@localhost:5432/compression_testing'
ENGINE = create_engine(CONN_STR)
Base.metadata.bind = ENGINE
Base.metadata.create_all(ENGINE)
Session = sessionmaker(bind=ENGINE)