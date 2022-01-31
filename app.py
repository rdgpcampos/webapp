#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 07:38:11 2022

@author: rodrigocampos
"""

import flask
from flask_restful import Resource, Api
from error_handler import InvalidRequest, CancelledOrder
from database_objects import connect_to_db
import app_header

app = flask.Flask(__name__)
clubbi_api = Api(app)
Session = connect_to_db()

@app.before_request
def before_request():
    flask.g.session = Session()

@app.teardown_request
def close_db_session(exception):
    try:
        flask.g.session.commit()
    except:
        flask.g.session.rollback()
    finally:
        flask.g.session.close()    

class OrderRequests(Resource):
    # get all items and total price of an order\
    def get(self):
        
        # parse input
        parameters = app_header.set_params('orderId')
        
        # first message in output
        header = 'Following products are present in order'
        
        # get id, description and unit price (at time of purchase)
        # of products from a given order_id
        try:
            order = app_header.get_order(flask.g.session,parameters[0],header)
        except InvalidRequest as e:
            return {str(e) : None}, 404
        except CancelledOrder as e:
            return {str(e) : None}, 404

        output = app_header.organize_order(order,header)

        # output items and total price of order
        return output, 200
        
    # add new order
    def post(self):
        
        # parse input
        parameters = app_header.set_params('clientId','productlist')
        
        # default status
        status = 'Released'

        # first message in output
        header = 'Following products were added to order'

        # update orders table
        try:
            order = app_header.post_order(flask.g.session,parameters[0],
                       parameters[1],status,header)
        except InvalidRequest as e:
            return {str(e) : None}, 404

        output = app_header.organize_order(order,header)

        # output items and total price of order
        return output, 200
    
    # modify an order
    def put(self):
        
        # parse input
        parameters = app_header.set_params('orderId','productId','addflag')
        
        # first message in output
        header = 'Order was modified to'
        
        # get id, description and unit price (at time of purchase)
        # of products from a given order_id
        try:
            order = app_header.put_order(flask.g.session,
                          parameters[0],
                          parameters[1],
                          parameters[2],
                          header)
        except InvalidRequest as e:
            return {str(e) : None}, 404
        except CancelledOrder as e:
            return {str(e) : None}, 404

        output = app_header.organize_order(order,header)

        return output, 200
    
    # cancel an order
    def delete(self):
        
        # parse input
        parameters = app_header.set_params('orderId')
        
        # first message in output
        header = 'Order deleted'
        
        # delete order (i.e. change status to cancelled, 
        # return all products to stock, delete elements in join table)
        try:
            # delete order
            output = app_header.delete_order(flask.g.session,
                                             parameters[0],
                                             header)
        except InvalidRequest as e:
            return {str(e) : None}, 404
        except CancelledOrder as e:
            return {str(e) : None}, 404
        
        return output, 200

clubbi_api.add_resource(OrderRequests, '/orders',endpoint="orders")

class ItemRequests(Resource):
    def put(self):
        
        # parse input
        parameters = app_header.set_params('productId','unitPrice')
        
        # first message in output
        header = 'Product price updated'
        
        try:
            # update
            output = app_header.\
                put_product(flask.g.session,
                            parameters[0],
                            parameters[1],
                            header)
        except InvalidRequest as e:
            return {str(e) : None}, 404
        
        return output, 200
        
clubbi_api.add_resource(ItemRequests,'/items',endpoint='items')    

if __name__ == "__main__":
    app.run(debug=True)