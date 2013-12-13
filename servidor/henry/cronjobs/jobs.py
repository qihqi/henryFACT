from django.core.management import setup_environ
import sys
sys.path.append('/var/servidor/henry')
import settings
setup_environ(settings)
from productos.models import *

from mostSelled import *
from snapshot.heavylifter import *

ALL_JOBS = ( update_record,
        )

for jobs in ALL_JOBS:
    jobs()
