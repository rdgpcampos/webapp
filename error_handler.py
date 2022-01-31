#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 00:02:24 2022

@author: rodrigocampos
"""
from database_objects import OrderTable, ProductTable

class InvalidRequest(Exception):
    pass

class CancelledOrder(Exception):
    pass

def if_valid(session,order_id):
    
    q = session.query(OrderTable.status).\
                       filter(OrderTable.order_id == order_id).all()
    
    if len(q) == 0:
        raise InvalidRequest("Invalid order ID")

    if q[0][0] == 'Cancelled':
        raise CancelledOrder("This order was cancelled")
    
    return True

def if_available(session,product_id):
    
    q = session.query(ProductTable.unit_price).\
                        filter(ProductTable.stock > 0,
                               ProductTable.product_id == product_id).all()
    
    if len(q) == 0:
        raise InvalidRequest("Product not available")
    
    return True,q[0][0]