"""
FastAPI Middleware
Location: /api/middleware.py
Purpose: Custom middleware for logging, rate limiting, etc.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import time
from collections import defaultdict
from datetime import datetime, timedelta

from utils.logger import get_logger

logger = get_logger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Request logging middleware"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        """Log request details"""
        start_time = time.time()
        
        # Log request
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )
        
        # Process request
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s"
        )
        
        # Add process time header
        response.headers["X-Process-Time"] = str(process_time)
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware (Namibian market: relaxed for UNAM, MTC)"""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next: Callable):
        """Rate limit requests"""
        # Get client identifier
        client_id = request.client.host if request.client else "unknown"
        
        # Check if client is from UNAM or MTC (relaxed limits)
        is_unam = "unam" in request.headers.get("User-Agent", "").lower()
        is_mtc = "mtc" in request.headers.get("User-Agent", "").lower()
        
        # Adjust rate limit for UNAM/MTC
        limit = self.requests_per_minute * 2 if (is_unam or is_mtc) else self.requests_per_minute
        
        # Clean old requests
        now = datetime.now()
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < timedelta(minutes=1)
        ]
        
        # Check rate limit
        if len(self.requests[client_id]) >= limit:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": "Too many requests. Please try again later.",
                        "details": {
                            "limit": limit,
                            "retry_after": 60
                        }
                    }
                },
                headers={"Retry-After": "60"}
            )
        
        # Add current request
        self.requests[client_id].append(now)
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(limit - len(self.requests[client_id]))
        response.headers["X-RateLimit-Reset"] = str(int((now + timedelta(minutes=1)).timestamp()))
        
        return response

