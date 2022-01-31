INSERT INTO products(description,unit_price,stock) VALUES
	('Heater',300.00,20),
	('Fridge',600.00,10),
	('AC',450.00,5),
	('TV',800.00,9),
	('Computer',600.00,15),
	('Cellphone',900.00,2),
	('Remote control',20.00,30),
	('Mouse',30.00,50),
	('Lamp',50.00,3),
	('Monitor',400.00,8),
	('Charger',25.00,10),
	('Alarm clock',20.00,15),
	('Speaker',30.00,8);

INSERT INTO orders(client_id,status) VALUES
	('1','Released'),
	('2','Cancelled');

INSERT INTO join_orders_products(order_id,product_id,unit_price) VALUES
	(1,3,350.00);	
