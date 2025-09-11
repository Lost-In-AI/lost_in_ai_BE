from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from api.api_router import router
from core.configs import settings


app = FastAPI(
    title=settings.APP_NAME
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # TODO solo per i test
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
