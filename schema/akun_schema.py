from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class cabang(BaseModel):
    nama_cabang:str


class daftarAkun(BaseModel):
    nama:str
    nik:str
    no_hp:str
    nama_cabang:str


class cekMutasibyRek(BaseModel):
    no_rek:str
    tanggal_awal: Optional[datetime] = None
    tanggal_akhir: Optional[datetime] = None

class cekMutasibyName(BaseModel):
    nama:str
    tanggal_awal: Optional[datetime] = None
    tanggal_akhir: Optional[datetime] = None




