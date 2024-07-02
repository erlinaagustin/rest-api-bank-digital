from pydantic import BaseModel



class tabung(BaseModel):
    no_rek:str
    nominal:int


class tarik(BaseModel):
    no_rek:str
    nominal:int

class saldo(BaseModel):
    no_rek:str

class transfer(BaseModel):
    no_rek_sumber:str
    no_rek_tujuan:str
    nominal:int


