from flask import Flask
from dotenv import load_dotenv
from connectors.mysql_connector import connection
from sqlalchemy import text
from models.product import Product
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

@app.route('/')
def hello_world():
    
    # Session = sessionmaker(connection)
    # with Session() as s:
    #     s.execute(text("INSERT INTO product (name, price, description, created_at) VALUES ('Wallet', 15000, 'Create from cow skin','2024-02-01 00:00:00')"))
    #     s.commit()

    NewProduct = Product(name='Snake Wallet', price=3000, description='Created from Snake Skin', created_at='2024-02-01 00:00:00')
    Session = sessionmaker(connection)
    with Session() as s:
        s.add(NewProduct)
        s.commit()

    return 'Hello, World!'