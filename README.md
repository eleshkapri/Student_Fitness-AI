# ⚡ StudentFit AI — Fitness Synced to Your Syllabus

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-000000?style=for-the-badge&logo=flask&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-black?style=for-the-badge&logo=vercel&logoColor=white)
![Groq AI](https://img.shields.io/badge/AI-Groq%20Cloud-orange?style=for-the-badge)

**StudentFit AI** is a hyper-personalized fitness, nutrition, and grocery planning platform designed specifically around real student constraints: **dorm room space, college grocery budgets, cooking appliances, and exam week schedules.**

---

## 🌟 Key Features

* **⚡ 6-Page Unified Experience:** Multi-page website featuring Home, How it Works, Features (6 3D flip cards & marquee), Plans & Tiers, Our Story, and AI Planner Studio.
* **🏋️ Dorm-Adaptive Workouts:** Workouts adapt to your exact space and gear (Full University Gym, Dumbbells Only, or No Equipment Dorm Floor).
* **🥗 Synchronized Campus Nutrition:** High-protein meal plans honoring your cuisine (Indian, Global, Mediterranean, Asian, Vegan) using affordable student staples.
* **🛒 1-Person Weekly Grocery Checklist:** Exact quantities with localized prices (₹ INR, $ USD, € EUR, £ GBP, etc.).
* **📄 Formatted PDF Export:** One-click download of your personalized 7-day schedule and grocery checklist formatted for A4 print.
* **🌌 3D Interactive Design:** Particle parallax constellation canvas, 65° perspective Cybergrid horizon, and volumetric drifting atmosphere blobs.
* **📱 Multi-Screen Responsive:** Mobile-first layout with horizontal scroll navigation, collapsible sidebar, and responsive 3D hero deck.

---

## 📂 Project Architecture

```
Student_Fitness-AI/
├── app.py                   # Central Streamlit entry point with st.navigation()
├── theme.py                 # Shared design tokens, Google Fonts, 3D tilt JS & ambient blobs
├── pages/
│   ├── home.py              # Hero with 3D fanned 7-card deck, stat ticker, testimonials
│   ├── how_it_works.py      # Detailed breakdown of all parameters & sync state
│   ├── features.py          # 6 3D interactive flip cards & complete literal marquee strip
│   ├── plans.py             # Cheap ($0), Moderate ($3), and Premium ($8) concept tiers
│   ├── story.py             # Positioning narrative for student housing & exam weeks
│   └── generator.py         # AI Planner Studio with sidebar wizard, paper cards & PDF export
├── planner/
│   ├── __init__.py          # Package initialization & facade exports
│   ├── prompt_builder.py    # Strict LLM prompt generator honoring student constraints
│   └── llm_client.py        # Groq client with model fallback cascade & PDF compilation
├── api/
│   └── index.py             # Serverless Flask web app for Vercel deployment
├── core.py                  # Compatibility facade over planner package
├── requirements.txt         # Python dependencies
├── vercel.json              # Vercel v2 serverless deployment configuration
└── README.md                # Project documentation
```

---

## 🛠️ Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/eleshkapri/Student_Fitness-AI.git
cd Student_Fitness-AI
```

### 2. Create and Activate a Virtual Environment
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

### 4. Setup API Key (Optional for Simulation)
Add your Groq API key in `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "gsk_your_actual_api_key_here"
```

### 5. Run the Streamlit Application
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🚀 Vercel Deployment

The repository includes `api/index.py` and `vercel.json` pre-configured for Vercel Python Serverless functions:
1. Connect your repository on [vercel.com](https://vercel.com).
2. Set Environment Variable: `GROQ_API_KEY = gsk_...` (optional).
3. Deploy!

---

## 🤝 Tech Stack & Credits

* **Frameworks:** [Streamlit](https://streamlit.io/) & [Flask](https://flask.palletsprojects.com/)
* **AI Engine:** [Groq Cloud](https://groq.com/) (GPT-OSS / Compound / Qwen / Llama)
* **PDF Engine:** [fpdf2](https://py-pdf.github.io/fpdf2/) & [html2pdf.js](https://ekoopmans.github.io/html2pdf.js/)
* **Typography:** Space Grotesk, Plus Jakarta Sans, Space Mono, Caveat
