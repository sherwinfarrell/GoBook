class User:

    def ___init__(self, user_id, username):
        self.user_id = user_id
        self.username = username


    @staticmethod
    def get_admin():
        return User('admin', 'admin')