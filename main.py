from datetime import datetime, timezone
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
import requests

app = FastAPI()


# Configure Rate limiter
limiter = Limiter(key_func=get_remote_address)

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        content={"detail":"Too many requests. Please try again later"})

app.state.limiter = limiter


# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoint
@app.get("/me")
@limiter.limit("5/minute")
def get_user_details(request: Request):
    user_data = {
        "email": "davideneasatochibueze@gmail.com",
        "name": "David Eneasato",
        "stack": "Python/FastAPI"
    }

    # Handle third party server error gracefully
    cat_fact = "Could not fetch cat fact at the moment. please try again later"
    try:
        response = requests.get("https://catfact.ninja/fact", timeout=5)
        response.raise_for_status()
        cat_fact = response.json().get("fact", cat_fact)
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error fetching cat fact: {e}")
    
    # Return response
    result = {
        "status":"success",
        "user": user_data,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "fact": cat_fact
    }
    return JSONResponse(content=result)