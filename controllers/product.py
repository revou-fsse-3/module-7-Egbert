from flask import Blueprint, render_template, request,jsonify
from connectors.mysql_connector import engine
from models.product import Product
from sqlalchemy import select, or_
from sqlalchemy.orm import sessionmaker
from flask_login import current_user, login_required
from decorators.role_checker import role_required
from validations.product_schema import product_schema
from cerberus import Validator

product_routes = Blueprint('product_routes',__name__)

@product_routes.route("/product", methods=['GET'])
@login_required
def product_home():
    response_data = dict()

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        product_query = select(Product)

        if request.args.get('query') != None:
            search_query = request.args.get('query')
            product_query = product_query.where(or_(Product.name.like(f"%{search_query}%"), Product.description.like(f"%{search_query}%")))

        products = session.execute(product_query)
        products = products.scalars()
        response_data['products'] = products
        response_data['name'] = current_user.name
    except Exception as e:
        print(e)
        return "Error Processing Data"

    return render_template("products/product_home.html", response_data = response_data)

@product_routes.route("/product/<id>", methods=['GET'])
def product_detail(id):
    response_data = dict()

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        product = session.query(Product).filter((Product.id==id)).first()
        if (product == None):
            return "Data not found"
        response_data['product'] = product
    except Exception as e:
        print(e)
        return "Error Processing Data"

    return render_template("products/product_detail.html", response_data = response_data)

@product_routes.route("/product", methods=['POST'])
@role_required('Admin')
def product_insert():

    v = Validator(product_schema)
    json_data = request.get_json()
    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400
    
    new_product = Product(
        name=json_data['name'],
        price=json_data['price'],
        description=json_data['description']
    )

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()
    try:
        session.add(new_product)
        session.commit()
    except Exception as e:
        session.rollback()
        return { "message": "Fail to insert data"}

    return { "message": "Success insert data"}

@product_routes.route("/product/<id>", methods=['DELETE'])
def product_delete(id):

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()

    try:
        product = session.query(Product).filter(Product.id==id).first()
        session.delete(product)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
        return { "message": "Fail to delete data"}
    
    return { "message": "Success delete data"}

@product_routes.route("/product/<id>", methods=['PUT'])
def product_update(id):

    v = Validator(product_schema)
    json_data = request.get_json()
    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()

    try:
        product = session.query(Product).filter(Product.id==id).first()

        product.name = json_data['name']
        product.price = json_data['price']
        product.description = json_data['description']

        session.commit()
    except Exception as e:
        session.rollback()
        return { "message": "Fail to Update data"}
    
    return { "message": "Success updating data"}



