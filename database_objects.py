#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 23:51:25 2022

@author: rodrigocampos
"""
# database-related classes and methods

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy_utils import database_exists,create_database
from sqlalchemy.orm import sessionmaker, mapper
from dataclasses import dataclass, asdict
import simplejson as json

class OrderTable(object):
    pass

class ProductTable(object):
    pass

class JoinTable(object):
    pass

@dataclass
class SingleProduct:
    product_id: int
    product_description: str
    product_price : str
    
@dataclass
class SingleOrder:
    order_id: int
    product_list : dict
    total_price : str
    client_id: str = '0'
    status : str = 'Released'


def make_into_product(query_row):
    return SingleProduct(query_row[0], query_row[1], json.dumps(query_row[2]))

def make_into_order(query,order_id):
    
    product_list = []
    total_price = 0
    
    for row in query:
        product_list.append(asdict(make_into_product(row)))
        total_price += row[2]
        
    return SingleOrder(order_id, product_list, json.dumps(total_price))
    
def insert_joint(session,order_id,product_id,unit_price):
    new_joint = JoinTable()
    new_joint.order_id = order_id
    new_joint.product_id = product_id
    new_joint.unit_price = unit_price
    session.add(new_joint)
    
    session.flush()
    session.refresh(new_joint)
    return new_joint.id
    
def insert_order(session,client_id,status):
    new_order = OrderTable()
    new_order.client_id = client_id
    new_order.status = status
    session.add(new_order)
    
    session.flush()
    session.refresh(new_order)
    return new_order.order_id
    
def connect_to_db():
    engine = create_engine("postgresql+psycopg2://postgres:postgres@db:5432/postgres")

    metadata = MetaData(engine)
    
    orders = Table('orders',metadata,autoload_with=engine)
    mapper(OrderTable,orders)
    
    products = Table('products',metadata,autoload_with=engine)
    mapper(ProductTable,products)
    
    joint = Table('join_orders_products',metadata,autoload_with=engine)
    mapper(JoinTable,joint)
    
    Session = sessionmaker(bind=engine)
    
    return Session
