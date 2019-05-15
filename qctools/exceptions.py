

class CustomErrorMsg(Exception):

    def __str__(self):
        return self.custom_error_msg


class UnkownProcessFunction(Exception):
    pass


class UnkownEvent(CustomErrorMsg):

    def __init__(self, event):
        self.custom_error_msg = ('Event "%s" unknown, please register before usage' 
                                  % event)

class MissingEventKeyword(CustomErrorMsg):

    def __init__(self, keyword):
        self.custom_error_msg = ("Keyword '%s' needs to be set in Event"
                                  % keyword)

class MissingEvent(CustomErrorMsg):

    def __init__(self, previous_event, current_event):
        self.custom_error_msg = (('Event "%s" needs to be' % previous_event,
                                  ' set and called before this Event "%s"'
                                  % current_event))


class MissingEventCall(CustomErrorMsg):

    def __init__(self, previous_event, current_event):
        self.custom_error_msg = (('Event "%s" needs to be' % previous_event,
                                  ' called before this Event "%s"'
                                  % current_event))

