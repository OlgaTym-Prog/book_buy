import os
import json
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

# Загрузка переменных окружения
load_dotenv()

DB_USER = os.getenv("DB_USER", "default_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "default_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "default_db")

# Подключение к базе данных
DSN = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Загрузка данных из JSON
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Добавление данных в таблицы
for item in data:
    if item["model"] == "publisher":
        publisher = Publisher(**item["fields"])
        session.add(publisher)

    if item["model"] == "shop":
        shop = Shop(**item["fields"])
        session.add(shop)

    if item["model"] == "book":
        book = Book(**item["fields"])
        session.add(book)

    if item["model"] == "stock":
        stock = Stock(**item["fields"])
        session.add(stock)

    if item["model"] == "sale":
        sale = Sale(**item["fields"])
        session.add(sale)

session.commit()
session.close()


# Функция для получения продаж по издателю
def get_publisher_sales(publisher_name_or_id: str):
    # Проверка, что введено имя или ID издателя
    query = session.query(Sale).join(Sale.stock).join(Stock.book).join(Book.publisher).join(Stock.shop)

    if publisher_name_or_id.isdigit():
        query = query.filter(Publisher.id == int(publisher_name_or_id))
    else:
        query = query.filter(Publisher.name == publisher_name_or_id)

    # Получение данных и вывод
    sales = query.all()
    if not sales:
        print("Нет данных для указанного издателя.")
        return

    for sale in sales:
        print(f"{sale.stock.book.title} | {sale.stock.shop.name} | {sale.price} | {sale.date_sale.strftime('%d.%m.%Y')}")

    session.close()


if __name__ == "__main__":
    publisher_name_or_id = input("Введите ID или имя издателя: ")
    get_publisher_sales(publisher_name_or_id)
