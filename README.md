# 🎓 StudentFit AI

![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AI](https://img.shields.io/badge/AI-Llama%203%20(Groq)-orange?style=for-the-badge)

**StudentFit AI** is a hyper-personalized fitness and nutrition planner designed specifically for university students. 

Unlike generic fitness apps, StudentFit understands the unique constraints of student life: **tight budgets, limited dorm room space, and specific cultural food preferences.** It uses the power of **Llama 3 (via Groq)** to generate full 7-day schedules instantly.

---

## 🚀 Key Features

* **⚡ AI-Powered Personalization:** Generates unique Monday-Sunday plans using **Groq (Llama 3)** for lightning-fast responses.
* **🏋️ Dorm-Friendly Workouts:** Tailors exercises to your available gear—whether you have a full university gym or just a dorm room floor.
* **🥗 Culture-Aware Nutrition:** Creates meal plans that respect your culinary background (e.g., Indian, Mexican, Asian) while keeping costs low.
* **🛒 Smart Grocery List:** Auto-calculates exact quantities (e.g., "1kg Rice", "1 Dozen Eggs") for a weekly student budget.
* **🎨 Glassmorphism UI:** A modern, dark-mode aesthetic with neon accents, interactive cards, and Lottie animations.

---

## 🛠️ Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/eleshkapri/Student_Fitness-AI.git](https://github.com/eleshkapri/Student_Fitness-AI.git)
cd Student_Fitness-AI

```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Setup API Key (Groq)

This project uses the **Groq API** (free tier available).

1. Get your key at [console.groq.com](https://console.groq.com).
2. Create a folder named `.streamlit` in the root directory.
3. Inside it, create a file named `secrets.toml`.
4. Paste your key:
```toml
GROQ_API_KEY = "gsk_your_actual_api_key_here"

```



### 5. Run the App

```bash
streamlit run app.py

```

---

## 📸 Screenshots

### 1. User Inputs & Dashboard

*(Note: You can upload your screenshots to a folder named 'screenshots' in your repo to display them here)*

### 2. The 7-Day Plan

---

## 📂 Project Structure

```text
Student_Fitness-AI/
├── .streamlit/
│   └── secrets.toml      # API Keys (Not uploaded to GitHub)
├── app.py                # Main application code
├── requirements.txt      # Python dependencies
├── .gitignore            # Files to exclude from Git
└── README.md             # Project documentation

```

## 🤝 Credits

* **Framework:** [Streamlit](https://streamlit.io/)
* **AI Model:** Llama 3 via [Groq Cloud](https://groq.com/)
* **Animations:** [LottieFiles](https://lottiefiles.com/)

---

### ⭐ Don't forget to star this repo if you found it useful!

```

```