import pandas as pd

justin_data = pd.read_csv("trackman-csv-export-20230807.Normalized.csv", skiprows = 1)
print(justin_data.columns)