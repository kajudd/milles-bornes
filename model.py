import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

database_url = os.environ.get('DATABASE_URL', 'postgres://localhost/milles-bornes.db')
ENGINE = create_engine(database_url, echo=False)
session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = session.query_property()


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String(140), nullable=True)
    email = Column(String(140), nullable=True)
    password = Column(String(140), nullable=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    type = Column(String(64), nullable=True)
    action = Column(String(64), nullable=True)
    image = Column(String(500), nullable=True)


class Usergame(Base):
    __tablename__ = "user_game"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer(1000), ForeignKey('games.id'))
    user_id = Column(Integer(1000), ForeignKey('players.id'))
    position = Column(Integer(1))
    hand = Column(String(30), nullable=True)
    miles = Column(Integer(4), nullable=True)
    immunities = Column(Integer(4), nullable=True)
    #Vulnerabilities
    can_be_stopped = Column(Integer(1), nullable=True)
    can_have_flat = Column(Integer(1), nullable=True)
    can_have_low_gas = Column(Integer(1), nullable=True)
    can_have_speed_limit = Column(Integer(1), nullable=True)
    can_be_in_accident = Column(Integer(1), nullable=True)
    #Status
    speed_limit = Column(Integer(1), nullable=True)
    can_go = Column(Integer(1), nullable=True)
    has_flat = Column(Integer(1), nullable=True)
    has_accident = Column(Integer(1), nullable=True)
    gas_empty = Column(Integer(1), nullable=True)
    game_status = Column(Integer(1), nullable=True)

    #Method displays the action of a card in player hand.
    def cards_in_hand(self, player_hand):
        cards_in_hand = []
        for card in player_hand:
            int_card = int(card)
            card_info = session.query(Card).get(int_card)
            cards_in_hand.append(card_info)
        return cards_in_hand

    def check_status(usergame):
        if usergame.can_go == 1:
            status = "Going"
        elif usergame.has_flat == 1:
            status = "Flat Tire"
        elif usergame.has_accident == 1:
            status = "Accident"
        elif usergame.gas_empty == 1:
            status = "Gas Empty"
        else:
            status = "Stopped"
        return status

    def check_speed(usergame):
        if usergame.speed_limit == 0:
            limit = "None"
        else:
            limit = usergame.speed_limit
        return limit

    def check_immunities(usergame):
        current_immunities = []
        string = str(usergame.immunities)

        if string[0] == "3":
            current_immunities.append("Extra Tank")
        if string[1] == "3":
            current_immunities.append("Puncture Proof")
        if string[2] == "3":
            current_immunities.append("Driving Ace")
        if string[3] == "3":
            current_immunities.append("Right of Way")

        return current_immunities

    game = relationship("Game", backref=backref("games", order_by=id))
    player = relationship("Player", backref=backref("players", order_by=id))


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    draw_pile = Column(String(500), nullable=True)
