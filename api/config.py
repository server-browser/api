from datetime import timedelta
import os


DEBUG = os.getenv("DEBUG", False)
 
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))


SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", f"sqlite:///{BASE_PATH}/api.db?check_same_thread=False")

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379")