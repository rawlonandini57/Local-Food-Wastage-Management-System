# 🍽️ Local Food Wastage Management System

A Python-based data application that connects surplus food providers with people in need — reducing food waste through smart tracking, SQL analytics, and an interactive Streamlit dashboard.
----------------------------------------------------------------------------------------------------------------------------

## 📌 Project Overview

Every day, restaurants, supermarkets, and catering services discard massive amounts of edible food while NGOs and shelters struggle to feed people. This system bridges that gap by:

- Letting providers list surplus food items
- Allowing NGOs and individuals to claim them
- Tracking every interaction through a SQL database
- Visualizing trends through an interactive web dashboard

## Features
- View available food donations
- Filter food by city, provider type, food type, and meal type
- View provider contact details
- Run 15 SQL analysis queries
- Add, update, and delete food listings
- Add food claims
- View dashboard metrics and charts
  
## Problem Statement

Food wastage is a significant issue, where many households and restaurants discard surplus food while many people struggle with food insecurity.

The aim of this project is to develop a Local Food Wastage Management System where restaurants and individuals can list surplus food, and NGOs or individuals in need can claim the available food.

The system uses SQL to store food details, provider information, receiver information, locations, and claim records. A Streamlit web application is used to interact with the data, apply filters, perform CRUD operations, and visualize food donation insights.

A full-stack data project connecting surplus food providers with those in need.

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| ![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python) | Core language |
| ![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?logo=sqlite) | Local SQL database |
| ![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit) | Interactive web app |
| ![Plotly](https://img.shields.io/badge/Plotly-Charts-purple?logo=plotly) | Data visualizations |
| ![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green?logo=pandas) | Data manipulation |

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

## 📁 Project Structure

```
food-waste-management/
│
├── app.py                    # Main Streamlit application
├── database.py               # SQLite setup + 15 SQL queries
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
│
├── providers_data.csv        # 2000 food providers
├── receivers_data.csv        # 1000 receivers (NGOs, shelters, individuals)
├── food_listings_data.csv    # 1000 food listings
└── claims_data.csv           # 1000 food claims

## Features
| Page | Features |
|------|---------|
| 📊 Dashboard | KPI metrics, pie/bar charts, city analysis |
| 🔍 SQL Queries | All 15 queries with interactive charts + CSV export |
| 🗺️ Explore Data | Filter providers, receivers, food listings, claims |
| ✏️ CRUD | Add/update/delete providers, receivers, listings, claims |
