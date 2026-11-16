from modules.data_loader import load_csv
from modules.profiler import profile_data
from modules.kpi_engine import calculate_kpis
from modules.summary import generate_summary

df = load_csv("data/sales.csv")

print(df)

profile_data(df)

calculate_kpis(df)

generate_summary(df)