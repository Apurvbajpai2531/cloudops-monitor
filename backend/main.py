from fastapi import FastAPI, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from prometheus_client import generate_latest

from database import Base, engine, SessionLocal
from models import Server
from schemas import ServerCreate, ServerResponse
from metrics import (
    api_requests_total,
    server_count,
    healthy_servers,
    unhealthy_servers
)
from otel import setup_otel

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CloudOps Monitor API")

setup_otel(app)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def update_metrics(db: Session):
    servers = db.query(Server).all()
    server_count.set(len(servers))
    healthy_servers.set(len([s for s in servers if s.status == "healthy"]))
    unhealthy_servers.set(len([s for s in servers if s.status == "unhealthy"]))

@app.get("/")
def root():
    api_requests_total.labels(endpoint="/").inc()
    return {"message": "CloudOps Monitor Backend Running"}

@app.get("/health")
def health():
    api_requests_total.labels(endpoint="/health").inc()
    return {"status": "healthy"}

@app.post("/servers", response_model=ServerResponse)
def create_server(server: ServerCreate, db: Session = Depends(get_db)):
    api_requests_total.labels(endpoint="/servers").inc()

    new_server = Server(**server.dict())
    db.add(new_server)
    db.commit()
    db.refresh(new_server)

    update_metrics(db)
    return new_server

@app.get("/servers", response_model=list[ServerResponse])
def get_servers(db: Session = Depends(get_db)):
    api_requests_total.labels(endpoint="/servers").inc()

    servers = db.query(Server).all()
    update_metrics(db)
    return servers

@app.patch("/servers/{server_id}/status")
def update_server_status(server_id: int, status: str, db: Session = Depends(get_db)):
    api_requests_total.labels(endpoint="/servers/status").inc()

    server = db.query(Server).filter(Server.id == server_id).first()

    if not server:
        return {"error": "Server not found"}

    server.status = status
    db.commit()
    update_metrics(db)

    return {"message": "Status updated", "id": server_id, "status": status}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
