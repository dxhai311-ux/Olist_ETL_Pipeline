import pandas as pd 


def extract(file_name : str) -> pd.DataFrame:
	"""
	Read csv file from data folder
	"""

	file_path = f"data/{file_name}"

	df = pd.read_csv(file_path)

	return df 