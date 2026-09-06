# src/db.py
import os
import duckdb

DB_PATH = "edisco-pipeline/data/processed/ediscovery.duckdb"

def get_connection(db_path: str = DB_PATH):
    """Establishes and returns a connection to the DuckDB database."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return duckdb.connect(db_path)

def init_db(db_path: str = DB_PATH):
    """Creates the base eDiscovery schema in DuckDB if it doesn't already exist."""
    conn = get_connection(db_path)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            document_id VARCHAR PRIMARY KEY,
            filename VARCHAR NOT NULL,
            file_path VARCHAR NOT NULL,
            file_type VARCHAR NOT NULL,
            file_size_bytes BIGINT NOT NULL,
            md5_hash VARCHAR NOT NULL,
            custodian VARCHAR,
            author VARCHAR,
            recipient VARCHAR,
            document_date VARCHAR,
            subject VARCHAR,
            raw_text TEXT,
            cluster_id VARCHAR,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Create indexes for fast metadata & deduplication queries
    conn.execute("CREATE INDEX IF NOT EXISTS idx_md5 ON documents(md5_hash);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_custodian ON documents(custodian);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_cluster ON documents(cluster_id);")
    
    conn.close()
    print("✅ DuckDB schema initialized successfully.")

if __name__ == "__main__":
    init_db()