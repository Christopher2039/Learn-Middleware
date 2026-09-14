from fastapi import Request, status
from fastapi.responses import JSONResponse

async def allow_ip_middleware(request: Request, call_next):
    # client_ip = request.client.host
    client_ip = "127.0.0.1"
    allowed_ips = ["127.0.0.1", "192.168.1.1"]  # Example allowed IPs
    if client_ip not in allowed_ips:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content="Access denied: Your IP is not allowed.")

    response = await call_next(request)

    return response
