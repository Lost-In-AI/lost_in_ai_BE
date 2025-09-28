from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from api.api_router import router
from core.configs import settings
from exceptions.exceptions_handler import register_exception_handlers

description = """
# Lost in AI

Lost in AI simulates a phone customer service experience with the most frustrating elements: hold music, continuous transfers, and AI operators (via OpenAI) that never seem to understand the problem. All designed to be technically brilliant but deliberately useless, demonstrating skills in conversational AI, development, deploy and UX design.

While all chatbots try to be helpful, ours must be memorably useless but in a sophisticated and entertaining way.

## Tech Stack

* **Framework**: FastAPI 0.116.1
* **Runtime**: Python 3.12+
* **Database**: PostgreSQL con SQLAlchemy 2.0
* **Migrazioni**: Alembic 1.16.5
* **Autenticazione**: Clerk Backend API
* **AI Integration**: OpenAI GPT API
* **Deployment**: Vercel

"""

app = FastAPI(
    title=settings.APP_NAME,
    description=description,
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://lost-in-ai-fe.vercel.app",
        "https://lost-in-ai-fe.vercel.app/",
        "https://lost-in-ai-fe-ivory.vercel.app/",
        "https://lost-in-ai-fe-git-feat-db-logic-74-lara-filippones-projects.vercel.app/",
        "https://7a39fe5f8410.ngrok-free.app"
    ],
    allow_origin_regex=(
        r"^https://lost-in-ai-fe/.vercel/.app.*$"
    ),
)

app.include_router(router, prefix='/api')
register_exception_handlers(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
