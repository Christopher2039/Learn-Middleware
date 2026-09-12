from fastapi import  Request, Response, status
from collections import defaultdict
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse


class RateLimitingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, time_window, max_requests):
        super().__init__(app)
        self.time_window = time_window
        self.max_requests = max_requests
        self.requests = defaultdict(list)

    async def dispatch(self, request:Request, call_next) -> Response:
        """"""
        client_ip = request.client.host
        current_time = time.time()

        # Get the list of request times for the client IP
        times_list = self.requests[client_ip]

        # Removes requests outside the window
        times_list = [time_stamp for time_stamp in times_list if time_stamp > current_time - self.time_window ]
        self.requests[client_ip] = times_list

        # Check if the client exceeds the max request limit
        if len(times_list) >= self.max_requests:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content="Limit Reached"
            )
        
         # Add the current request time to the list
        times_list.append(current_time)
            
        # Proceed with the request
        response = await call_next(request)

        response.headers["custom"] = str(self.requests)
        return response