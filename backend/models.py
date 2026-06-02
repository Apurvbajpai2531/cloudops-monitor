from sqlalchemy import Column, Integer, String
from database import Base

class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ip = Column(String, nullable=False)
    environment = Column(String, nullable=False)
    region = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    application = Column(String, nullable=False)
    status = Column(String, default="healthy")
