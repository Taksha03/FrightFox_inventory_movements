# FreightFox Warehouse Inventory Analytics 📦

## 📌 Project Overview
This repository contains my submission for the FreightFox Data Analyst assignment (Warehouse Inventory Analytics).
The objective of this project is to analyze warehouse movement-level data to identify stock discrepancy patterns, evaluate supplier cost anomalies, and flag SKUs with negative inventory — all across 6 warehouses.

**Live Dashboard:** https://frightfoxinventorymovements-ktmgrj5pjgsggtaskn9ydf.streamlit.app/

## 🚀 Key Business Findings
- **Systemic Discrepancies:** The overall discrepancy rate sits between 8–11% across all 6 warehouses. **Pune** leads at 11.34%, but the uniform distribution confirms this is a network-wide operational issue rather than an isolated warehouse failure.
- **Supplier Cost Anomaly:** **SUP_09** is billing at an average of ₹10,559 per unit — a staggering **10.3x above the market average** of ₹1,026. An immediate procurement audit and contract renegotiation is required.
- **ERP System Bug:** The WMS (Warehouse Management System) physically allows dispatch transactions where `quantity > stock_before`, resulting in negative inventory. In some records, the subtraction math itself is corrupted (e.g., 1494 - 272 = -90). A hard-block validation is required at the dispatch layer.

## 🛠️ Tech Stack
- **Python:** Data cleaning and analysis (Pandas)
- **Visualization:** Plotly Express
- **Dashboard:** Streamlit

## 📁 Repository Structure
```
FrightFox_inventory_movements/
├── data/
│   └── inventory_movements.csv     # Raw dataset
├── app.py                          # Streamlit dashboard (with cleaning pipeline)
├── BUSINESS_ANSWERS.md             # Answers to all 5 business questions
├── requirements.txt                # Python dependencies for deployment
└── README.md                       # Project documentation
```

## 💻 How to Run Locally
1. Clone this repository:
   ```bash
   git clone https://github.com/Taksha03/FrightFox_inventory_movements.git
   ```
2. Navigate to the project directory:
   ```bash
   cd FrightFox_inventory_movements
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit dashboard:
   ```bash
   streamlit run app.py
   ```

## 🌍 Live Dashboard
The dashboard is deployed on **Streamlit Community Cloud** and is accessible via the Live Dashboard link at the top of this README.
No installation, Python, or terminal commands are required. Simply open the URL.
