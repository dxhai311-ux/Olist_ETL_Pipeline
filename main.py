from etl import (
	extract,
 	transform,
 	load
)
from db import get_engine

TABLES = [
	('olist_orders_dataset.csv', 'orders'),
	('olist_customers_dataset.csv', 'customers'),
	('olist_sellers_dataset.csv', 'sellers'),
	('olist_products_dataset.csv', 'products'),
	('olist_order_items_dataset.csv', 'order_items'),
	('olist_order_payments_dataset.csv', 'order_payments'),
	('olist_order_reviews_dataset.csv', 'order_reviews'),
	('olist_geolocation_dataset.csv', 'geolocation'),
	('product_category_name_translation.csv', 'category_translation')
]

def run_pipeline():
	engine = get_engine()
	for file_name, table_name in TABLES:
		df = extract(file_name)
		df = transform(df, table_name)
		load(df, engine, table_name)
	

def check_file(file_name : str) -> None:
	import pandas as pd
	df = extract(file_name)
	#df = transform(df, 'category_translation')
	df.info()

if __name__ == "__main__":
	run_pipeline()
	#check_file()
