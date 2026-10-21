
# 🧬 Immunology Web Application (BIA0403)

An interactive, full-stack web application developed for an Immunology academic project. The platform models and tracks immunological concepts—including antigen interactions, diagnostic simulations, and cellular responses—using a Python backend and a relational database.

---

## 🚀 Features
* **Antigen Module (`antigen.html`):** Explore and manage data related to various antigens and their biological properties.
* **Cellular Interaction Simulator (`interaction.html`):** Visualize and query immune cell interactions and pathways.
* **Diagnosis Tracker (`diagnosis.html`):** Record, query, and simulate immunological diagnostic scenarios.
* **Persistent Storage:** Integrated **SQLite** database managed via Python to store and query relational immunological data.

---

## 🛠️ Tech Stack
* **Backend:** Python, Flask
* **Database:** SQLite
* **Frontend:** HTML5, CSS3 (Custom styling via `static/style.css`)

---

## 📂 Project Structure
```text
BIA0403-immunology/
│
├── app.py                  # Main Flask application and database routing logic
├── requirements.txt        # Python package dependencies
├── static/
│   └── style.css           # Custom CSS styling and responsive dashboard UI
└── templates/
    ├── base.html           # Master template layout with navigation bar
    ├── index.html          # Main landing dashboard
    ├── antigen.html        # Antigen tracking view
    ├── interaction.html    # Cell interaction simulation view
    └── diagnosis.html      # Immunological diagnosis view
```

---

## ⚙️ Getting Started Locally

Follow these steps to run the application on your local machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/poosithkanna-s/BIA0403-immunology.git
   cd BIA0403-immunology
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   Navigate to `http://127.0.0.1:5000/` to launch the app UI.

---

## 👤 Author
* **Poosith Kanna S**
* *B.Tech Computer Science and Biosciences*

