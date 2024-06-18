from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import akun_app, transaksi_app
from utils import get_async_session, respOutCustom
from schema import daftarAkun, tabung, tarik, saldo

router = APIRouter()


@router.post("/daftar/")
async def registrasiRouter(
    request: daftarAkun,
    db: AsyncSession = Depends(get_async_session)
):
    outResponse, err = await akun_app.registerAkun(request, db)
    if err is not None:
        if err == "NIK sudah terdaftar":
            return respOutCustom("400", err, None)
        elif err == "No HP sudah terdaftar":
            return respOutCustom("400", err, None)
        else:
            respOutCustom("02", f"registrasi akun gagal: {err}", None)
    
    return respOutCustom("200", "success", {"no_rek": outResponse.no_rek})


@router.post("/tabung/")
async def tabungRouter(
    request:tabung,
    db:AsyncSession = Depends(get_async_session)
):
    outResponse, err = await transaksi_app.tambahSaldo(request, db)
    if err is not None:
        if err == "Nomor rekening tidak dikenali":
            return respOutCustom("400", err, None)
        else:
            return respOutCustom("02", f"gagal menabung: {err}", None)
    
    return respOutCustom("200", "sukses", outResponse)


@router.post("/tarik/")
async def tarikRouter(
    request:tarik,
    db:AsyncSession = Depends(get_async_session)
):
    outResponse, err = await transaksi_app.tarikSaldo(request, db)
    if err is not None:
        if err == "Nomor rekening tidak dikenali":
            return respOutCustom("400", err, None)
        elif err == "Saldo tidak cukup":
            return respOutCustom("400", err, None)
        else:
            return respOutCustom("02", f"tarik tunai gagal: {err}", None)
    
    return respOutCustom("200", "sukses", outResponse)


@router.get("/saldo/")
async def saldoRouter(
    no_rek:str,
    db: AsyncSession = Depends(get_async_session)
):
    request = saldo(no_rek = no_rek)
    outResponse, err = await transaksi_app.cekSaldo(request, db)
    if err is not None:
        if err == "Nomor rekening tidak dikenali":
            return respOutCustom("400", err, None)
        else:
            return respOutCustom("02", f"data gagal ditampilkan: {err}", None)
    return respOutCustom("200", "sukses", outResponse)

