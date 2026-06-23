from etl import (
	extract,
 	transform,
 	load
)
from db import get_engine
import logging 

#Cấu hình mặc địch cho hệ thống logging

logging.basicConfig(        #là 1 hàm để cấu hình logging nhanh 
	level = logging.INFO, # dùng để hiện thị nếu là informat = "%(asctime)s - %(levelname)s - %(message)s"
	#format là định dạng log khi in ra terminal
	
	format = "%(asctime)s - %(levelname)s - %(message)s"
	#asctime : thời gian log
	#levelname : mức độ log
	#message : nội dung 
)


logger = logging.getLogger(__name__) # tạo object logger như nhân viên nhật kí

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
	logger.info("Starting ETL Pipeline")
	engine = get_engine()
	for file_name, table_name in TABLES:
		logger.info(f"Processing table : %s", table_name)
		df = extract(file_name)
		logger.info(
			f"Extracted %s rows from %s", len(df), table_name)
		df = transform(df, table_name)
		logger.info(
			f"Tranformed %s, remaining rows : %s", table_name, len(df))
		load(df, engine, table_name)
		logger.info(
			f"Loaded %s into PoestgreSQL", table_name)
	

def check_file(file_name : str) -> None:
	import pandas as pd
	df = extract(file_name)
	#df = transform(df, 'category_translation')
	df.info()

if __name__ == "__main__":
	run_pipeline()
	#check_file()
