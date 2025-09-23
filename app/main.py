from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from api.api_router import router
from api.webhook import router as webhook
from core.configs import settings
from exceptions.exceptions_handler import register_exception_handlers


app = FastAPI(
    title=settings.APP_NAME
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://lost-in-ai-fe.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(router, prefix='/api')
app.include_router(webhook, prefix='/webhook')
register_exception_handlers(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
