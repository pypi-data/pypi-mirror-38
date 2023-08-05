from glesys import mixins
from .base import ModuleBase


class User(mixins.DetailsMixin, ModuleBase):
    _detail_path = "/user/details"
