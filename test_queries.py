import sqlite3
import pandas as pd

conn = sqlite3.connect('nykaa.db')

with open('queries.sql', 'r') as f:
    sql_script = f.read()

queries = [q.strip() for q in sql_script.split(';') if q.strip()]

with open('query_results.txt', 'w', encoding='utf-8') as out:
    for i, query in enumerate(queries, 1):
        header = f"\n{'='*60}\nQUERY {i}\n{'='*60}\n"
        print(header)
        out.write(header)
        try:
            df = pd.read_sql_query(query, conn)
            print(df.head(10))
            print(f"\nRows returned: {len(df)}")
            out.write(df.head(10).to_string())
            out.write(f"\n\nRows returned: {len(df)}\n")
        except Exception as e:
            err = f"Error: {e}"
            print(err)
            out.write(err + "\n")

conn.close()
print("\n✅ Full results saved to query_results.txt")