from datetime import datetime, timedelta

from sqlalchemy import create_engine, Integer, Column, String, DateTime, select
from sqlalchemy.orm import declarative_base, Session

from settings import MINUTES_UNTIL_KICK, DEBUG, GOOGLE_CLOUD_INFO

DB_URLS = {
    'sqlite': 'sqlite+pysqlite:///{path}',
    'google_cloud_sql_internal': 'mysql+mysqldb://root@/{dbname}?unix_socket=/cloudsql/{projectid}:{instancename}'.format(**GOOGLE_CLOUD_INFO),
    'google_cloud_sql_external': 'mysql+mysqldb://{user}:{password}@{host}:{port}/{dbname}'.format(**GOOGLE_CLOUD_INFO),
}

db_url = DB_URLS['google_cloud_sql_internal'] if not DEBUG else DB_URLS['google_cloud_sql_external']
engine = create_engine(db_url, echo=True, future=True)  # seconds

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)
    status = Column(Integer, nullable=False)

    def __repr__(self):
        return f'User(id={repr(self.id)}, chat_id={repr(self.chat_id)}, timestamp={repr(self.timestamp)}, name={repr(self.name)}, code={repr(self.code)}, status={repr(self.status)})'

    def is_invalid(self):  # -> bool
        seconds_joined = (datetime.now() - self.timestamp).seconds
        seconds_until_kick = timedelta(minutes=MINUTES_UNTIL_KICK).seconds
        return seconds_joined > seconds_until_kick and self.is_new()

    def is_new(self):  # -> bool
        return self.status == 0

    def is_verified(self):
        return self.status == 1

    def has_error(self):
        return self.status == 2

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


def get_verified_users():  # -> list[User]
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


if __name__ == '__main__':
    ...