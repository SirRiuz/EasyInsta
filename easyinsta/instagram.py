from easyinsta.modules import Auth, Direct, Profiles, Validators


class Instagram:

    def __init__(self):
        self.auth = Auth()

        # Public modules (no auth required)
        self.validators = Validators()

        # Private modules (auth required)
        self.direct = Direct(self.auth)
        self.profiles = Profiles(self.auth)
