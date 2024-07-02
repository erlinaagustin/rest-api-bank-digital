from schema import daftarAkun, cabang, cekMutasibyRek, cekMutasibyName
from model import Akuns, Cabangs, Mutasi
from sqlalchemy import select,  update
import datetime

    
async def daftarCabang(data: cabang, session):
    try:
        existing_cabang   = await session.execute(select(Cabangs).filter(Cabangs.nama_cabang == data.nama_cabang.title()))
        if existing_cabang.scalars().first():
            raise Exception(f"Kantor cabang {data.nama_cabang.title()} sudah terdaftar")
        
        paramsInsert = Cabangs(
            nama_cabang = data.nama_cabang
        )

        session.add(paramsInsert)
        await session.commit()
        await session.refresh(paramsInsert)
        return paramsInsert, None
    
    except Exception as e:
        return None, e


async def registrasi(data:daftarAkun, session):
    try:
        if not data.nik.isdigit() or len(data.nik) != 16:
            raise Exception("NIK harus terdiri dari 16 digit angka")
        
        if not data.no_hp.isdigit() or len(data.no_hp) != 12:
            raise Exception("Nomor Hp harus terdiri dari 12 digit angka")
            
        existing_nik = await session.execute(select(Akuns).filter(Akuns.nik == data.nik))
        if existing_nik.scalars().first():
            raise Exception ("NIK sudah terdaftar")
        
        existing_no_hp = await session.execute(select(Akuns).filter(Akuns.no_hp == data.no_hp))
        if existing_no_hp.scalars().first():
            raise Exception ("No HP sudah terdaftar")
        
        existing_cabang = await session.execute(select(Cabangs).filter(Cabangs.nama_cabang == data.nama_cabang.title()))
        cabang = existing_cabang.scalars().first()
        
        if not cabang:
            return None, f"Kantor cabang {data.nama_cabang.title()} tidak ditemukan"
        
        paramsInsert = Akuns(
            nik = data.nik,
            nama = data.nama,
            no_hp = data.no_hp,
            id_cabang = cabang.id
            )

        session.add(paramsInsert)
        await session.commit()
        await session.refresh(paramsInsert)
        return paramsInsert, None
    
    except Exception as e:
        return None, e
    
async def cekMutasiByRekening(data: cekMutasibyRek, session):
    try:
        akun = await session.execute(select(Akuns).filter(Akuns.no_rek == data.no_rek))
        akun = akun.scalars().first()

        if not akun:
            raise Exception(f"Nomor rekening {akun.no_rek} tidak ditemukan")

        query = select(Mutasi).filter(
            (Mutasi.id_akun == akun.id) |
            (Mutasi.id_sumber == akun.id) |
            (Mutasi.id_tujuan == akun.id)
        )

        if data.tanggal_awal:
            query = query.filter(Mutasi.tanggal_transaksi >= data.tanggal_awal)
        if data.tanggal_akhir:
            query = query.filter(Mutasi.tanggal_transaksi <= data.tanggal_akhir)

        result = await session.execute(query)
        mutasi_list = result.scalars().all()
        

        mutasi_detailed = []
        for mutasi in mutasi_list:
            mutasi_info = {
                "id": mutasi.id,
                "tanggal_transaksi": mutasi.tanggal_transaksi,
                "nominal": mutasi.nominal,
                "jenis_transaksi": mutasi.jenis_transaksi,
                "no_rek_sumber": None,
                "no_rek_tujuan": None,
            }
            if mutasi.jenis_transaksi == "transfer":
                sumber = await session.execute(select(Akuns.no_rek).filter(Akuns.id == mutasi.id_sumber))
                tujuan = await session.execute(select(Akuns.no_rek).filter(Akuns.id == mutasi.id_tujuan))
                mutasi_info["no_rek_sumber"] = sumber.scalar()
                mutasi_info["no_rek_tujuan"] = tujuan.scalar()
            
            mutasi_detailed.append(mutasi_info)

        return mutasi_detailed, None

    except Exception as e:
        return None, e
    

async def cekMutasiByName(data: cekMutasibyName, session):
    try:
        akun_result = await session.execute(select(Akuns).where(Akuns.nama.ilike(f"%{data.nama}%")))
        akun_list = akun_result.scalars().all()

        if not akun_list:
            raise Exception(f"Rekening dengan nama {data.nama} tidak ditemukan")

        all_mutasi_detailed = []
        no_transaction_accounts = []

        for akun in akun_list:
            query = select(Mutasi).filter(
                (Mutasi.id_akun == akun.id) |
                (Mutasi.id_sumber == akun.id) |
                (Mutasi.id_tujuan == akun.id)
            )

            if data.tanggal_awal:
                query = query.filter(Mutasi.tanggal_transaksi >= data.tanggal_awal)
            if data.tanggal_akhir:
                query = query.filter(Mutasi.tanggal_transaksi <= data.tanggal_akhir)

            result = await session.execute(query)
            mutasi_list = result.scalars().all()

            if not mutasi_list:
                no_transaction_accounts.append(akun.nama)
                continue

            for mutasi in mutasi_list:
                mutasi_info = {
                    "id": mutasi.id,
                    "tanggal_transaksi": mutasi.tanggal_transaksi,
                    "nominal": mutasi.nominal,
                    "jenis_transaksi": mutasi.jenis_transaksi,
                    "no_rek_sumber": None,
                    "no_rek_tujuan": None,
                }
                if mutasi.jenis_transaksi == "transfer":
                    sumber_result = await session.execute(select(Akuns.no_rek).filter(Akuns.id == mutasi.id_sumber))
                    tujuan_result = await session.execute(select(Akuns.no_rek).filter(Akuns.id == mutasi.id_tujuan))
                    mutasi_info["no_rek_sumber"] = sumber_result.scalar()
                    mutasi_info["no_rek_tujuan"] = tujuan_result.scalar()
                
                all_mutasi_detailed.append(mutasi_info)

        if not all_mutasi_detailed and no_transaction_accounts:
            return {"message": "belum ada transaksi", "no_transaction_accounts": no_transaction_accounts}, None

        return {"mutasi_detailed": all_mutasi_detailed, "no_transaction_accounts": no_transaction_accounts}, None

    except Exception as e:
        return None, str(e)

    


    


