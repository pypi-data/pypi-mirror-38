class ListMixin(object):
    """For endpoints that have a ``/list`` method."""

    def list(self):
        """Calls the ``/list`` method of the endpoint."""
        url = self.glesys.API_BASE + self._ls_path
        return self.glesys.s.get(url).json()


class DetailsMixin(object):
    def details(self, _id=None, **kwargs):
        url = self.glesys.API_BASE + self._detail_path
        data = kwargs.copy()
        try:
            data.update({self._id_key: _id})
        except AttributeError:
            pass
        return self.glesys.s.post(url, json=data).json()
