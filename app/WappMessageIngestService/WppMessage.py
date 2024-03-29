import os
import re

import unicodedata
from sqlalchemy import exc
from datetime import datetime
from typing import Union, List

import app.WappMessageIngestService.MessageService as Messages
from app.WappMessageIngestService.WppMessageDto import WppMessageDto
from app.ConfigService.Config import config

from .Exceptions import *
from .Constants import *


def is_valid(message_raw: str) -> Union[str, None]:
    '''Verify if given string is a valid whatsapp message. A message is valid if it contains datetime data at the start of the message'''
    
    regular_exp = re.compile(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2} -.*')

    datetime_content = re.match(regular_exp, message_raw)
    return datetime_content.group(0) if datetime_content else None


class WppMessage:
    '''Creates a Message Object from a line of whatsapp exported text file.'''
    __message: WppMessageDto
    __is_info_message: bool
    __content_tmp: str

    def __init__(self, raw_message: str):
        self.__message = WppMessageDto()
        self.__message.set_raw(raw_message)
        self.__extract_datetime()
        self.__extract_message_data()

    def __extract_datetime(self):
        '''Extracts datetime data from stored raw message'''

        raw = self.__message.get_raw()
        datetime_content = is_valid(raw)

        if datetime_content:
            datetime_content = datetime_content.split('-')[0]

            if len(datetime_content) == 17:  # size of a datetime string dd/mm/yyyy hh:MM
                # remove '-' and spaces in message string
                sanitized_content = datetime_content.strip()

                # create datetime class with given value
                datetime_content = datetime.strptime(
                    sanitized_content, "%d/%m/%Y %H:%M")

                # store in message DTO
                self.__message.set_datetime(datetime_content)
                return
            else:
                raise MessageDatetimeReadError
        else:
            raise MessageDatetimeReadError

    def __extract_message_data(self):
        '''Extract message from raw message without date and author.'''
        raw = self.__message.get_raw()
        message_content = re.search(r"-.*", raw)

        if message_content:
            # remove '-' and spaces in content string
            sanitized_message_content = message_content.group(
                0).replace('-', '').strip()
            sender = re.match(r"(.*?):", sanitized_message_content)
            message = re.search(r":.*", sanitized_message_content)

            if sender:
                sender = self.__sender_formater(sender.group(0)[:-1])
                message = message.group(0)[1:].strip()  # type: ignore

                # continue normally
                self.__message.set_author(sender)
                self.__message.set_content([message])
                self.__message.set_type(DEFAULT_TYPE)
                return
            else:
                self.__is_info_message = True
                self.__content_tmp = sanitized_message_content
                self.__message.set_author(SYSTEM_AUTHOR_NAME)
                self.__extract_message_type()
                return
        else:
            raise MessageReadError

    def __sender_formater(self, sender):
        '''Remove aditional spaces and unicodes from message sender.'''
        sender_str = re.sub(' +', ' ', sender)
        sender_str = sender.strip().replace('  ', ' ')
        sender_str = ''.join(
            c for c in sender_str if unicodedata.category(c)[0] != 'C')

        sender_str = sender_str.encode("utf8", "ignore")

        return sender_str.decode()

    def __extract_message_type(self):
        '''Sets the message type that are generated by whatsapp. I.e a notification that a member was added to a group. '''

        if self.__verify_member_add_msg() or self.__verify_member_mapping() or self.__verify_member_left_msg() or self.__verify_member_removed_msg():

            return  # operation ended
        else:
            self.__message.set_author(SYSTEM_AUTHOR_NAME)
            self.__message.set_content([self.__content_tmp])
            self.__message.set_type(OTHER_MSG_TYPE)
            return

    def __verify_member_add_msg(self) -> bool:
        '''Verify if message is a user was added whatsapp notification.'''

        if self.__is_info_message:
            content = self.__content_tmp
            message_add = re.search(r".*adicionou", content)

            if message_add:
                """then maybe we have a valid member_add message"""
                message_add = content.split("adicionou")
                members_added_comma_separated = message_add[1].split(',')
                members_added_article_separated = message_add[1].split(' e ')

                if (len(members_added_comma_separated) >= 2) | (len(members_added_article_separated) >= 2):
                    members_added_comma_separated = [
                        x.split(' e ') for x in members_added_comma_separated]
                    members_added_comma_separated = [
                        item for sublist in members_added_comma_separated for item in sublist]

                sender = self.__sender_formater(message_add[0])

                members_added_comma_separated = [
                    x.strip() for x in members_added_comma_separated]

                self.__message.set_author(sender)
                self.__message.set_content(members_added_comma_separated)
                self.__message.set_type(MEMBER_ADDED_TYPE)
                return True
            else:
                return False

        else:
            logger.warning("Only use this method on informative message.")
            raise NotASystemMessageType

    def __verify_member_mapping(self) -> bool:
        '''Verify if message is a whatsapp notification of a user changing the phone number.'''

        if self.__is_info_message:
            content = self.__content_tmp
            msg_mapping = re.search(".*mudou para", content)

            if msg_mapping:
                msg_mapping = msg_mapping.group(0).split("mudou para")

                if len(msg_mapping) > 2:
                    logger.error("This might be an bug. Message may contain 'mudou para' multiple times,"
                                 "causing a unknown message state")
                    raise UnexpectedContentSize
                else:
                    self.__message.set_author(msg_mapping[0])
                    self.__message.set_content([msg_mapping[1]])
                    self.__message.set_type(MEMBER_ID_MAPPING_TYPE)
                    return True
            else:
                """message is not of type member_mapping"""
                return False
        else:
            logger.warning("Only use this method on informative message.")
            raise NotASystemMessageType

    def __verify_member_left_msg(self) -> bool:
        '''Verify if message is a whatsapp notification of a user that has left a group.'''

        if self.__is_info_message:
            content = self.__content_tmp
            left_message = re.search(r".*saiu", content)

            if left_message:
                left_message = left_message.group(0).split("saiu")

                if len(left_message) > 2:
                    logger.error("This might be an bug. Message may contain 'saiu' as a sender name, causing a "
                                 "unknown sender number or name")
                    raise UnexpectedContentSize
                else:
                    """ may be a message of type member_left"""
                    self.__message.set_type(MEMBER_LEFT_TYPE)
                    self.__message.set_content([])
                    self.__message.set_author(
                        self.__sender_formater(left_message[0]))
                    return True
            else:
                """message is not of type member_left"""
                return False
        else:
            # Exception("Message is not a system information. Only use this method on informative message.")
            raise NotASystemMessageType

    def __verify_member_removed_msg(self) -> bool:
        '''Verify if message is a whatstapp notification of a user that was removed from a group.'''

        if self.__is_info_message:
            content = self.__content_tmp
            msg_removed = re.search(r".*removeu", content)

            if msg_removed:
                """then maybe we have a valid member_removed message"""
                msg_removed = content.split("removeu")

                sender = self.__sender_formater(msg_removed[0])
                receiver = self.__sender_formater(msg_removed[1])

                self.__message.set_author(sender)
                self.__message.set_content(msg_removed[1])
                self.__message.set_type(MEMBER_REMOVED_TYPE)
                return True
            else:
                return False

        else:
            logger.warning("Only use this method on informative message.")
            raise NotASystemMessageType

    def get_message(self):
        '''Returns the stored message'''
        return self.__message


def read_dataset_file(dataset: str):
    '''Read a file containing the dump of whatsapp group messages, and processes it.'''
    treated_dataset = []
    dataset = os.path.join(config.project_workdir, dataset)  # type: ignore

    with open(dataset, "r", encoding='utf8') as dataset_file:
        dataset_lines = dataset_file.readlines()
        logger.info(
            f'Reading {len(dataset_lines)}. This might take a while. Coffee-break ☕?')
        # ingest from dataset file and pushes to db
        for line in dataset_lines:
            if is_valid(line):
                line_to_object = WppMessage(line)
                object_dto = line_to_object.get_message()
                treated_dataset.append(object_dto)
            else:
                # concatenate line to the rest of message
                # update message content
                last_message_content = treated_dataset[-1].get_content()[0]
                # update raw message
                last_message_raw = treated_dataset[-1].get_raw()
                line_glue = '' if line == '\n' else '\n'
                treated_dataset[-1].set_content(
                    [last_message_content + line_glue + line])
                treated_dataset[-1].set_raw(last_message_raw +
                                            line_glue + line)

    return treated_dataset


def load_database_with_dataset(data: List[WppMessageDto], start_at=0):
    '''Store all available messages from a whatsapp group messages dump in database.'''
    data_size = len(data)
    item_track = start_at
    next_checkpoint = config.chunk_size  # type: ignore
    persisted = False

    # verify if table is already in use to prevent overwrites.
    if Messages.index():
        logger.error("Table already in use")
        return

    # Set the start point
    if (start_at < data_size) and (start_at >= 0):
        sub_list = data[start_at:]

        for item in sub_list:
            persisted = False

            try:
                Messages.create(item, auto_persist=False)

                if item_track == next_checkpoint:
                    # update checkpoint
                    next_checkpoint += config.chunk_size  # type: ignore
                    Messages.persist()
                    persisted = True
                    logger.info(
                        f"Checkpoint: {item_track} of {data_size} items persisted.")

            except exc.IntegrityError:
                Messages.rollback()
                logger.error(
                    f"Persistence process failed at item {item_track}")
                return item_track  # break with item position to resume

            item_track += 1

        if not persisted:
            Messages.persist()

    logger.info(f'Persistence process done. {item_track} items processed.')
