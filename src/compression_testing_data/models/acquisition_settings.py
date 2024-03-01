import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from .base import Base


class CameraSetting(Base):
    __tablename__ = 'Camera_Settings'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    autopoweroff = Column(String, default='0')
    capture = Column(String, default='0')
    imageformat = Column(String, default='0')  # 21 = raw
    iso = Column(String, default='13')
    focusmode = Column(String, default='0') # 0 = one shot
    aspectratio = Column(Integer, default=0)  # 0 native aspect is best
    aperture = Column(Integer, default=4)
    shutterspeed = Column(Integer, default=35)

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

    processed_point_clouds = relationship(
        'ProcessedPointCloud',
        back_populates='platon_dimension',
        cascade="all, delete",
        passive_deletes=True
    )

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