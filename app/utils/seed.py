from app.controllers.users import create
from app.utils.logger import logger_setup
from sqlmodel import Session
from app.database import engine
from app.config import settings
from app.models.users import UserCreate
from datetime import datetime

logger = logger_setup(__name__)




def create_admin():
    userAcesss = None
    with Session(engine) as db:
        init_user = UserCreate(
            name = settings.API_USERNAME,
            email = settings.API_EMAIL,
            password = settings.API_PASSWORD,
            is_active = True,
            is_superuser = True,
            date_of_birth = datetime(1995, 5, 2).isoformat(),
            personalID = "8299609519"
        )
        try: 
            create(init_user, userAcesss, db)
            logger.info("Admin created successfully!")
            logger.info("Email: %s", init_user.email)
            logger.info("Password: %s", init_user.password)
        except Exception as e:
            logger.error("Error creating admin: %s", e)
            logger.error("Admin already exists")
            return