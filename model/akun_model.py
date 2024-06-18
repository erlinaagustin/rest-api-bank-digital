from sqlalchemy import(
  Column, String, Integer, event
)

import random

from utils import Base

class Akuns(Base):
    __tablename__ = "akuns"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String)
    nik = Column(String)
    no_hp = Column(String)
    no_rek = Column(String(5), unique=True, nullable=False)
    saldo = Column(Integer, default=0)

def generate_no_rek(mapper, connection, target):
    target.no_rek = ''.join([str(random.randint(0, 9)) for _ in range(5)])


event.listen(Akuns, 'before_insert', generate_no_rek)
    
