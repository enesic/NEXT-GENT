#!/usr/bin/env python3
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="nextgent",
    user="postgres",
    password="password"
)

cur = conn.cursor()
cur.execute("""
    SELECT customer_id, name, 
           CASE WHEN pin_hash IS NOT NULL THEN 'VAR' ELSE 'YOK' END as pin_status
    FROM customers 
    WHERE customer_id LIKE '%-000001'
    ORDER BY customer_id
""")

print("\n=== Veritabanındaki Sektör Girişleri ===\n")
print(f"{'Müşteri ID':<15} | {'İsim':<30} | {'PIN Durumu'}")
print("-" * 70)

for row in cur.fetchall():
    print(f"{row[0]:<15} | {row[1]:<30} | {row[2]}")

cur.close()
conn.close()
