# ✈️ Flight Assistant — Real-Time Flight Dashboard & Chatbot

This project provides a **real-time flight dashboard** and a **chatbot interface** that allows users to:

- View live flight data from the [Aviationstack API](https://aviationstack.com/)
- Store and manage data in **Google BigQuery**
- Interact via natural queries (e.g., “AI302” or “BLR to DEL”) using a **terminal-based chatbot**
- Visualize data using a **Streamlit** dashboard with a live table and pie chart

---

## ✅ Features

- 🔄 **Live flight data fetch** (100–200 flights per request)
- 🧠 **Smart chatbot** using regex-based routing
- 📊 **Beautiful dashboard** with pie chart + flight table
- 🌍 **BigQuery integration** with auto schema update
- 🎯 **City pair insights** like "BLR to DEL"
- 🛬 **Flight status lookup** like "AI202"
- 🇮🇳 **Time conversion** to Indian Standard Time (IST)
- 🖼️ **Flight background image** on dashboard

---

## 🧱 Prerequisites

1. **Python 3.8+**
2. **Google Cloud project** with BigQuery API enabled
3. **Aviationstack API key**
4. **Service Account Key** (`.json`) for BigQuery access

---

🔐 `.env` Configuration

- Create a `.env` file in your root directory:
- PROJECT_ID=your-gcp-project-id
- DATASET_ID=avaiation_data
- TABLE_ID=weekly_flight_logs
- AVIATIONSTACK_API_KEY=your_aviationstack_api_key

Set:
--
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account.json

⚙️ Installation
1️⃣ Clone the Repository
--- 
```bash
git clone https://github.com/ssharmak/flight-assistant-chatbot.git
cd flight-assistant
```

2️⃣ Create Virtual Environment (optional) 
```bash
python -m venv venv
venv\Scripts\activate # On Windows
# OR
source venv/bin/activate  # On macOS/Linux
```

3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

🏗️ Setup BigQuery Table
Create the table and update schema if needed:
```bash
python scripts/setup_bigquery.py
```
Test environment variables:
```bash
python scripts/env_check.py
```

📥 Fetch and Upload Flight Data

```bash
python scripts/fetch_and_upload.py
```

✅ This will insert the latest flights into BigQuery.

📊 Run the Streamlit Dashboard
```bash
streamlit run dashboards/flight_dashboard.py
```
Click 🔁 to refresh flight data from the API

Shows all flights in a live table

Displays pie chart of status distribution

💬 Run the Chatbot
```bash
python chatbot.py
```
Sample Queries:
AI302 (Flight number) 

## 🔍 Technologies Used
| Component  | Technology              |
| ---------- | ----------------------- |
| Backend    | Python 3, Regex         |
| APIs       | Aviationstack API       |
| Data Store | Google BigQuery         |
| Dashboard  | Streamlit, Plotly       |
| Auth       | GCP Service Account     |
| Deployment | Local / Streamlit Cloud |
---
