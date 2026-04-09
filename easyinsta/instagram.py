from easyinsta.modules import Auth, Direct, Profiles


class Instagram:

    def __init__(self):
        self.auth = Auth()

        # Private modules (auth required for some methods)
        self.direct = Direct(self.auth)
        self.profiles = Profiles(self.auth)
