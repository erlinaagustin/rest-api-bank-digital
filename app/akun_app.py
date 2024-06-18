import datastore
from sqlalchemy.ext.asyncio import AsyncSession
from schema import daftarAkun
        

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

        
