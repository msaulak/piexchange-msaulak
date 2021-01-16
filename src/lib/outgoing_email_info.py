class OutgoingEmailInfor:
    def __init__(self, to: str, subject: str = None, body: str = None):
        self.to = to
        self.subject = subject
        self.body = body

