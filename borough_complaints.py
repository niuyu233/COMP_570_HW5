
import argparse
import pandas as pd

p = argparse.ArgumentParser(description="Count 311 complaints by type and borough in a date range")
p.add_argument("-i", required=True, help="input csv file")
p.add_argument("-s", required=True, help="start date, YYYY-MM-DD")
p.add_argument("-e", required=True, help="end date, YYYY-MM-DD")
p.add_argument("-o", help="output file (default: print to screen)")
a = p.parse_args()

df = pd.read_csv(a.i, usecols=["Created Date", "Complaint Type", "Borough"])
df["Created Date"] = pd.to_datetime(df["Created Date"], format="%m/%d/%Y %I:%M:%S %p")

end = pd.to_datetime(a.e) + pd.Timedelta(days=1)          # include the end date
df = df[(df["Created Date"] >= a.s) & (df["Created Date"] < end)]

result = df.groupby(["Complaint Type", "Borough"]).size().reset_index(name="count")
result.columns = ["complaint type", "borough", "count"]
result.to_csv(a.o, index=False)  if a.o else print(result.to_csv(index=False))