import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import random
import datetime

DB_PATH = 'sqlite:///sochi_athletes.sqlite3'
Base = declarative_base()

class Athlete(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    weight = sa.Column(sa.Integer)
    name = sa.Column(sa.Text)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find_random_athlete(athletes_data, athlete_id):
    random_athlete = random.choice(athletes_data)
    while random_athlete.id == athlete_id.id or random_athlete.height is None:
        random_athlete = random.choice(athletes_data)
    return random_athlete

def find_nearest_athlete_height(athletes_data, athlete_id, nearest_athlete):    
    height_delta = abs(nearest_athlete.height * 100 - athlete_id.height * 100)
    for athlete in athletes_data:
        if athlete.id != athlete_id.id and athlete.height is not None:
           delta = abs(athlete.height * 100 - athlete_id.height * 100)
           if delta < height_delta:
               height_delta = delta
               nearest_athlete = athlete
    return nearest_athlete

def define_local_date(athlete_birthdate):
    year, month, day = athlete_birthdate.split('-')
    if month[0] == '0':
        month = int(month[1])
    else:
        month = int(month)
    if day[0] == '0':
        day = int(day[1])
    else:
        day = int(day)
    year = int(year)
    
    local_date = datetime.datetime(year=year, month=month, day=day)
    return local_date

def find_nearest_athlete_birthdate(athletes_data, athlete_id, nearest_athlete):
    athlete_id_birthdate = define_local_date(athlete_id.birthdate)
    nearest_athlete_birthdate = define_local_date(nearest_athlete.birthdate)
    time_delta = abs(athlete_id_birthdate - nearest_athlete_birthdate)
    for athlete in athletes_data:
        if athlete.id != athlete_id.id:
            nearest_athlete_birthdate = define_local_date(athlete.birthdate)
            delta = abs(athlete_id_birthdate - nearest_athlete_birthdate)
            if delta < time_delta:
                time_delta = delta
                nearest_athlete = athlete
    return nearest_athlete


if __name__ == '__main__':
    session = connect_db()
    user_id = int(input('Please, input athlete id:'))
    session = connect_db()
    athlete_id = session.query(Athlete).filter(Athlete.id == user_id).first()
    print(f'You have chosen athlet id:{athlete_id.id}, name:{athlete_id.name}, height:{athlete_id.height}, birthdate:{athlete_id.birthdate}')
    if athlete_id and athlete_id.height is not None:
        athletes_data = session.query(Athlete).all()
        nearest_athlete = find_random_athlete(athletes_data, athlete_id)
        nearest_athlete_height = find_nearest_athlete_height(athletes_data, athlete_id, nearest_athlete)
        nearest_athlete_birthdate = find_nearest_athlete_birthdate(athletes_data, athlete_id, nearest_athlete)
        print(f'Nearest athlete in height id:{nearest_athlete_height.id}, name:{nearest_athlete_height.name}, height:{nearest_athlete_height.height}')
        print(f'Nearest athlete in birthdate id:{nearest_athlete_birthdate.id}, name:{nearest_athlete_birthdate.name}, birthdate:{nearest_athlete_birthdate.birthdate}')
    else:
        print("There's no such athlete id in database!")
