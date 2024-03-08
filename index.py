from dotenv import load_dotenv
from flask import Flask
from connectors.mysql_connector import engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from models.product import Product
from sqlalchemy import select

from flask_login import LoginManager
from models.user import User
import os

# Load Controller Files
from controllers.product import product_routes
from controllers.user import user_routes

load_dotenv()

app=Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    return session.query(User).get(int(user_id))

app.register_blueprint(product_routes)
app.register_blueprint(user_routes)

# Product Route
@app.route("/")
def hello_world():
    # Insert a Product Object

    ## SQL Way
    # Session = sessionmaker(connection)
    # with Session() as session:
    #     session.execute(text("INSERT INTO product (name, price, description) VALUES ('Steel Wallet', 145000, 'Created from synthetic steel. Water-proof.')"))
    #     session.commit()

    ## ORM Way
    ### Create Product Object First
    # NewProduct = Product( name='Plastic Wallet', price=12000, description='Made from recyled plastic bags' )
    # Session = sessionmaker(connection)
    # with Session() as session:
    #     session.add(NewProduct)
    #     session.commit()

    # Fetch all Products
    product_query = select(Product)
    Session = sessionmaker(connection)
    with Session() as session:
        result = session.execute(product_query)
        for row in result.scalars():
            print(f'ID: {row.id}, Name: {row.name}')

    return "<p>Insert Success</p>"