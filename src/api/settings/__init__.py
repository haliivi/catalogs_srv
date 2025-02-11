try:
    from .local_settings import *
except ImportError:
    from .deploy_settings import *
