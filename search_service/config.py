import os
from dotenv import load_dotenv


load_dotenv()


METADATA_SERVICE_URL = os.environ.get('METADATA_SERVICE_URL')
HTSGET_SERVICE_URL = os.environ.get('HTSGET_SERVICE_URL')
