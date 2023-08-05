import requests

from .exceptions import LoginException
from . import endpoints


class Glesys(object):
    """Main class for interacting with the GleSYS API.

    Both ``account`` and ``api_key`` needs to be specified or neither.
    If the latter, the :meth:`login` methods has to be called before
    trying to access any API resources.

    Args
    ----
    authinfo : tuple, optional
        Tuple of length 2 on the format ``(account number, api_key)``.

    """

    #: Base URL for the API
    API_BASE = "https://api.glesys.com"

    def __init__(self, authinfo=None):
        self.s = requests.Session()
        self.s.headers.update({"Content-Type": "application/json"})

        if authinfo and len(authinfo) != 2:
            raise ValueError("Wrong format for authinfo. Has to be of length 2.")
        elif authinfo:
            self.s.auth = authinfo

        #: Server: Server endpoint
        self.server = endpoints.Server(self)
        #: User: User endpoint
        self.user = endpoints.User(self)

    def login(self, username, password):
        """Authenticate using a username and password

        Note
        ----
        This method should only be used for local testing, when
        deploying a project using pyglesys, pass an account number
        and API key to the constructor instead.

        Args
        ----
        username : str
            The username of the user to authenticate.
        password : str
            The password of the user to authenticate.
        """
        payload = {"username": username, "password": password}
        res = self.s.post("{}/user/login".format(self.API_BASE), json=payload)
        if res.status_code != 200:
            resp_data = res.json()["response"]
            raise LoginException(resp_data["status"]["text"])
        login = res.json()["response"]["login"]
        account = login["accounts"][0]["account"]
        api_key = login["apikey"]
        self.s.auth = (account, api_key)
