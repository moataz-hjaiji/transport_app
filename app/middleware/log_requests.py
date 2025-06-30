# In middleware.py
from fastapi import Request
from time import time
from app.helper.logger import logger

async def log_requests(request: Request, call_next):
    start_time = time()
    
    response = await call_next(request)
    
    process_time = (time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    
    logger.info(
        f"Request: {request.method} {request.url.path} "
        f"completed in {formatted_process_time}ms "
        f"status_code={response.status_code}"
    )
    
    return response