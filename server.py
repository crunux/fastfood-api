import uvicorn
from app.app import create_app
from app.config import settings

api = create_app(settings)

if __name__ == "__main__":
    uvicorn.run("server:api", port=5000, log_level='info', reload=True)
