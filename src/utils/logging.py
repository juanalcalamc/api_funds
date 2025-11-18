import logging
from  logging.handlers import RotatingFileHandler


handler = RotatingFileHandler("utils/logs/app.log", maxBytes=1000000, backupCount=5)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
 
logger = logging.getLogger("api_funds")
logger.setLevel(logging.ERROR)
logger.addHandler(handler)

