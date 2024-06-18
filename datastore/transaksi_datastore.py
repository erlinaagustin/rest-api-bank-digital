from schema import tabung, tarik, saldo
from model import Akuns
from sqlalchemy import select,  update

    
async def tambahSaldo(data: tabung, session):
    try:
        existing_account = await session.execute(select(Akuns).filter(Akuns.no_rek == data.no_rek))
        account = existing_account.scalars().first()
        
        if not account:
            return None, "Nomor rekening tidak dikenali"

        query = update(Akuns).where(Akuns.no_rek == data.no_rek).values(
            saldo=Akuns.saldo + data.nominal)
        
        await session.execute(query)
        await session.commit()

        select_query = select(Akuns.saldo).where(Akuns.no_rek == data.no_rek)
        result = await session.execute(select_query)
        updated_saldo = result.scalar_one()
        
        return {"saldo": updated_saldo}, None
    except Exception as e:
        return None, e
    
    
async def tarikSaldo(data: tarik, session):
    try:
        existing_account = await session.execute(select(Akuns).filter(Akuns.no_rek == data.no_rek))
        account = existing_account.scalars().first()
        
        if not account:
            return None, "Nomor rekening tidak dikenali"
        
        if data.nominal > account.saldo:
            return None, "Saldo tidak cukup"
        
        query = update(Akuns).where(Akuns.no_rek == data.no_rek).values(
            saldo=Akuns.saldo - data.nominal)
        
        await session.execute(query)
        await session.commit()

        select_query = select(Akuns.saldo).where(Akuns.no_rek == data.no_rek)
        result = await session.execute(select_query)
        updated_saldo = result.scalar_one()
        
        return {"saldo": updated_saldo}, None
    except Exception as e:
        return None, e
    
async def cekSaldo(data: saldo, session):
    try:
        existing_account = await session.execute(select(Akuns).filter(Akuns.no_rek == data.no_rek))
        account = existing_account.scalars().first()
        
        if not account:
            return None, "Nomor rekening tidak dikenali"
        
        saldo_account = account.saldo

        return saldo_account, None
    except Exception as e:
        return None, e

