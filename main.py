from fastapi import FastAPI
import uvicorn
from api.api_router import router

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.0", port=8000)


