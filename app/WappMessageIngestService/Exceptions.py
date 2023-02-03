from app.LoggingService.DefaultLogger import logger


class Error(Exception):
    """Base class for other exceptions"""
    pass


class UnknownMessageType(Error):
    """Raised when a given message type is not available in constants.py"""

    def __init__(self):
        logger.error(
            "Unknow Used Message Type. Please refer to constants.py available constants.")
        super().__init__()


class NotASystemMessageType(Error):
    """Raised when a given message was not send from the system"""

    def __init__(self):
        logger.warning("Message was not sent from system.")
        super().__init__()


class MessageReadError(Error):
    """Raised when it is not possible read a message"""

    def __init__(self):
        logger.error("Unable to read message content.")
        super().__init__()


class MessageDatetimeReadError(Error):
    """Raised when datetime data cannot be extracted from message"""

    def __init__(self):
        logger.error(
            "wppMessage does not contain datetime information. Maybe a multiline msg?")
        super().__init__()


class UnexpectedContentSize(Error):
    """Raised when a content size is expected but was attended"""

    def __init__(self):
        logger.error("The content size was not expected.")
        super().__init__()
