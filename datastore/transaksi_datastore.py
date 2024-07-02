from schema import tabung, tarik, saldo, transfer
from model import Akuns, Mutasi
from sqlalchemy import select,  update

        

async def tambahSaldo(data: tabung, session):
    try:
        existing_account = await session.execute(select(Akuns).filter(Akuns.no_rek == data.no_rek))
        account = existing_account.scalars().first()
        
        if not account:
            raise Exception(f"Nomor rekening {data.no_rek} tidak dikenali")

        query = update(Akuns).where(Akuns.no_rek == data.no_rek).values(
            saldo=Akuns.saldo + data.nominal)
        
        await session.execute(query)
        await session.commit()

        paramsInsert = Mutasi(
            id_akun = account.id,
            nominal = data.nominal,
            jenis_transaksi = "tabung"
        )

        session.add(paramsInsert)
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
            raise Exception(f"Nomor rekening {data.no_rek} tidak dikenali")
        
        if data.nominal > account.saldo:
            raise Exception (f"Saldo tidak cukup. saldo anda saat ini {account.saldo}")
        
        query = update(Akuns).where(Akuns.no_rek == data.no_rek).values(
            saldo=Akuns.saldo - data.nominal)
        
        await session.execute(query)
        await session.commit()

        paramsInsert = Mutasi(
            id_akun = account.id,
            nominal = data.nominal,
            jenis_transaksi = "tarik tunai"
        )

        session.add(paramsInsert)
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
            raise Exception (f"Nomor rekening {data.no_rek} tidak dikenali")
        
        saldo_account = account.saldo

        return saldo_account, None
    except Exception as e:
        return None, e
    
async def transferUang(data: transfer, session):
    try:
        
        
        no_rek_sumber = await session.execute(select(Akuns).filter(Akuns.no_rek == data.no_rek_sumber))
        no_rek_sumber = no_rek_sumber.scalars().first()
        if not no_rek_sumber:
            raise Exception(f"Nomor rekening {data.no_rek_sumber} tidak ditemukan")
        
        no_rek_tujuan = await session.execute(select(Akuns).filter(Akuns.no_rek == data.no_rek_tujuan))
        no_rek_tujuan = no_rek_tujuan.scalars().first()
        if not no_rek_tujuan:
            raise Exception(f"Nomor rekening {data.no_rek_tujuan} tidak ditemukan")
        
        if data.nominal < 10000:
            raise Exception ("Nominal transfer minimal 10.000")
        
        if no_rek_sumber.saldo < data.nominal:
            raise Exception (f"Saldo tidak cukup. saldo anda saat ini adalah {no_rek_sumber.saldo}")
        
        no_rek_sumber.saldo = no_rek_sumber.saldo - data.nominal
        no_rek_tujuan.saldo = no_rek_tujuan.saldo + data.nominal

        await session.commit()

        paramsInsert = Mutasi(
            id_akun = no_rek_sumber.id,
            id_sumber = no_rek_sumber.id,
            id_tujuan = no_rek_tujuan.id,
            nominal = data.nominal,
            jenis_transaksi = "transfer"
        )

        session.add(paramsInsert)
        await session.commit()

        return {"message": f"Transfer ke {data.no_rek_tujuan} berhasil"}, None
    except Exception as e:
        return None, e

