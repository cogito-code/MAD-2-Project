from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import auth_token_required

from database import db
from models import Products


class ProductResource(Resource):
    #/api/product/<int: product_id>  :GET

    def get(self, product_id):
        #Read operation
        product = Products.query.get(product_id)

        if not product:
            return make_response(
                jsonify({'message': 'Product not found.'}),
                404
            )
        
        result = {
            "message": "Product retrieved successfully.",
            "product" : {
                'id': product.id,
                'name': product.name,
                'description': product.description, 
                'price': product.price,
                'stock': product.stock
            }
        }

        return make_response(
            jsonify(result),
            200
        )
    
    #/api/product  :Post
    def post(self):
        prod_cred = request.get_json()

        if not prod_cred or not prod_cred.get('name') or not prod_cred.get('price') or not prod_cred.get('stock'):
            return make_response(
                jsonify({'message': 'Product name, stock and price are required.'}),
                400
            )
        
        name = prod_cred['name']
        price = prod_cred['price']
        description = prod_cred.get('description', '')
        stock = prod_cred.get('stock', 0)

        # Data validation
        if Products.query.filter_by(name=name).first():
            return make_response(
                jsonify({'message': 'Product with this name already exists.'}),
                400
            )
        
        new_product = Products(
            name=name,
            description=description,
            price=price,
            stock=stock
        )  

        db.session.add(new_product)
        db.session.commit()

        result = {
            "message": "Product created successfully.",
            "product": {
                'id': new_product.id,
                'name': new_product.name,
                'description': new_product.description,
                'price': new_product.price,
                'stock': new_product.stock
            }
        }

        return make_response(
            jsonify(result),
            201
        )

    #/api/product/<int: product_id>  :PUT
    def put(self, product_id):
        product =  Products.query.get(product_id)
        if not product:
            return make_response(
                jsonify({'message': 'Product not found.'}),
                404
            )
        
        prod_cred = request.get_json()
        if not prod_cred or not prod_cred.get('name') or not prod_cred.get('price') or not prod_cred.get('stock'):
            return make_response(
                jsonify({'message': 'Product name, stock and price are required.'}),
                400
            )
        
        name = prod_cred['name']
        price = prod_cred['price']
        description = prod_cred.get('description', '')
        stock = prod_cred.get('stock', 0)

        new_product = Products.query.filter_by(name=name).first()
        if new_product and new_product.id != product_id:
            return make_response(
                jsonify({'message': 'Product with this name already exists.'}),
                400
            )
        
        product.name = name
        product.description = description
        product.price = price
        product.stock = stock


        db.session.commit()
        result = {
            "message": "Product updated successfully.",
            "product": {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'stock': product.stock
            }
        }   

        return make_response(
            jsonify(result),
            200
        )
    
    #/api/product/<int: product_id>  :DELETE
    def delete(self, product_id):
        product = Products.query.get(product_id)
        if not product:
            return make_response(
                jsonify({'message': 'Product not found.'}),
                404
            )
        
        db.session.delete(product)
        db.session.commit()

        return make_response(
            jsonify({'message': 'Product deleted successfully.'}),
            200
        )


