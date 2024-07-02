from sqlalchemy import(
  Column, String, Integer, event, ForeignKey, select, DateTime, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
import random, enum
from sqlalchemy.sql import func

from utils import Base


class Mutasi(Base):
    __tablename__ = "mutasis"
    id = Column(Integer, primary_key = True, index = True)
    id_akun = mapped_column(ForeignKey("akuns.id"))
    id_sumber = mapped_column(ForeignKey("akuns.id"))
    id_tujuan = mapped_column(ForeignKey("akuns.id"))
    tanggal_transaksi = Column(DateTime(timezone=True), server_default=func.now())
    nominal = Column(Integer)
    jenis_transaksi = Column(String)
    akun = relationship("Akuns", foreign_keys=[id_akun], back_populates="mutasi")
    akun_sumber = relationship("Akuns", foreign_keys=[id_sumber], back_populates="mutasi_sumber")
    akun_tujuan = relationship("Akuns", foreign_keys=[id_tujuan], back_populates="mutasi_tujuan")

class Akuns(Base):
    __tablename__ = "akuns"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String)
    nik = Column(String)
    no_hp = Column(String)
    id_cabang = mapped_column(ForeignKey('cabangs.id'))
    no_rek = Column(String(8), unique=True, nullable=False)
    saldo = Column(Integer, default=0)
    cabang = relationship("Cabangs", back_populates="akun")
    mutasi = relationship("Mutasi", foreign_keys=[Mutasi.id_akun], back_populates="akun")
    mutasi_sumber = relationship("Mutasi", foreign_keys=[Mutasi.id_sumber], back_populates="akun_sumber")
    mutasi_tujuan = relationship("Mutasi", foreign_keys=[Mutasi.id_tujuan], back_populates="akun_tujuan")
    

def generate_no_rek(mapper, connection, target):
    cabang = connection.execute(select(Cabangs).filter(Cabangs.id == target.id_cabang)).fetchone()
    if not cabang:
        raise ValueError("ID cabang tidak ditemukan")
    target.no_rek = cabang.kode_cabang + ''.join([str(random.randint(0, 9)) for _ in range(5)])



event.listen(Akuns, "before_insert", generate_no_rek)

    
class Cabangs(Base):
    __tablename__ = "cabangs"
    id = Column(Integer, primary_key=True, index=True)
    nama_cabang = Column(String)
    kode_cabang = Column(String(3), unique=True, nullable=False)

    akun = relationship("Akuns", back_populates="cabang")

def generate_kode_cabang(mapper, connection, target):
    target.kode_cabang = ''.join(str(random.randint(0,9)) for _ in range(3))

def format_nama_cabang(mapper, connection, target):
    target.nama_cabang = target.nama_cabang.title()

event.listen(Cabangs, "before_insert", format_nama_cabang)
event.listen(Cabangs, "before_insert", generate_kode_cabang)




    


