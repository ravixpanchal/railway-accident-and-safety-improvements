# 🚂 Railway Accident Analysis Dashboard

> An interactive data analytics dashboard built with Streamlit, exploring **3,859 European railway accident investigations** to surface safety patterns, causes, and risk factors across **31 countries** (2002–2025).

---

## 📌 Project Overview

This project is a **B.Tech 3rd Year academic project** focused on Exploratory Data Analysis (EDA) and safety intelligence for European railway systems. It leverages the **ERAIL (European Railway Accident Investigation Links)** database, a comprehensive repository of accident investigation reports compiled by the European Union Agency for Railways (ERA).

The dashboard enables users to interactively filter, visualize, and interpret accident data across time, geography, severity, and accident type — helping identify systemic risks and safety improvement opportunities.

---

## 🎯 Key Features

| Feature | Description |
|---|---|
| 🌗 **Theme Toggle** | Switch between Dark and Light mode instantly |
| 📅 **Year Range Filter** | Slice data by any year range (2002–2025) |
| 🌍 **Country Filter** | Focus on specific countries or regions |
| ⚠️ **Occurrence Type Filter** | Filter by accident category (derailment, collision, SPAD, etc.) |
| 📊 **22 Interactive Charts** | Plotly-powered visualisations across 5 analysis tabs |
| 🧠 **Observation Insights** | AI-style commentary on every chart |
| 📱 **Fully Responsive** | Adapts to laptop, tablet, and mobile |

---

## 🗂️ Dashboard Tabs

### 📊 Tab 1 — Temporal Analysis
- Accidents per year (bar chart)
- Yearly trend line with annotations
- Accidents by hour of day
- Day-of-week distribution
- Weather condition breakdown

### ⚠️ Tab 2 — Causes & Types
- Top occurrence types
- Cause category breakdown
- Severity category distribution
- Weather vs severity correlation

### 💥 Tab 3 — Severity & Fatalities
- Severity level distribution
- Fatal vs Non-Fatal split
- Fatalities by category (Passenger / Staff / Unauthorised)
- Fatality trends over years
- Correlation matrix heatmap

### 🌍 Tab 4 — Geography
- Top 15 countries by accident count
- Average fatalities by location type
- Average severity by railway system
- Accident types × country heatmap

### 🔬 Tab 5 — Deep Dive
- Line type distribution
- Movement type at accident
- Monthly accident heatmap by year
- Stacked area chart — fatality types over time
- Summary statistics table

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| **Frontend** | Streamlit 1.32+ |
| **Data Processing** | Pandas 2.0+, NumPy 1.24+ |
| **Visualisation** | Plotly Express & Graph Objects 5.18+ |
| **File I/O** | OpenPyXL 3.1+ |
| **Fonts** | Syne, DM Sans, JetBrains Mono (Google Fonts) |
| **Data Source** | ERAIL European Railway Accident Database (ERA) |

---

## 📦 Project Structure

```
📁 railway-accident-dashboard/
├── app.py                  # Main Streamlit application
├── erail_database.xlsx     # ERAIL accident database (Excel)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9 or higher
- pip

### 1. Clone the repository

```bash
git clone https://github.com/your-username/railway-accident-dashboard.git
cd railway-accident-dashboard
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Place the data file

Ensure `erail_database.xlsx` is in the **same directory** as `app.py`. The app reads from the `Investigations` sheet.

### 4. Run the app

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501` in your browser.

---

## 📋 Requirements

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
openpyxl>=3.1.0
matplotlib
```

---

## 🗃️ Data Source

**ERAIL — European Railway Accident Investigation Links**
Maintained by the **European Union Agency for Railways (ERA)**

The dataset includes:
- Accident date, time, country, and location
- Occurrence/accident type classification
- Fatalities and serious injuries by category (Passenger, Staff, LC User, Unauthorised)
- Railway system type and line type
- Investigation reports and findings

> ⚠️ Data columns with sensitive investigation details (legal basis, report links, body names) have been removed for anonymisation and to focus on quantitative safety analysis.

---

## 📐 Severity Classification

Accident types are mapped to severity levels (1–4) as follows:

| Level | Label | Example Types |
|---|---|---|
| 1 | Near Miss / Low | Operational event, Near miss |
| 2 | Moderate | SPAD, Broken rails, Track buckles |
| 3 | Serious | Derailment, Level crossing accident, Fire |
| 4 | Critical | Train collision, Dangerous goods release |

---

## 🖥️ Screenshots

> The dashboard features a fully themed dark/light interface with animated KPI cards, gradient hero section, and 22 interactive Plotly charts.

**Dark Mode** — Deep navy background with blue accent highlights  
**Light Mode** — Clean white/slate background with blue accent highlights

---

## 👥 Team

Made with ❤️ by **Team RailAnalytics**  
B.Tech 3rd Year — Data Science & Analytics Project

📧 [ravi.panchal.kaithi@gmail.com](mailto:ravi.panchal.kaithi@gmail.com)

---

## 📄 License

This project is intended for **academic and educational purposes only**.  
The ERAIL dataset is publicly available via the European Union Agency for Railways.

---

*© 2026 RailAnalytics Team · All Rights Reserved*
