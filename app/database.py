import os
from sqlalchemy import create_engine, Column, String, Integer, Text, ForeignKey, Date, Float
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine

Session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if os.path.exists("travel_agency.db"):
    os.remove("travel_agency.db")

engine = create_engine("sqlite:///travel_agency.db", echo=True)


class Base(DeclarativeBase):
    pass


class Clients(Base):
    """Клиент"""
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String(50))
    email = Column(String(100))
    phone = Column(String(15))


class Guides(Base):
    """Гид"""
    __tablename__ = 'guide'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String(50))
    specialization = Column(String(100))
    phone = Column(String(15))


class Tours(Base):
    """Тур"""
    __tablename__ = 'tour'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(100))
    description = Column(Text)
    price = Column(Float)
    count_place = Column(Integer)
    guide_id = Column(Integer, ForeignKey('guide.id'))
    transport_id = Column(Integer, ForeignKey('transport.id'))

    guide = relationship('Guides', backref='tour_guide', lazy='subquery')


class Reservations(Base):
    """Бронирование"""
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    date_reservation = Column(Date)
    quantity_people = Column(Integer)
    status = Column(String(50))
    client_id = Column(Integer, ForeignKey('client.id'))
    tour_id = Column(Integer, ForeignKey('tour.id'))

    client = relationship('Clients', backref='reservation_client', lazy='subquery')
    tour = relationship('Tours', backref='reservation_tour', lazy='subquery')


class Hotels(Base):
    """Отель"""
    __tablename__ = 'hotel'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(100))
    address = Column(String(200))
    price = Column(Float)
    rating = Column(Float)


class Transports(Base):
    """Транспорт"""
    __tablename__ = 'transport'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    type = Column(String(50))
    company = Column(String(100))
    price = Column(Float)


class Payments(Base):
    """Оплата"""
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    summa = Column(Float)
    method_payment = Column(String(50))
    reservation_id = Column(Integer, ForeignKey('reservation.id'))

    reservation = relationship('Reservations', backref='payment_reservation', lazy='subquery')


class Reviews(Base):
    """Отзыв"""
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    appraisal = Column(Float)   # Оценка
    comment = Column(Text)
    client_id = Column(Integer, ForeignKey('client.id'))
    tour_id = Column(Integer, ForeignKey('tour.id'))

    client = relationship('Clients', backref='review_client', lazy='subquery')
    tour = relationship('Tours', backref='review_tour', lazy='subquery')


class SpecialPackages(Base):
    """Специальное предложение"""
    __tablename__ = 'specialpackage'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(50))
    description = Column(Text)
    price = Column(Float)
    tour_id = Column(Integer, ForeignKey('tour.id'))

    tour = relationship('Tours', backref='specialpackage_tour', lazy='subquery')


class ServicePackages(Base):
    """Пакет услуг"""
    __tablename__ = 'servicepackage'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(100))
    description = Column(Text)
    price = Column(Float)
    tour_id = Column(Integer, ForeignKey('tour.id'))

    tour = relationship('Tours', backref='servicepackage_tour', lazy='subquery')


class TourHotel(Base):
    """Промежуточная таблица для связи Туров и Отелей"""
    __tablename__ = 'tourhotel'

    tour_id = Column(Integer, ForeignKey('tour.id'), primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotel.id'), primary_key=True)

    tour = relationship("Tour", back_populates="tourhotel_tour")
    hotel = relationship("Hotel", back_populates="tourhotel_tour")


def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()


# Создание всех таблиц в базе данных
Base.metadata.create_all(engine)