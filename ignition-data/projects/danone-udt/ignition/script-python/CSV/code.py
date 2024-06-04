"""
This script provides DanPT specific CSV functions
"""
import csv

LOGGER = system.util.getLogger("General.Conversion")

def convert_dataset_to_list(dataset):
	"""
	DESCRIPTION: This function converts a dataset to a list of dictionaries 
	PARAMETERS: dataset (REQ, dataset): The dataset to be converted to a list of dictionaries
	"""
	LOGGER.trace("convert_dataset_to_list(dataset=%s)" % (dataset))
	
	if not hasattr(dataset, "getColumnNames"):
		return dataset
	
	column_names = dataset.getColumnNames()

	data = []
	
	for row in range(dataset.getRowCount()):
		row_data = {}
		for column in range(dataset.getColumnCount()):
			row_data[column_names[column]] = dataset.getValueAt(row, column)
		data.append(row_data)
	return data

def parse_csv_into_list(file_string, as_dataset=False):
	"""
	DESCRIPTION: Parses csv string into a list of dictionaries
	VARIABLES: file_string, (REQ, str): csv data
			as_dataset, (bool): flag to return as a dataset or list
	RETURNS: list, (list): csv formatted into a list of dictionaries OR
			dataset, (dataset): csv formatted into an Ignition Dataset
	"""
	file_string = file_string.replace('\xef\xbb\xbf', '')
	file_string.replace('\r', '').replace('\r', '')
	
	f = file_string.split('\n')
	
	reader = csv.reader(f)

	row_data = []
	for index, row in enumerate(reader):
		if index == 0:
			headers = row
			continue
		if len(row) != len(headers):
			continue
		row_data.append(row)
	
	dataset = system.dataset.toDataSet(headers, row_data)
	if as_dataset:
		return dataset
	return convert_dataset_to_list(dataset)