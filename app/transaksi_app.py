import datastore
from sqlalchemy.ext.asyncio import AsyncSession
from schema import tabung, tarik, saldo


async def tambahSaldo(data:tabung, db:AsyncSession):
    async with db as session:
        try:
            res, err = await datastore.tambahSaldo(data, session)
            if err is not None:
                return None, err
            await session.commit()
            return res, None
            
        except Exception as e:
            return None, e
        

async def tarikSaldo(data:tarik, db:AsyncSession):
    async with db as session:
        try:
            res, err = await datastore.tarikSaldo(data, session)
            if err is not None:
                return None, err
            await session.commit()
            return res, None
            
        except Exception as e:
            return None, e
        

async def cekSaldo(data:saldo, db:AsyncSession):
    async with db as session:
        try:
            res, err = await datastore.cekSaldo(data, session)
            if err is not None:
                return None, err
            await session.commit()
            return res, None
        
        except Exception as e:
            return None, e  
        
