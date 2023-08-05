VERSION = (0, 1, 9)
__version__ = '.'.join(map(str, VERSION))

default_app_config = 'acmin.apps.AcminConfig'


from . import utils
from . import views