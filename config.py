import pandas as pd
import csv

with open('2015.csv', mode='r', newline='', encoding='latin-1') as f:
    reader = csv.reader(f)
    column_names = next(reader)
print(column_names)
