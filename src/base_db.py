from database.models.database import engine, Base
from utils.logging import logger

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

logger.info("Base de datos creada correctamente con las tablas de pensions.py")