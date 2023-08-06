__version__ = '1.2.2'

from .datastrctures import Result, Valid, MethodProxy
from .para import para_ok_or_400, perm_ok_or_403
from .doc import patch_all

__all__ = ("Result", "MethodProxy", "Valid", "para_ok_or_400", "perm_ok_or_403")
patch_all()
