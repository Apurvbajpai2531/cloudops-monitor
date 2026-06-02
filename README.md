# CloudOps Monitor Architecture

```text
                         GitHub Repository
                                 │
                                 ▼
                      GitHub Actions CI/CD
                                 │
                                 ▼
                         Docker Build Process
                                 │
                                 ▼
                      Kubernetes Deployment
                                 │
      ┌──────────────────────────┼──────────────────────────┐
      │                          │                          │
      ▼                          ▼                          ▼

 ┌─────────────┐         ┌─────────────┐          ┌─────────────┐
 │  Frontend   │         │   Backend   │          │ PostgreSQL  │
 │ Streamlit   │◄──────► │   FastAPI   │ ◄──────► │  Database   │
 └─────────────┘         └─────────────┘          └─────────────┘
        │                        │
        │                        │
        ▼                        ▼

 ┌─────────────────────────────────────────────┐
 │           OpenTelemetry Collector           │
 └─────────────────────────────────────────────┘
                        │
                        ▼

 ┌─────────────────────────────────────────────┐
 │                Prometheus                   │
 │     Metrics Collection & Monitoring         │
 └─────────────────────────────────────────────┘
                        ▲
                        │
                        │
               ┌────────────────┐
               │ Node Exporter  │
               │ Host Metrics   │
               └────────────────┘
                        │
                        ▼

 ┌─────────────────────────────────────────────┐
 │                  Grafana                    │
 │      Dashboards & Visualization             │
 └─────────────────────────────────────────────┘


Monitoring Flow:
Node Exporter ──► Prometheus ──► Grafana

Application Flow:
User ──► Streamlit Frontend ──► FastAPI Backend ──► PostgreSQL

Observability Flow:
FastAPI ──► OpenTelemetry Collector ──► Monitoring Stack

Deployment Flow:
GitHub Push ──► GitHub Actions ──► Docker Build ──► Kubernetes
```
