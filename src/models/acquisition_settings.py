import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from .base import Base


class CameraSetting(Base):
    __tablename__ = 'Camera_Settings'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    syncdatetimeutc = Column(String)
    syncdatetime = Column(String)
    uilock = Column(String)
    popupflash = Column(String)
    autofocusdrive = Column(String)
    manualfocusdrive = Column(String)
    cancelautofocus = Column(String)
    eoszoom = Column(String)
    eoszoomposition = Column(String)
    viewfinder = Column(String)
    eosremoterelease = Column(String)
    eosmoviemode = Column(String)
    opcode = Column(String)
    datetimeutc = Column(String)
    datetime = Column(String)
    output = Column(String)
    movierecordtarget = Column(String)
    evfmode = Column(String)
    ownername = Column(String)
    artist = Column(String)
    copyright = Column(String)
    nickname = Column(String)
    customfuncex = Column(String)
    focusarea = Column(String)
    strobofiring = Column(String)
    flashcharged = Column(String)
    oneshotrawon = Column(String)
    autopoweroff = Column(String)
    depthoffield = Column(String)
    capturetarget = Column(String)
    capture = Column(String)
    remotemode = Column(String)
    eventmode = Column(String)
    serialnumber = Column(String)
    manufacturer = Column(String)
    cameramodel = Column(String)
    deviceversion = Column(String)
    vendorextension = Column(String)
    model = Column(String)
    batterylevel = Column(String)
    lensname = Column(String)
    eosserialnumber = Column(String)
    availableshots = Column(String)
    eosmovieswitch = Column(String)
    imageformat = Column(String)
    imageformatsd = Column(String)
    imageformatcf = Column(String)
    iso = Column(String)
    whitebalance = Column(String)
    colortemperature = Column(Integer)
    whitebalanceadjusta = Column(Integer)
    whitebalanceadjustb = Column(Integer)
    whitebalancexa = Column(Integer)
    whitebalancexb = Column(Integer)
    colorspace = Column(String)
    zoomspeed = Column(Integer)
    exposurecompensation = Column(Float)
    focusmode = Column(String)
    continuousaf = Column(String)
    aspectratio = Column(Integer)
    storageid = Column(String)
    highisonr = Column(String)
    autoexposuremode = Column(String)
    autoexposuremodedial = Column(String)
    drivemode = Column(String)
    picturestyle = Column(String)
    aperture = Column(Float)
    shutterspeed = Column(Float)
    meteringmode = Column(String)
    liveviewsize = Column(String)
    bracketmode = Column(String)
    aeb = Column(String)
    alomode = Column(String)
    d406 = Column(String)

    frames = relationship('Frame', back_populates='camera_setting')


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