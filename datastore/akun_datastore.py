from schema import daftarAkun
from model import Akuns
from sqlalchemy import select,  update
import datetime

    
async def registrasi(data:daftarAkun, session):
    try:
        existing_nik = await session.execute(select(Akuns).filter(Akuns.nik == data.nik))
        if existing_nik.scalars().first():
            return None, "NIK sudah terdaftar"
        
        existing_no_hp = await session.execute(select(Akuns).filter(Akuns.no_hp == data.no_hp))
        if existing_no_hp.scalars().first():
            return None, "No HP sudah terdaftar"
        
        paramsInsert = Akuns(
            nik = data.nik,
            nama = data.nama,
            no_hp = data.no_hp
            )

        session.add(paramsInsert)
        await session.commit()
        await session.refresh(paramsInsert)
        return paramsInsert, None
    
    except Exception as e:
        return None, e

