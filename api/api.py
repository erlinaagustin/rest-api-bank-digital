from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime
from app import akun_app, transaksi_app
from utils import get_async_session, respOutCustom
from schema import daftarAkun, tabung, tarik, saldo, transfer, cabang, cekMutasibyRek, cekMutasibyName

router = APIRouter()


@router.post("/daftar-cabang")
async def cabangRouter(
    request: cabang,
    db: AsyncSession = Depends(get_async_session)
):
    outResponse, err = await akun_app.tambahCabang(request, db)
    if err is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail = f"tambah cabang gagal: {err}")
    
    return respOutCustom(status.HTTP_200_OK, "sukses", {"kode cabang": outResponse.kode_cabang})


@router.post("/daftar/")
async def registrasiRouter(
    request: daftarAkun,
    db: AsyncSession = Depends(get_async_session)
):
    outResponse, err = await akun_app.registerAkun(request, db)
    if err is not None:
       raise HTTPException(status.HTTP_400_BAD_REQUEST, detail = f"registrasi akun gagal: {err}")
    
    return respOutCustom(status.HTTP_200_OK, "sukses", {"no_rek": outResponse.no_rek})


@router.post("/tabung/")
async def tabungRouter(
    request:tabung,
    db:AsyncSession = Depends(get_async_session)
):
    outResponse, err = await transaksi_app.tambahSaldo(request, db)
    if err is not None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, detail = f"gagal menabung: {err}")
    
    return respOutCustom(status.HTTP_200_OK, "sukses", outResponse)


@router.post("/tarik/")
async def tarikRouter(
    request:tarik,
    db:AsyncSession = Depends(get_async_session)
):
    outResponse, err = await transaksi_app.tarikSaldo(request, db)
    if err is not None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, detail = f"tarik tunai gagal: {err}")
    
    return respOutCustom(status.HTTP_200_OK, "sukses", outResponse)


@router.get("/saldo/")
async def saldoRouter(
    no_rek:str,
    db: AsyncSession = Depends(get_async_session)
):
    request = saldo(no_rek = no_rek)
    outResponse, err = await transaksi_app.cekSaldo(request, db)
    if err is not None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, detail = f"data gagal ditampilkan: {err}")
    
    return respOutCustom(status.HTTP_200_OK, "sukses", outResponse)


@router.post("/transfer/")
async def transferRouter(
    request:transfer,
    db:AsyncSession = Depends(get_async_session)
):
    outResponse, err = await transaksi_app.transferUang(request, db)
    if err is not None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, detail = f"transfer gagal: {err}")
    
    return respOutCustom(status.HTTP_200_OK, "sukses", outResponse)


@router.get("/cek-mutasi-by-rekening/")
async def cekMutasibyRekeningRouter(
    no_rek: str,
    tanggal_awal: Optional[datetime] = None,
    tanggal_akhir: Optional[datetime] = None,
    db: AsyncSession = Depends(get_async_session)
):
    request = cekMutasibyRek(no_rek=no_rek, tanggal_awal= tanggal_awal, tanggal_akhir=tanggal_akhir)
    outResponse, err = await akun_app.cekMutasi(request, db)
    if err is not None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, detail = f"cek mutasi gagal: {err}")
    return respOutCustom(status.HTTP_200_OK, "sukses", outResponse)

@router.get("/cek-mutasi-by-nama/")
async def cekMutasibyNameRouter(
    nama: str,
    tanggal_awal: Optional[datetime] = None,
    tanggal_akhir: Optional[datetime] = None,
    db: AsyncSession = Depends(get_async_session)
):
    request = cekMutasibyName(nama=nama, tanggal_awal=tanggal_awal, tanggal_akhir=tanggal_akhir)
    outResponse, err = await akun_app.cekMutasibyNama(request, db)
    if err is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"cek mutasi gagal: {err}")

    if "mutasi_detailed" in outResponse and "no_transaction_accounts" in outResponse:
        return respOutCustom(status.HTTP_200_OK, "sukses", outResponse)
    if "no_transaction_accounts" in outResponse and "message" in outResponse:
        return respOutCustom(status.HTTP_200_OK, outResponse["message"], outResponse)

    return respOutCustom(status.HTTP_200_OK, "sukses", outResponse)

