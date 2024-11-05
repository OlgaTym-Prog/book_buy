import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

# Базовый класс для таблиц
Base = declarative_base()


# Модели данных
class Publisher(Base):
    __tablename__ = 'publisher'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)

    books = relationship("Book", back_populates="publisher")


class Book(Base):
    __tablename__ = 'book'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=50), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship('Publisher', back_populates="books")
    stock = relationship('Stock', back_populates="book")


class Stock(Base):
    __tablename__ = 'stock'
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship('Book', back_populates="stock")
    shop = relationship('Shop', back_populates="stock")
    sales = relationship('Sale', back_populates="stock")


class Sale(Base):
    __tablename__ = 'sale'
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship('Stock', back_populates="sales")


class Shop(Base):
    __tablename__ = 'shop'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)

    stock = relationship('Stock', back_populates="shop")


# Функция для создания таблиц
def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
