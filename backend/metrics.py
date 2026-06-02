from prometheus_client import Counter, Gauge

api_requests_total = Counter(
    "api_requests_total",
    "Total API requests",
    ["endpoint"]
)

server_count = Gauge(
    "server_count",
    "Total number of registered servers"
)

healthy_servers = Gauge(
    "healthy_servers",
    "Total healthy servers"
)

unhealthy_servers = Gauge(
    "unhealthy_servers",
    "Total unhealthy servers"
)
