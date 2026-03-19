from easyinsta.modules import Profiles, Validators


class Instagram:

    def __init__(self):
        # Public modules (no auth required)
        self.validators = Validators()
        self.profiles = Profiles()

        # Private modules (auth required)
        # self.auth = Auth(self._session)
        # self.direct = Direct(self._session)
