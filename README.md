# ⚡ StudentFit AI — Fitness Synced to Your Syllabus

<div align="center">

[![Live Website](https://img.shields.io/badge/Live%20Website-student--fitness--ai.vercel.app-FF6B54?style=for-the-badge&logo=vercel&logoColor=white)](https://student-fitness-ai.vercel.app/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Groq AI](https://img.shields.io/badge/Groq%20Cloud-Llama%203%20%7C%20Compound%20%7C%20Qwen-E4FF5B?style=for-the-badge&logoColor=black)](https://groq.com)

**Hyper-personalized weekly fitness, nutrition & budget grocery planning designed specifically for university students.**

[🌐 Explore Live Website](https://student-fitness-ai.vercel.app/) • [🚀 Get Started](#-installation--local-setup) • [📖 Architecture](#-project-architecture)

</div>

---

## 📖 About StudentFit AI

Most commercial fitness apps assume you have a fully equipped kitchen, a car for shopping trips, hundreds of dollars in weekly grocery budgets, and hours of free time.

**StudentFit AI was built between lectures and leftovers.** It plans around the real variables of college life:
- **Dorm-Room Space & Gear:** Whether you have full university gym access, a pair of dumbbells, or just a 6x4 ft dorm room floor.
- **Realistic Student Budgets:** Cheap, Moderate, and Premium tiers with localized currencies (`INR ₹`, `USD $`, `EUR €`, `GBP £`, `CAD $`, `AUD $`, `AED د.إ`).
- **Campus Cooking Constraints:** Meal prep for Microwave/Kettle Only, Single Induction/Basic Stove, or Full Kitchen Chef.
- **Exam Week Stress Relief:** First-class wellness focus, cognitive fuel, and active recovery routines tailored to exam season.
- **Custom Fitness Targets:** Type in any goal (*e.g. Marathon Prep, Vertical Jump, Posture Correction*).

---

## 🌟 Key Features

| Feature | Description |
| :--- | :--- |
| **⚡ 6-Page Unified Suite** | Seamless navigation across **Home**, **How it Works**, **Features**, **Plans**, **Our Story**, and **AI Planner Studio**. |
| **🎯 Custom Target Input** | Preset goals (*Build Muscle, Lose Fat, Athletic Tone, Exam Relief*) plus custom write-in goals with instant AI synchronization. |
| **🏃‍♂️ Campus Bio-Data** | Calculates BMR, TDEE, target calories, and macro splits (Protein, Carbs, Fats, Water) in metric and imperial. |
| **🥗 Synchronized Meal Plans** | High-protein recipes respecting cultural palettes (Indian, Global, Mediterranean, Asian, Vegan) with realistic batch prep. |
| **🛒 1-Person Grocery List** | Itemized shopping checklist with realistic estimated costs in your local currency. |
| **📄 Formatted PDF Export** | Client-side, print-ready A4 PDF download of your complete 7-day schedule and grocery checklist. |
| **🔘 Collapsible Studio Sidebar** | Toggle between clean full-screen schedule reading (`✕ Close`) and live parameter tuning (`⚡ Show Controls ▸`). |
| **🌌 3D Interactive Atmosphere** | 3D particle constellation starfield with touch/mouse parallax, perspective Cybergrid horizon, and volumetric drifting gradient blobs. |
| **📱 Mobile-First Responsive** | 2-tier sticky mobile header with horizontal auto-centering pill scroll and tap-to-flip cards. |

---

## 📂 Project Architecture

```
Student_Fitness-AI/
├── app.py                   # Central Streamlit entry point with st.navigation() router
├── theme.py                 # Shared design tokens, Google Fonts, 3D tilt JS & ambient blobs
├── pages/
│   ├── __init__.py          # Pages package initialization
│   ├── home.py              # Hero with 3D fanned 7-card deck, stat ticker, testimonials
│   ├── how_it_works.py      # Detailed breakdown of all parameters & sync state
│   ├── features.py          # 6 3D interactive flip cards & complete literal marquee strip
│   ├── plans.py             # Cheap ($0), Moderate ($3), and Premium ($8) concept tiers
│   ├── story.py             # Positioning narrative for student housing & exam weeks
│   └── generator.py         # AI Planner Studio with sidebar wizard, dark cards & PDF export
├── planner/
│   ├── __init__.py          # Planner package initialization & facade exports
│   ├── prompt_builder.py    # Strict LLM prompt generator honoring student constraints
│   └── llm_client.py        # Groq client with model fallback cascade & PDF compilation
├── api/
│   └── index.py             # Serverless Flask web app for Vercel deployment
├── core.py                  # Lightweight compatibility facade (zero code duplication)
├── requirements.txt         # Optimized Python dependencies
├── vercel.json              # Vercel v2 serverless deployment configuration
├── .gitignore               # Clean standard exclusions
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

# Windows (PowerShell):
.\venv\Scripts\activate

# Mac / Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup API Key (Optional for Simulation)
This project uses **Groq Cloud AI** with automated model failover (`GPT-OSS`, `Compound`, `Qwen`, `Llama 3.3`).

Create a `.streamlit/secrets.toml` file:
```toml
GROQ_API_KEY = "gsk_your_actual_api_key_here"
```
*(If no API key is provided, the platform automatically runs in Simulation / Demo Mode with realistic sample schedules).*

### 5. Launch the Streamlit App
```bash
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## 🚀 Vercel Deployment

The repository is pre-configured for one-click deployment on **Vercel** via serverless Python (`api/index.py` & `vercel.json`):

1. Fork or import this repository on [vercel.com](https://vercel.com).
2. Set Environment Variable: `GROQ_API_KEY = gsk_...` (optional).
3. Click **Deploy**!

---

## 🤝 Tech Stack & Credits

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/) & [Flask](https://flask.palletsprojects.com/)
- **Inference Engine:** [Groq Cloud](https://groq.com/) (Llama 3.3 70B, GPT-OSS, Compound, Qwen)
- **PDF Engine:** [fpdf2](https://py-pdf.github.io/fpdf2/) & [html2pdf.js](https://ekoopmans.github.io/html2pdf.js/)
- **Design System:** Space Grotesk, Plus Jakarta Sans, Space Mono, Caveat
- **Developer:** [Elesh Kapri](https://github.com/eleshkapri)

---

<div align="center">
⭐ <b>Star this repository if StudentFit AI helps you conquer campus fitness and exams!</b>
</div>
