CREATE TABLE IF NOT EXISTS orders (
	order_id SERIAL PRIMARY KEY,
	client_id VARCHAR( 50 ) NOT NULL,
	status VARCHAR( 50 ) NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
	product_id SERIAL PRIMARY KEY,
	stock INT CHECK (stock >= 0),
	description VARCHAR( 250 ),
	unit_price DECIMAL(12,2) CHECK (unit_price >= 0)
);

CREATE TABLE IF NOT EXISTS join_orders_products (
	id SERIAL PRIMARY KEY,
    	order_id INT,
    	product_id INT,
	unit_price Decimal(12,2) CHECK (unit_price >= 0),
    	FOREIGN KEY (order_id) REFERENCES orders(order_id),
    	FOREIGN KEY (product_id) REFERENCES products(product_id)
);
