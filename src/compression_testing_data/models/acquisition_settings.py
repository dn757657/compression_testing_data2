import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from .base import Base


class CameraSetting(Base):
    __tablename__ = 'Camera_Settings'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    autopoweroff = Column(String)
    capture = Column(String)
    imageformat = Column(String)  # 21 = raw
    iso = Column(String)
    focusmode = Column(String) # 0 = one shot
    aspectratio = Column(Integer)  # 0 native aspect is best
    aperture = Column(Integer)
    shutterspeed = Column(Integer)

    frames = relationship(
        'Frame',
        back_populates='camera_setting',
        cascade="all, delete",
        passive_deletes=True
    )


class PlatonDimension(Base):
    __tablename__ = 'Platon_Dimensions'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    dim1 = Column(Float, default=40, nullable=False)
    dim2 = Column(Float, default=40, nullable=False)
    dim3 = Column(Float, default=40, nullable=False)
    dim4 = Column(Float, default=40, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            'dim1',
            'dim2',
            'dim3',
            'dim4',
            name=f'uix_{__tablename__}'
        ),
    )


AcquisitionModels = [cls for cls in Base.__subclasses__()]