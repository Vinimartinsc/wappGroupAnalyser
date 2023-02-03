from app.DatabaseService.Models import Messages
from app.DatabaseService.Database import session

from .WppMessageDto import WppMessageDto


def index():
    '''Get all messages in database.'''
    return session.query(Messages).all()


def create(message: WppMessageDto, auto_persist=True):
    '''Store a new message in database.'''
    new_message = Messages(
        at_datetime=message.get_datetime(),
        author=message.get_author(),
        raw=message.get_raw(),
        type=message.get_type(),
        content=','.join(message.get_content())
    )

    session.add(new_message)

    if auto_persist:
        session.commit()


def read(identifier: int):
    '''Read a message with given id.'''
    return session.query(Messages).get(identifier)


def persist():
    '''Commit all session changes.'''
    session.commit()


def rollback(flush=True):
    '''Rollback all session changes.'''
    if flush:
        session.flush()

    session.rollback()
    session.close()
