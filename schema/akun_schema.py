from pydantic import BaseModel

class daftarAkun(BaseModel):
    nama:str
    nik:str
    no_hp:str


