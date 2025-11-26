from fastapi import FastAPI
import asyncio
import httpx
from contextlib import asynccontextmanager
from app.core.config import env_conf

async def periodic_call():
    """Background task to keep server alive on render"""
    while True:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(env_conf.API_ENDPOINT)
                print(f"Periodic call response: {response.status_code}")
        except Exception as e:
            print(f"Error in periodic call: {e}")
        
        await asyncio.sleep(300)  

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Starting background task
    task = asyncio.create_task(periodic_call())
    print("Background task started - calling backend every 5 minutes")
    yield
    # Canceling task when app shuts down
    task.cancel()

