import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = 'sqlite:///sochi_athletes.sqlite3'
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.INTEGER, primary_key=True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.TEXT)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def save_user_to_db(user, session):
    session.add(user)
    session.commit()

if __name__ == '__main__':
    session = connect_db()
    first_name = input('Please, input user name: ')
    last_name = input('Please, input user surname: ')
    gender = input('Please, input user gender: ')
    email = input('Please, input user email: ')
    birthdate = input('Please, input birthdate: ')
    user = User(first_name=first_name,
                last_name=last_name,
                gender=gender,
                email=email,
                birthdate=birthdate)
    save_user_to_db(user, session)
