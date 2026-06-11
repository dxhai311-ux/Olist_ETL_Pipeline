import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine #Class Engine dùng để type hint 

load_dotenv()

def get_engine() -> Engine: # Hàm này trả về 1 đối tượng Engine

	# Gọi là docstring , có thể truy cập được bằng cách : get_engine.__doc__ 
	"""Return SQLAlchemy engine for PostgreSQL."""

	#os.getenv('ten_bien', 'gia_tri_mac_dich')
	user = os.getenv('DB_USER')
	password = os.getenv('DB_PASSWORD')
	host = os.getenv('DB_HOST')
	db_name = os.getenv('DB_NAME')
	port = os.getenv('DB_PORT', '5432') # nếu không có env thì trả về 5432

	#all() kiểm tra tất cả giá trị có tồn tại hay không
	#dùng tuple vì các biến không thay đổi
	if not all((user, password, host, db_name, port)):
		#raise báo lỗi và dừng chương trình 
		raise ValueError(
			'Thiếu thông tin database trong .env!'
		)

	connection_url = (
		f"postgresql+psycopg2://"
		f"{user}:{password}@{host}:{port}/{db_name}"
	)

	#trả về object Engine
	return create_engine(connection_url)