

"""
Append Entries request message.
"""
APPEND_ENTRIES = 1

"""
Append Entries response message.
"""
APPEND_RESPONSE = 2

"""
Vote request message.
"""
VOTE_REQUEST = 3

"""
Vote response message.
"""
VOTE_RESPONSE = 4


class Message(object):
    def __init__(self, type, sender, recipient, term, mode, data):
        """
        :param int type:
        :param str sender:
        :param str recipient:
        :param int term:
        :param int mode:
        :param dict data:
        """
        self.type = type
        self.sender = sender
        self.recipient = recipient
        self.term = term
        self.mode = mode
        self.data = data

    @staticmethod
    def build(message_type, state, recipient, data):
        """
        :param int message_type:
        :param state.State state:
        :param str recipient:
        :param dict data:
        :rtype: Message
        """
        return Message(message_type, state.node.name, recipient, state.current_term, state.node.mode, data)

    def __str__(self):
        if self.type == APPEND_ENTRIES:
            m_type = "APPEND_ENTRIES"
        elif self.type == APPEND_RESPONSE:
            m_type = "APPEND_RESPONSE"
        elif self.type == VOTE_REQUEST:
            m_type = "VOTE_REQUEST"
        elif self.type == VOTE_RESPONSE:
            m_type = "VOTE_RESPONSE"
        else:
            m_type = "UNKNOWN(%2d)" % self.type

        return "{0}[{1}]({2}:{3}|{4})".format(m_type, self.term, self.sender, self.recipient, self.data)

    def is_response(self):
        return self.type in [VOTE_RESPONSE, APPEND_RESPONSE]
