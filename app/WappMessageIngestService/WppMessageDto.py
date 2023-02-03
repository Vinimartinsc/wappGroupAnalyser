from datetime import datetime
from typing import List
from app.WappMessageIngestService.Constants import MESSAGE_TYPES
from app.WappMessageIngestService.Exceptions import *


class WppMessageDto:
    '''A object that represents a whatsapp message'''
    __at_datetime: datetime
    __author: str
    __content: List[str]
    __raw: str
    __type: str

    def __init__(self):
        pass

    def set_datetime(self, msg_datetime: datetime):
        '''Set the datetime a message was sent.'''
        self.__at_datetime = msg_datetime

    def get_datetime(self) -> datetime:
        '''Get the datetime a message was sent.'''
        return self.__at_datetime

    def set_author(self, author: str):
        '''Set the message author - can be a name or a phone number.'''
        self.__author = author

    def get_author(self) -> str:
        '''Get a message author.'''
        return self.__author

    def set_content(self, content: List[str]):
        '''Set a message content'''
        self.__content = content

    def get_content(self) -> List[str]:
        '''Get the message content.'''
        return self.__content

    def set_raw(self, raw_message: str):
        '''Set a message as it is available in dataset text file.'''
        self.__raw = raw_message

    def get_raw(self) -> str:
        '''Get message as available in dataset text file.'''
        return self.__raw

    def get_type(self) -> str:
        '''Get the message category type. For example, if it is a a user adition operation or a plain message.'''
        return self.__type

    def set_type(self, message_type: str):
        '''Set a message type from MESSAGE_TYPES constant.'''
        if message_type in MESSAGE_TYPES:
            self.__type = message_type
        else:
            # Exception("Unknown Used Message Type. Please refer to constants.py available constants.")
            raise UnknownMessageType
