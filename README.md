# 🍽️ Local Food Wastage Management System

A full-stack data project connecting surplus food providers with those in need.

## Tech Stack
- **Python** · **SQLite** · **Streamlit** · **Plotly** · **Pandas**

## Setup Instructions

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Place your CSV files in this folder
- `providers_data.csv`
- `receivers_data.csv`
- `food_listings_data.csv`
- `claims_data.csv`

### 3. Run the app
```bash
streamlit run app.py
```

The database (`food_waste.db`) is created automatically on first run.

---

## Project Structure
```
food_waste_app/
├── app.py              ← Streamlit UI (4 pages)
├── database.py         ← SQLite setup + 15 SQL queries
├── requirements.txt
├── providers_data.csv
├── receivers_data.csv
├── food_listings_data.csv
└── claims_data.csv
```

## Features
| Page | Features |
|------|---------|
| 📊 Dashboard | KPI metrics, pie/bar charts, city analysis |
| 🔍 SQL Queries | All 15 queries with interactive charts + CSV export |
| 🗺️ Explore Data | Filter providers, receivers, food listings, claims |
| ✏️ CRUD | Add/update/delete providers, receivers, listings, claims |
