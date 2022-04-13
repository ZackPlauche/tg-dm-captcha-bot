from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import create_engine, Integer, Column, String, DateTime, select
from sqlalchemy.orm import declarative_base, Session

from settings import MINUTES_UNTIL_KICK

db_location = Path(__file__).resolve().parent.parent / 'db.sqlite3'
db_type = 'sqlite'
engine = create_engine(f'{db_type}:///{db_location}', echo=True, future=True)

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    status = Column(Integer, nullable=False)

    def __repr__(self):
        return f'User(id={repr(self.id)}, chat_id={repr(self.chat_id)}, timestamp={repr(self.timestamp)}, name={repr(self.name)}, code={repr(self.code)}, status={repr(self.status)})'

    def is_invalid(self):  # -> bool
        seconds_joined = (datetime.now() - self.timestamp).seconds
        seconds_until_kick = timedelta(minutes=MINUTES_UNTIL_KICK).seconds
        return seconds_joined > seconds_until_kick and self.is_banned()

    def is_banned(self):  # -> bool
        return self.status == 0

Base.metadata.create_all(engine)


def add_user(user):  # user: User
    session = Session(engine)
    session.add(user)
    session.commit()
    session.close()

create_user = add_user


def get_user(chat_id):  # chat_id: int -> User
    session = Session(engine)
    user = session.scalars(select(User).filter_by(chat_id=chat_id)).first()
    session.close()
    return user


def get_all_users():  # -> list[User]
    session = Session(engine)
    users = session.scalars(select(User)).all()
    session.close()
    return users


def get_banned_users():  # -> list[User]
    session = Session(engine)
    users = session.scalars(select(User).filter_by(status=1)).all()
    session.close()
    return users


def update_user(user, **kwargs):  # user: User
    session = Session(engine)
    session.add(user)
    for key, value in kwargs.items():
        setattr(user, key, value)
    session.commit()
    session.close()