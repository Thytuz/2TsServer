class UserModel(object):
    def __init__(self, id=None, name=None, email=None, password=None, permission=None, token=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.permission = permission
        self.token = token
