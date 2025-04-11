# export_snomed.py
import argparse
import os
import psycopg2
import pandas as pd
import polars as pl

def get_table_names(conn, schema):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = %s
        """, (schema,))
        return [r[0] for r in cur.fetchall()]

def fetch_table_as_polars(conn, schema, table):
    with conn.cursor() as cur:
        cur.execute(f'SELECT * FROM {schema}.{table}')
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=columns)
        return pl.from_pandas(df)

def export_all_tables(conn, schema, tables, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for table in tables:
        df = fetch_table_as_polars(conn, schema, table)
        path = os.path.join(output_dir, f'{table}.csv')
        df.write_csv(path)
        print(f'Exported: {path}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', choices=['csv'], required=True)
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()

    db_user = "username"
    db_password = "password"
    db_host = "localhost"
    db_port = "5432"
    db_name = "SCT_20250101"
    schema = "snomedct"

    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )

    if args.type == 'csv':
        tables = get_table_names(conn, schema)
        export_all_tables(conn, schema, tables, args.output)

    conn.close()

if __name__ == '__main__':
    main()
