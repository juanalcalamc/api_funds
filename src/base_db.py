from src.models.database import engine, Base
from src.utils.logging import logger
from src.models import pensions

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

logger.info("Base de datos creada correctamente con las tablas de pensions.py")