from easyinsta.modules import Account, Auth, Direct, Profiles


class Instagram:

    def __init__(self):
        self.auth = Auth()

        # Private modules (auth required for some methods)
        self.account = Account(self.auth)
        self.direct = Direct(self.auth)
        self.profiles = Profiles(self.auth)
