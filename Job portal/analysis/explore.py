import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import psycopg2
from config import DB_CONFIG

conn = psycopg2.connect(**DB_CONFIG)

df = pd.read_sql("""
    SELECT 
        j.title,
        j.department,
        j.location,
        j.first_published,
        j.updated_at,
        j.pay_min,
        j.pay_max,
        j.currency,
        j.url,
        j.description,
        c.name as company
    FROM jobs j
    JOIN companies c ON j.company_id = c.id
""", conn)

conn.close()

print("Total jobs:", len(df))
print("\nJobs per company:")
print(df["company"].value_counts())

print("\nJobs per department:")
print(df["department"].value_counts().head(10))

print("\nJobs per location:")
print(df["location"].value_counts().head(10))

print("\nJobs with pay disclosed:")
print(df[df["pay_min"].notna()][["company", "title", "pay_min", "pay_max", "currency"]])