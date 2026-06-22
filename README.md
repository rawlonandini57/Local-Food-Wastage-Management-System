# 🍽️ Local Food Wastage Management System

A Python-based data application that connects **surplus food providers** with **people in need** — reducing food waste through smart tracking, SQL analytics, and an interactive Streamlit dashboard.

---

## 📌 Project Overview

Every day, restaurants, supermarkets, and catering services discard massive amounts of edible food while NGOs and shelters struggle to feed people. This system bridges that gap by:

- Letting providers list surplus food items
- Allowing NGOs and individuals to claim them
- Tracking every interaction through a SQL database
- Visualizing trends through an interactive web dashboard

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| ![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python) | Core language |
| ![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?logo=sqlite) | Local SQL database |
| ![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit) | Interactive web app |
| ![Plotly](https://img.shields.io/badge/Plotly-Charts-purple?logo=plotly) | Data visualizations |
| ![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green?logo=pandas) | Data manipulation |

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
```

---

## 🗄️ Database Schema

```
providers          receivers
──────────         ──────────
Provider_ID  ←──┐  Receiver_ID  ←──┐
Name             │  Name             │
Type             │  Type             │
Address          │  City             │
City             │  Contact          │
Contact          │                   │
                 │  food_listings    │
                 │  ───────────────  │
                 └─ Provider_ID      │   claims
                    Food_ID     ←──┐ │   ───────────
                    Food_Name       │ │   Claim_ID
                    Quantity        └─┼── Food_ID
                    Expiry_Date       └── Receiver_ID
                    Provider_Type         Status
                    Location              Timestamp
                    Food_Type
                    Meal_Type
```

---

## 📊 15 SQL Queries Covered

| # | Query | Description |
|---|-------|-------------|
| Q1 | Providers per City | Cities with the most food providers |
| Q2 | Provider Type Analysis | Which type lists the most food |
| Q3 | Provider Contact Info | Directory of all providers by city |
| Q4 | Top Receivers | Receivers who claimed the most food |
| Q5 | Total Food Available | Overall food quantity in the system |
| Q6 | Cities with Most Listings | Hotspot cities for food availability |
| Q7 | Food Type Distribution | Vegetarian vs Vegan vs Non-Vegetarian |
| Q8 | Most Claimed Food Items | Which foods get claimed most |
| Q9 | Top Performing Providers | Providers with highest completed claims |
| Q10 | Claim Status Breakdown | % of Completed / Pending / Cancelled |
| Q11 | Avg Quantity per Receiver | Who receives the most food per claim |
| Q12 | Meal Type Popularity | Breakfast vs Lunch vs Dinner vs Snacks |
| Q13 | Total Donations per Provider | Quantity donated by each provider |
| Q14 | Expiring Soon | Food listings expiring in next 30 days |
| Q15 | Monthly Claim Trends | Day-wise claim volume over time |

---

## 🖥️ App Features

### 📊 Dashboard
- KPI cards — total food, completed/pending/cancelled claims
- Provider type pie chart
- Claim status bar chart
- Food type distribution
- Meal type popularity
- Top 10 cities by listings

### 🔍 SQL Queries Page
- Select and run any of the 15 queries
- View SQL code
- Interactive charts (bar / line / scatter)
- Download results as CSV

### 🗺️ Explore Data
- Filter **Providers** by city and type
- Filter **Receivers** by city and type
- Filter **Food Listings** by location, food type, meal type, provider type
- Search **Claims** by status and receiver name

### ✏️ CRUD Operations
- ➕ Add new food listings
- ✏️ Update claim status (Pending → Completed / Cancelled)
- 🗑️ Delete food listings
- ➕ Add new providers
- ➕ Add new receivers

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/food-waste-management.git
cd food-waste-management
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

The SQLite database (`food_waste.db`) is created **automatically** on first run.

> 🌐 The app opens at `http://localhost:8501`

---

## 📦 Requirements

```
streamlit>=1.32.0
pandas>=2.0.0
plotly>=5.18.0
```

---

## 📈 Dataset Summary

| Dataset | Records | Key Columns |
|---------|---------|-------------|
| Providers | 2,000 | Name, Type, City, Contact |
| Receivers | 1,000 | Name, Type, City, Contact |
| Food Listings | 1,000 | Food_Name, Quantity, Expiry_Date, Meal_Type |
| Claims | 1,000 | Status, Timestamp |

---

## 🙋 Author

**Your Name**
- GitHub: [@rawlonandini57](https://github.com/rawlonandini57)
- LinkedIn: [nandini-rawlo](https://www.linkedin.com/in/nandini-rawlo-34b2043a3/)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> ⭐ If you found this project helpful, please give it a star on GitHub!
