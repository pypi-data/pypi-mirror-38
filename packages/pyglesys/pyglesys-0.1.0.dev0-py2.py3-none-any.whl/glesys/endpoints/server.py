from glesys import mixins
from .base import ModuleBase


class Server(mixins.ListMixin, mixins.DetailsMixin, ModuleBase):
    """Server API endpoint."""

    _ls_path = "/server/list"
    _detail_path = "/server/details"
    _id_key = "serverid"
