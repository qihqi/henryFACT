from django.core.management import setup_environ
import sys
sys.path.append('/var/servidor/henry')
import settings
setup_environ(settings)
from productos.models import *

from mostSelled import *
from delete_past_data import *
ALL_JOBS = ( delete_past_data,
        )

for jobs in ALL_JOBS:
    jobs()
