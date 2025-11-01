import pandas as pd
import duckdb
import os

DATA_DIR = 'data'
DB_FILE = 'samarth.duckdb'

# Try to read using proper encoding and separator
rain_path = os.path.join(DATA_DIR, 'rainfall.csv')
crop_path = os.path.join(DATA_DIR, 'crops.csv')

rain_df = pd.read_csv(rain_path, encoding='utf-8', on_bad_lines='skip')
crop_df = pd.read_csv(crop_path, encoding='utf-8', on_bad_lines='skip')

# Add traceability
rain_df['source_url'] = 'https://www.data.gov.in/resource/sub-divisional-monthly-rainfall-1901-2017'
crop_df['source_url'] = 'https://www.data.gov.in/resource/district-wise-season-wise-crop-production-statistics-1997'

# Save into a DuckDB database
con = duckdb.connect(DB_FILE)
con.execute("CREATE OR REPLACE TABLE rainfall AS SELECT * FROM rain_df")
con.execute("CREATE OR REPLACE TABLE crop_production AS SELECT * FROM crop_df")
con.close()

print("✅ Database created successfully: samarth.duckdb")
