#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import psycopg2
from flask_restful import reqparse
from database_objects import OrderTable, ProductTable, JoinTable,\
insert_joint, insert_order, make_into_order
from error_handler import InvalidRequest, if_valid, if_available

# function to read parameters
def set_params(*args):
    
    parser = reqparse.RequestParser()
    
    # check which arguments are present
    if 'orderId' in args:
        parser.add_argument('orderId', required=True, type=int)
        
    if 'clientId' in args:
        parser.add_argument('clientId', required=True, type=int)
    
    if 'productId' in args:
        parser.add_argument('productId', required=True, type=int)
    
    if 'productlist' in args:
        parser.add_argument('productId', required=True, type=int, 
                            action='append')
    
    if 'status' in args:
        parser.add_argument('status', required=False, default = 'Released',
                            type=str)
    
    if 'addflag' in args:
        parser.add_argument('addflag', required=False, choices=['True', 'False'],
        default = 'True', type=str)
    
    if 'unitPrice' in args:
        parser.add_argument('unitPrice', required=True, type=float)
    
    dict_param = parser.parse_args()
    list_param = []
    for v in dict_param.values():
        list_param.append(v)
    
    return list_param

# organize output of get query
def organize_order(order, header: str):
    
    pre_output = {}
    
    for i, product in enumerate(order.product_list, start=1):
        pre_output['Product {}'.format(i)] = product
    
    output = { header : pre_output }
    output['Total price'] = order.total_price
    
    return output

def get_order(session,order_id,header: str,check_if_valid=True):
    
    # check validity of order
    if check_if_valid:
        if_valid(session,order_id)
    
    # select all products with a given order_id
    q = session.query(ProductTable.product_id,
                      ProductTable.description,
                      JoinTable.unit_price).\
                join(ProductTable).\
                filter(JoinTable.order_id == order_id).all()
    
    order = make_into_order(q,order_id)
        
    return order

def post_order(session,client_id,product_list,status,header: str):
    
    # insert new order
    order_id = insert_order(session,client_id,status)

    cnt = 0
    
    for product_id in product_list:
        
        try:
            available,cur_price = if_available(session,product_id)
        except InvalidRequest:
            cnt += 1
            continue
            
        # update join table with new order id, product id, and current unit price
        insert_joint(session,order_id,product_id,cur_price)
        
        # update product stock (-1)
        session.query(ProductTable).\
                        filter(ProductTable.product_id == product_id).\
                        update({ProductTable.stock: ProductTable.stock -1})
                        
    if cnt == len(product_list):
        raise InvalidRequest("No products available")
            
    return get_order(session,order_id,header,False)

def put_order(session,order_id,product_id,addflag,header: str):
    
    # check validity of order
    if_valid(session, order_id)

    if addflag == 'True':
        change = -1
        add_product_to_order(session, order_id, product_id)
        
    else:
        change = 1
        remove_product_from_order(session, order_id, product_id)  

    # update product stock (+change)
    session.query(ProductTable).\
                    filter(ProductTable.product_id == product_id).\
                    update({ProductTable.stock: ProductTable.stock +change})
        
    return get_order(session,order_id,header,False)

def add_product_to_order(session,order_id,product_id):
    
    # check if product is available
    available,cur_price = if_available(session, product_id)
    
    # update join table with new order id, product id, and current unit price
    insert_joint(session,order_id,product_id,cur_price)

def remove_product_from_order(session,order_id,product_id):
    
    # delete one of the products in the join table that match parameters
    f = session.query(JoinTable).\
        filter(JoinTable.order_id == order_id,
               JoinTable.product_id == product_id).first()
    # exception if this product is not in this order
    if f is None:
        raise InvalidRequest("This product is not available in this order")
        
    session.delete(f)

def delete_order(session,order_id,header: str):
    
    # check validity of order
    if_valid(session, order_id)
    
    # add products back in stock
    q = session.query(JoinTable.product_id).filter(JoinTable.order_id == order_id)
    for row in q:
        session.query(ProductTable).filter(ProductTable.product_id == row[0]).\
            update({ProductTable.stock: ProductTable.stock +1})
    
    # delete elements corresponding to this order from join table
    session.query(JoinTable).filter(JoinTable.order_id == order_id).\
                            delete(synchronize_session=False)
    
    # change status of order to 'Cancelled'
    session.query(OrderTable).\
                    filter(OrderTable.order_id == order_id).\
                    update({OrderTable.status: 'Cancelled'})
    
    return { header : None }

def put_product(session,product_id,unit_price,header: str):
    
    # check availability of product
    if_available(session, product_id)
    
    # update price
    session.query(ProductTable).filter(ProductTable.product_id == product_id).\
        update({ProductTable.unit_price: unit_price})
        
    return { header : None }
    
            
    