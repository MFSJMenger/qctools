class CustomErrorMsg(Exception):

    def __init__(self, mgs):
        self.custom_error_msg = msg

    def __str__(self):
        return self.custom_error_msg

    def __repr__(self):
        return self.custom_error_msg
