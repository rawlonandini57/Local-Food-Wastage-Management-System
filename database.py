import sqlite3
import pandas as pd
import os

DB_PATH = "food_waste.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    """Create tables and load CSV data into SQLite database."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS providers (
            Provider_ID   INTEGER PRIMARY KEY,
            Name          TEXT,
            Type          TEXT,
            Address       TEXT,
            City          TEXT,
            Contact       TEXT
        );

        CREATE TABLE IF NOT EXISTS receivers (
            Receiver_ID   INTEGER PRIMARY KEY,
            Name          TEXT,
            Type          TEXT,
            City          TEXT,
            Contact       TEXT
        );

        CREATE TABLE IF NOT EXISTS food_listings (
            Food_ID       INTEGER PRIMARY KEY,
            Food_Name     TEXT,
            Quantity      INTEGER,
            Expiry_Date   TEXT,
            Provider_ID   INTEGER,
            Provider_Type TEXT,
            Location      TEXT,
            Food_Type     TEXT,
            Meal_Type     TEXT,
            FOREIGN KEY (Provider_ID) REFERENCES providers(Provider_ID)
        );

        CREATE TABLE IF NOT EXISTS claims (
            Claim_ID    INTEGER PRIMARY KEY,
            Food_ID     INTEGER,
            Receiver_ID INTEGER,
            Status      TEXT,
            Timestamp   TEXT,
            FOREIGN KEY (Food_ID)     REFERENCES food_listings(Food_ID),
            FOREIGN KEY (Receiver_ID) REFERENCES receivers(Receiver_ID)
        );
    """)

    # Load CSVs only if tables are empty
    base = os.path.dirname(os.path.abspath(__file__))

    if cursor.execute("SELECT COUNT(*) FROM providers").fetchone()[0] == 0:
        df = pd.read_csv(os.path.join(base, "providers_data.csv"))
        df.to_sql("providers", conn, if_exists="append", index=False)

    if cursor.execute("SELECT COUNT(*) FROM receivers").fetchone()[0] == 0:
        df = pd.read_csv(os.path.join(base, "receivers_data.csv"))
        df.to_sql("receivers", conn, if_exists="append", index=False)

    if cursor.execute("SELECT COUNT(*) FROM food_listings").fetchone()[0] == 0:
        df = pd.read_csv(os.path.join(base, "food_listings_data.csv"))
        df.to_sql("food_listings", conn, if_exists="append", index=False)

    if cursor.execute("SELECT COUNT(*) FROM claims").fetchone()[0] == 0:
        df = pd.read_csv(os.path.join(base, "claims_data.csv"))
        df.to_sql("claims", conn, if_exists="append", index=False)

    conn.commit()
    conn.close()
    print("✅ Database initialised successfully.")

def run_query(sql, params=()):
    conn = get_connection()
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()
    return df

def execute_dml(sql, params=()):
    """Run INSERT / UPDATE / DELETE and return rows affected."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected


# ─── 15 SQL Queries ───────────────────────────────────────────────────────────

QUERIES = {
    "Q1: Providers & Receivers per City": """
        SELECT city, COUNT(*) AS total_providers
        FROM providers
        GROUP BY city
        ORDER BY total_providers DESC
        LIMIT 20
    """,

    "Q2: Provider Type with Most Food Listings": """
        SELECT Provider_Type, COUNT(*) AS listing_count, SUM(Quantity) AS total_quantity
        FROM food_listings
        GROUP BY Provider_Type
        ORDER BY listing_count DESC
    """,

    "Q3: Contact Info of Providers by City": """
        SELECT Name, Type, Address, City, Contact
        FROM providers
        ORDER BY City
    """,

    "Q4: Receivers Who Claimed the Most Food": """
        SELECT r.Name, r.Type, r.City, COUNT(c.Claim_ID) AS total_claims
        FROM receivers r
        JOIN claims c ON r.Receiver_ID = c.Receiver_ID
        GROUP BY r.Receiver_ID
        ORDER BY total_claims DESC
        LIMIT 20
    """,

    "Q5: Total Food Quantity Available": """
        SELECT SUM(Quantity) AS total_quantity_available,
               COUNT(*)     AS total_listings
        FROM food_listings
    """,

    "Q6: City with Highest Number of Food Listings": """
        SELECT Location AS city, COUNT(*) AS listing_count, SUM(Quantity) AS total_quantity
        FROM food_listings
        GROUP BY Location
        ORDER BY listing_count DESC
        LIMIT 20
    """,

    "Q7: Most Commonly Available Food Types": """
        SELECT Food_Type, COUNT(*) AS count, SUM(Quantity) AS total_quantity
        FROM food_listings
        GROUP BY Food_Type
        ORDER BY count DESC
    """,

    "Q8: Food Claims per Food Item": """
        SELECT fl.Food_Name, fl.Food_Type, fl.Meal_Type,
               COUNT(c.Claim_ID) AS total_claims
        FROM food_listings fl
        LEFT JOIN claims c ON fl.Food_ID = c.Food_ID
        GROUP BY fl.Food_ID
        ORDER BY total_claims DESC
        LIMIT 20
    """,

    "Q9: Provider with Highest Successful Claims": """
        SELECT p.Name AS provider_name, p.Type AS provider_type, p.City,
               COUNT(c.Claim_ID) AS successful_claims
        FROM providers p
        JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID
        JOIN claims c ON fl.Food_ID = c.Food_ID
        WHERE c.Status = 'Completed'
        GROUP BY p.Provider_ID
        ORDER BY successful_claims DESC
        LIMIT 20
    """,

    "Q10: Claim Status Breakdown (%)": """
        SELECT Status,
               COUNT(*) AS count,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS percentage
        FROM claims
        GROUP BY Status
    """,

    "Q11: Average Quantity Claimed per Receiver": """
        SELECT r.Name, r.Type, r.City,
               ROUND(AVG(fl.Quantity), 2) AS avg_quantity_claimed
        FROM receivers r
        JOIN claims c ON r.Receiver_ID = c.Receiver_ID
        JOIN food_listings fl ON c.Food_ID = fl.Food_ID
        GROUP BY r.Receiver_ID
        ORDER BY avg_quantity_claimed DESC
        LIMIT 20
    """,

    "Q12: Most Claimed Meal Type": """
        SELECT fl.Meal_Type, COUNT(c.Claim_ID) AS total_claims
        FROM food_listings fl
        JOIN claims c ON fl.Food_ID = c.Food_ID
        GROUP BY fl.Meal_Type
        ORDER BY total_claims DESC
    """,

    "Q13: Total Quantity Donated per Provider": """
        SELECT p.Name AS provider_name, p.Type, p.City,
               SUM(fl.Quantity) AS total_donated
        FROM providers p
        JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID
        GROUP BY p.Provider_ID
        ORDER BY total_donated DESC
        LIMIT 20
    """,

    "Q14: Food Listings Expiring Soon (Next 30 Days)": """
        SELECT Food_Name, Quantity, Expiry_Date, Location, Food_Type, Meal_Type
        FROM food_listings
        WHERE date(Expiry_Date) BETWEEN date('now') AND date('now', '+30 days')
        ORDER BY Expiry_Date
        LIMIT 50
    """,

    "Q15: Monthly Claim Trends": """
        SELECT substr(Timestamp, 1, 7) AS month,
               COUNT(*)                AS total_claims,
               SUM(CASE WHEN Status='Completed' THEN 1 ELSE 0 END) AS completed,
               SUM(CASE WHEN Status='Pending'   THEN 1 ELSE 0 END) AS pending,
               SUM(CASE WHEN Status='Cancelled' THEN 1 ELSE 0 END) AS cancelled
        FROM claims
        GROUP BY month
        ORDER BY month
    """,
}

if __name__ == "__main__":
    init_db()
    for name, sql in QUERIES.items():
        print(f"\n{'='*60}\n{name}\n{'='*60}")
        print(run_query(sql).to_string(index=False))
