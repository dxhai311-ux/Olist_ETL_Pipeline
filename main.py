from etl import extract, transform

def run_pipeline():

	df = extract(
		"olist_orders_dataset.csv"
	)

	df = transform(df)

	df.info()

if __name__ == "__main__":
	run_pipeline()