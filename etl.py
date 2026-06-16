import pandas as pd 
from sqlalchemy.engine import Engine
from pathlib import Path 

# __file__ : đường dẫn tới file hiện tại 
# .parent  : thư mục chứa file hiện tại
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" # tương đương : os.path.join(BASE_DIR, "data")

def extract(file_name : str) -> pd.DataFrame:
	"""
	Read csv file from data folder
	"""

	file_path = DATA_DIR / file_name
	
	df = pd.read_csv(file_path)

	return df	

def transform(df : pd.DataFrame, table_name) -> pd.DataFrame:
	if table_name == 'orders':
		return transform_orders(df)
	elif table_name == 'products':
		return transform_products(df)
	elif table_name == 'customers':
		return transform_basic(df, 'customer_id')
	elif table_name == 'sellers':
		return transform_basic(df, 'seller_id')
	elif table_name == 'order_items':
		return transform_with_datetime(
				df,
				['order_id', 'order_item_id'],
				['shipping_limit_date']
			)
	elif table_name == 'order_reviews':
		return transform_with_datetime(
				df,
				['order_id', 'review_id'],
				['review_creation_date', 'review_answer_timestamp']
			)
	elif table_name == 'order_payments':
		return transform_basic(df, ['order_id', 'payment_sequential'])
	elif table_name == 'geolocation':
		return transform_geolocation(df)
	elif table_name == 'category_translation':
		return transform_basic(df, 'product_category_name')
	else:
		return df

def transform_products(df : pd.DataFrame) -> pd.DataFrame:

	#B1: Drop duplicate theo primary key
	df = df.drop_duplicates(subset = 'product_id')

	#B2: Xóa các đơn thiếu thông tin 
	df = df.dropna(subset = [
		'product_category_name',
		'product_name_lenght',
		'product_description_lenght',
		'product_photos_qty'
	])

	return df

def transform_basic(df : pd.DataFrame, primary_key) -> pd.DataFrame:
	"""Transform basic primary key"""

	#B1: Drop duplicate theo primary key
	df = df.drop_duplicates(subset = primary_key)

	return df

def transform_orders(df : pd.DataFrame) -> pd.DataFrame:
	"""
	Transfrom delivered orders only.
	"""

	#B1: Lọc đơn đã giao
	df = df[df['order_status'] == 'delivered']
	
	#B2: Lọc các nhân bản trong df
	#Chỉ lọc order_id vì nó là khóa chính 
	df = df.drop_duplicates(subset = ['order_id'])

	#B3: Xóa các cột NULL vì đã lọc delivered nên không thể NULL
	df = df.dropna(subset = [
		'order_approved_at',
		'order_delivered_carrier_date',
		'order_delivered_customer_date'
		])

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

def transform_with_datetime(
	df : pd.DataFrame,
	primary_keys : list,
	datetime_cols : list
) -> pd.DataFrame:
	
	"""Drop duplicates and convert datetime columns"""
	df = df.drop_duplicates(subset = primary_keys)

	for col in datetime_cols:
		df[col] = pd.to_datetime(df[col])

	return df

def transform_geolocation(df : pd.DataFrame) -> pd.DataFrame:
	"""Aggregate geolocation by zip code prefix"""

	#agg() nhận vào 1 dict
	#{'tên_cột' : 'hàm_áp_dụng'}
	df = df.groupby('geolocation_zip_code_prefix').agg({
		#Lấy trung bình tọa đọo vì 1 zip code có nhiều điểm tọa đọo khác nhau
		'geolocation_lat' : 'mean',
		'geolocation_lng' : 'mean',

		#Lấy giá trị xuất hiện nhiều nhất vì 1 zip code có thể có nhiều city/state
		#mode() trả về series giảm dần -> [0] là lấy giá trị đầu tiên trong series đó
		#nếu bằng nhau thì xếp theo alphabet
		'geolocation_city' : lambda x : x.mode()[0],
		'geolocation_state' : lambda x : x.mode()[0]
	}).reset_index() #đưa zip code từ index về thành cột bình thường

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