# middleware.py
import time
from typing import Callable
from fastapi import Request, Response
from app.helper.logger import logger

async def log_requests(request: Request, call_next: Callable) -> Response:
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}ms".format(process_time)
    
    # Get just the path and query string
    path_with_query = request.url.path
    if request.url.query:
        path_with_query += "?" + request.url.query
    
    logger.info(
        f"{request.method} {path_with_query} status_code={response.status_code} {formatted_process_time}"
    )
    
    return response