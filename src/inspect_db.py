from models.database import engine, Base
from models import pensions 


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Base de datos creada correctamente con las tablas de pensions_funds.py")