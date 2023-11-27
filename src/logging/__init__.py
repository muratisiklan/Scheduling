import os
import sys
import logging
from datetime import datetime


LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
log_dir = "LOGS"
logs_path = os.path.join(log_dir,  LOG_FILE)
os.makedirs(log_dir, exist_ok=True)


LOG_FILE_PATH = os.path.join(logs_path)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("cnnClassifierLogger")
