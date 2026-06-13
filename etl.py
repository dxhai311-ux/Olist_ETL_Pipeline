import pandas as pd 
from sqlalchemy.engine import Engine

def extract(file_name : str) -> pd.DataFrame:
	"""
	Read csv file from data folder
	"""

	file_path = f"data/{file_name}"

	df = pd.read_csv(file_path)

	return df 

def transform(df : pd.DataFrame) -> pd.DataFrame:
	"""
	Transfrom delivered orders only.
	"""

	#B1: Lọc đơn đã giao
	df = df[df['order_status'] == 'delivered']
	
	#B2: Lọc các nhân bản trong df
	#Chỉ lọc order_id vì nó là khóa chính 
	df = df.drop_duplicates(subset = ['order_id'])

	#B3: Xóa các cột NULL vì đã lọc delivered nên không thể NULL
	df = df.dropna(subset = ['order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date'])

	#B4: Str convert datetime
	date_cols = [
		'order_purchase_timestamp',
		'order_approved_at',
		'order_delivered_carrier_date',
		'order_delivered_customer_date',
		'order_estimated_delivery_date'
	]
	#Dùng for vì data nhỏ, phù hợp với project 
	for col in date_cols:
		df[col] = pd.to_datetime(df[col])

	#B5: Thêm cột để tính số ngày giao đúng hạn, sớm hạn, trễ hạn
	df['delivery_delay'] = (
		df['order_delivered_customer_date'] - df['order_estimated_delivery_date']
	).dt.days
	return df

def load(df : pd.DataFrame, engine : Engine, table_name : str) -> None:

	"""Load DataFrame into PostgreSQL table"""

	df.to_sql(
		name = table_name, 
		con = engine, 
		#replace - xóa bảng cũ, tạo bảng mới
		#append = giữ bảng cũ, thêm data vào cuối
		#fail - báo lỗi nếu bảng đã tồn tại
		if_exists = 'replace', 
		index = False, #Pandas tự tạo cột STT -> False k tạo
		chunksize = 1000 # thay vì load toàn bộ data, thì load 1000row tránh tốn ram và timeout khi data lớn
	)