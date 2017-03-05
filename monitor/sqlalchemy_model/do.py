from sqlalchemy import Column, Integer, String, Boolean,DateTime,ForeignKey,BigInteger
from sqlalchemy import func
from sqlalchemy import Sequence
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class TimestampMixin(object):
    created_at = Column(DateTime, default=func.now())
    updated_at = Column('last_updated',DateTime,onupdate=func.now())

class DataCenter(TimestampMixin, Base):
    __tablename__ =  'data_center'
    id = Column(Integer, Sequence('dc_id_seq'), primary_key=True)

    name = Column(String(100))

    physcial_hosts = relationship("PhyscialHost",back_populates="datacenter")

class PhyscialHost(TimestampMixin,Base):
    __tablename__ =  'physcial_host'
    id = Column(Integer, Sequence('ph_id_seq'), primary_key=True)
    dc_id = Column(Integer,ForeignKey("data_center.id"))

    name = Column(String(100))
    ipaddr = Column(String(16))

    datacenter = relationship("DataCenter",uselist = False,back_populates="physcial_hosts")
    containers = relationship("Container",back_populates = "physcial_host")
    virtual_machines = relationship("VirtualMachine",back_populates = "physcial_host")

class Container(TimestampMixin,Base):
    __tablename__ =  'container'
    id = Column(Integer, Sequence('container_id_seq'), primary_key=True)
    ph_id = Column(Integer,ForeignKey("physcial_host.id"))

    name = Column(String(100))

    physcial_host = relationship("PhyscialHost",uselist = False,back_populates="containers")

class VirtualMachine(TimestampMixin,Base):
    __tablename__ =  'virtual_machine'
    id = Column(Integer, Sequence('vm_id_seq'), primary_key=True)
    ph_id = Column(Integer,ForeignKey("physcial_host.id"))

    name = Column(String(100))

    physcial_host = relationship("PhyscialHost",uselist = False,back_populates="virtual_machines")


if __name__ == '__main__':
  connect_url = "mysql+mysqldb://root:root@localhost/test"
  engine = create_engine(connect_url)
  Base.metadata.create_all(engine)