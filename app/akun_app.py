import datastore
from sqlalchemy.ext.asyncio import AsyncSession
from schema import daftarAkun, cabang, cekMutasibyRek, cekMutasibyName
        

async def tambahCabang(data: cabang, db: AsyncSession):
    async with db as session:
        try:
            res, err = await datastore.daftarCabang(data, session)
            if err is not None:
                return None, err
            await session.commit()
            return res, None
        
        except Exception as e:
            return None, str(e)


async def registerAkun(data: daftarAkun, db: AsyncSession):
    async with db as session:
        try:
            res, err = await datastore.registrasi(data, session)
            if err is not None:
                return None, err
            await session.commit()
            return res, None

        except Exception as e:
            return None, str(e)
        
async def cekMutasi(data: cekMutasibyRek, db: AsyncSession):
    async with db as session:
        try:
            res, err = await datastore.cekMutasiByRekening(data, session)
            if err is not None:
                return None, err
            await session.commit()
            return res, None

        except Exception as e:
            return None, str(e)
        
async def cekMutasibyNama(data: cekMutasibyName, db: AsyncSession):
    async with db as session:
        try:
            res, err = await datastore.cekMutasiByName(data, session)
            if err is not None:
                return None, err
            await session.commit()
            return res, None

        except Exception as e:
            return None, str(e)
        


        
