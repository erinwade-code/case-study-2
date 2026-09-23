path_input = "data/raw/2015.csv"
output_folder = "outputs/"

required_columns = ['tq', 'countryorigin_iso3', 'dutiablevaluephp']
filter_values = {}
grouping_columns = []

config = {
    "input_path": path_input,
    "required_columns": required_columns,
    "filter_values": filter_values,
    "grouping_columns": grouping_columns,
    "output_folder": output_folder,
}

print(config)
