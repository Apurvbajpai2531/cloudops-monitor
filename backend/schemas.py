from pydantic import BaseModel

class ServerCreate(BaseModel):
    name: str
    ip: str
    environment: str
    region: str
    owner: str
    application: str

class ServerResponse(ServerCreate):
    id: int
    status: str

    class Config:
        from_attributes = True
