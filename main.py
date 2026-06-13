from etl import extract, transform, load
from db import get_engine

def run_pipeline():

	df = extract(
		"olist_orders_dataset.csv"
	)

	df = transform(df)

	engine = get_engine()
	load(df, engine, 'orders')	

if __name__ == "__main__":
	run_pipeline()