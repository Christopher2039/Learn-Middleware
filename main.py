from fastapi import FastAPI, Request

# from custom_middleware.timing import timing_middleware
# from custom_middleware.allow_ip import allow_ip_middleware
from custom_middleware.rate_limiter import RateLimitingMiddleware


app = FastAPI()
# app.middleware("http")(timing_middleware)
# app.middleware("http")(allow_ip_middleware)
app.add_middleware(RateLimitingMiddleware, max_requests=10, time_window=60)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}