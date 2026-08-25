# ⚡ StudentFit AI — Fitness Synced to Your Syllabus

<div align="center">

[![Live Website](https://img.shields.io/badge/Live%20Website-student--fitness--ai.vercel.app-FF6B54?style=for-the-badge&logo=vercel&logoColor=white)](https://student-fitness-ai.vercel.app/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Groq AI](https://img.shields.io/badge/Groq%20Cloud-Llama%203.3%20%7C%20GPT--OSS%20%7C%20Qwen-E4FF5B?style=for-the-badge&logoColor=black)](https://groq.com)
[![Architecture](https://img.shields.io/badge/Architecture-Secure%20OOP-9C8CFF?style=for-the-badge)](https://github.com/eleshkapri/Student_Fitness-AI)

**Hyper-personalized weekly fitness, nutrition & budget grocery planning designed specifically for university students.**

[🌐 Explore Live Website](https://student-fitness-ai.vercel.app/) • [🚀 Get Started](#-installation--local-setup) • [🏛️ OOP Architecture](#-object-oriented-architecture-oop) • [📂 Project Structure](#-project-structure)

</div>

---

## 📖 About StudentFit AI

Most commercial fitness apps assume you have a fully equipped kitchen, a car for shopping trips, hundreds of dollars in weekly grocery budgets, and hours of free time.

**StudentFit AI was built between lectures and leftovers.** It plans around the real variables of college life:
- **Dorm-Room Space & Gear:** Whether you have full university gym access, a pair of dumbbells, or just a 6x4 ft dorm room floor.
- **Global Region & Currency Selector:** Auto-synchronizes local currency (`INR ₹`, `USD $`, `EUR €`, `GBP £`, `CAD $`, `AUD $`, `JPY ¥`), cuisine defaults, and metric/imperial units.
- **Campus Cooking Constraints:** Meal prep tailored for Microwave/Kettle Only, Single Induction/Basic Stove, or Full Kitchen Chef.
- **Exam Week Stress Relief:** First-class wellness focus, cognitive fuel, and active recovery routines tailored to exam season.
- **Custom Fitness Targets:** Type in any write-in goal (*e.g. Marathon Prep, Vertical Jump, Posture Correction*).
- **Persistent State:** Saves your chosen active tab and region in `localStorage` & URL hash so reloading never loses your progress.

---

## 🌟 Key Features

| Feature | Description |
| :--- | :--- |
| **⚡ 7-Page Unified Suite** | Seamless navigation across **Home**, **How it Works**, **Features**, **Macro Hub**, **Plans**, **Our Story**, and **AI Planner Studio**. |
| **🌍 Global Region Selector** | Sleek navbar dropdown syncing currency, cuisine defaults, metric/imperial units, and plan tier pricing. |
| **🎯 Custom Target Input** | Preset goals (*Build Muscle, Lose Fat, Athletic Tone, Exam Relief*) plus custom write-in goals with instant AI synchronization. |
| **🏃‍♂️ Campus Bio-Data** | Calculates BMR, TDEE, target calories, and macro splits (Protein, Carbs, Fats, Water) in metric and imperial. |
| **🥗 Synchronized Meal Plans** | High-protein recipes respecting cultural palettes (Indian, Global, Mediterranean, Asian, Vegan) with realistic batch prep. |
| **🛒 1-Person Grocery List** | Itemized shopping checklist with realistic estimated costs in your local currency. |
| **📄 Formatted PDF Export** | Client-side and server-side, print-ready A4 PDF download of your complete 7-day schedule and grocery checklist. |
| **🔘 Collapsible Studio Sidebar** | Toggle between clean full-screen schedule reading (`✕ Close`) and live parameter tuning (`⚡ Show Controls ▸`). |
| **📱 Mobile-First Responsive** | 2-tier sticky mobile header with horizontal auto-centering pill scroll, touch swipe day cards, and hardware-accelerated 60fps animations. |
| **🛡️ Hardened Security** | Strict Content Security Policy (CSP), Permissions-Policy, 100KB DoS payload limits, and OOP sanitization. |

---

## 🏛️ Object-Oriented Architecture (OOP)

The backend is built upon a secure, modular **Object-Oriented Programming (OOP)** foundation:

```
┌─────────────────────────────────────────────────────────────┐
│                    FitnessPlannerService                    │
│                      (Composite Facade)                     │
└──────────────────────────────┬──────────────────────────────┘
                               │
       ┌───────────────────────┼────────────────────────┐
       ▼                       ▼                        ▼
┌──────────────┐      ┌─────────────────┐      ┌────────────────┐
│StudentProfile│      │BasePlanGenerator│      │ BasePlanParser │
│(Encapsulation│      │ (Polymorphism)  │      │ (Abstraction)  │
│& Validation) │      └────────┬────────┘      └───────┬────────┘
└──────────────┘               │                       │
                     ┌─────────┴─────────┐             ▼
                     ▼                   ▼     ┌────────────────┐
             ┌───────────────┐   ┌───────────┐ │MarkdownPlan    │
             │MockPlan       │   │GroqPlan   │ │Parser          │
             │Generator      │   │Generator  │ └────────────────┘
             └───────────────┘   └───────────┘
```

### 1. Encapsulation & Defensive Validation (`planner/models.py`)
- **`StudentProfile`**: Encapsulates student bio-data with strict property getters/setters.
- **Defensive Boundary Clamping**: Automatically protects against out-of-bounds payloads ($14 \le \text{age} \le 90$, $25.0 \le \text{weight} \le 350.0\text{ kg}$, $50.0 \le \text{height} \le 260.0\text{ cm}$).
- **Injection Sanitization**: Strips control characters and escapes HTML inputs to prevent prompt injection and XSS.
- **`MacroResult`**, **`DailyPlan`**, **`WeeklyFitnessPlan`**: Encapsulates typed data transfer objects.

### 2. Abstraction & Single Responsibility (`planner/calculator.py` & `planner/prompt_builder.py`)
- **`MacroCalculator`**: Encapsulates Mifflin-St Jeor metabolic math and student activity multipliers.
- **`StudentPromptBuilder`**: Separates prompt structuring and formatting delimiters from execution logic.
- **`SecretsManager`**: Encapsulates multi-source API key resolution (`env`, `.streamlit/secrets.toml`, parameter).

### 3. Inheritance & Polymorphism (`planner/generators.py` & `planner/parser.py`)
- **`BasePlanGenerator` (ABC)** $\to$ **`MockPlanGenerator`** & **`GroqPlanGenerator`** (with automated candidate model failover cascade).
- **`BasePlanParser` (ABC)** $\to$ **`MarkdownPlanParser`** (pre-compiled regexes with singleton performance caching).
- **`PDFReportGenerator` (`planner/pdf_service.py`)**: Encapsulates character transliteration, typography, and A4 page breaks.

---

## 📂 Project Structure

```
Student_Fitness-AI/
├── api/                      # Vercel Serverless REST & Web Engine
│   ├── index.py              # Single-page app + API routes (CSP & Security headers)
│   └── requirements.txt      # Lightweight serverless dependencies (<15MB bundle)
├── pages/                    # Streamlit Multi-Page Studio Views
│   ├── __init__.py           # Package marker
│   ├── home.py               # Hero with 3D fanned 7-card deck & live metrics
│   ├── how_it_works.py       # Parameter breakdowns & syllabus synchronization
│   ├── features.py           # 3D interactive flip cards & animated marquee
│   ├── macro_hub.py          # Student BMR, TDEE & Macro Calculator Studio
│   ├── plans.py              # Transparent student tier concepts ($0 / $3 / $8)
│   ├── story.py              # Campus dorm & exam-week survival philosophy
│   └── generator.py          # 7-day synchronized AI planner studio
├── planner/                  # Core OOP Domain Models & AI Orchestration
│   ├── __init__.py           # Unified package exports & facades
│   ├── models.py             # StudentProfile (Validation, Sanitization, Bounds)
│   ├── calculator.py         # MacroCalculator (Mifflin-St Jeor metabolic math)
│   ├── prompt_builder.py     # StudentPromptBuilder (LLM prompt engineering)
│   ├── parser.py             # MarkdownPlanParser (Pre-compiled regex engine)
│   ├── pdf_service.py        # PDFReportGenerator (A4 PDF compilation engine)
│   ├── generators.py         # BasePlanGenerator, Mock, Groq & FitnessPlannerService
│   └── llm_client.py         # LLM client & backward-compatibility facade
├── .gitignore                # Production ignore rules
├── .python-version           # Explicit Python runtime version for Vercel (3.11)
├── app.py                    # Streamlit application router
├── requirements.txt          # Python dependencies (Streamlit & Full Suite)
├── theme.py                  # Shared design tokens & 3D ambient layers
├── vercel.json               # Modern zero-warning Vercel rewrites configuration
└── README.md                 # Complete documentation
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
