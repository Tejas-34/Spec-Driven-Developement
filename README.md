# FocusSprint ⚡
> A premium, high-fidelity futuristic dark-glassmorphism productivity SaaS dashboard built for students, developers, and creators to turn deep work into visible progress.

---

## 🎨 Premium Visual Aesthetics

FocusSprint is engineered with state-of-the-art modern SaaS UI aesthetics (drawing inspiration from platforms like Linear, Raycast, and Vercel):
- **Futuristic Dark Theme**: Curated harmonious HSL-tailored palette (`--bg: #040814`) with dynamic, fluid neon blur backdrops (`--cyan`, `--purple`, `--pink`).
- **Clean Glassmorphism**: Cards and panels styled with advanced semi-transparent layers (`rgba(10, 18, 35, 0.72)`), subtle thin borders, soft outer shadows, and backdrop filters (`blur(22px)`).
- **Single-Screen Fold Layout**: Authenticated dashboard pages lock dynamically to `100vh` on desktop viewports, removing vertical scrollbars to fit all focus metrics, weekly charts, motivation panels, and upcoming sessions cleanly in a single viewport.
- **Fixed Sidebar with Independent Scrolling**: Provides quick navigation while scoping vertical scrollbars exclusively to page content panels on long list views (History) or charts (Analytics).
- **Micro-Animations & Glow Effects**: Smooth hover transitions, scaling icons, active menu glowing borders, and high-contrast violet name shadow greetings (`Good evening, Tejas! 👋`).

---

## 🚀 Screenshots Showcase

### 1. The Dynamic Dashboard (`/dashboard`)
Fully responsive layout displaying the flex-configured stats cards, curating real-time focus metrics (`2h 35m`, `8 Days Streak`), curved gradient line charts, motivational quotes, and study sprint timer controls.
![FocusSprint Dashboard](/Users/tejas/Documents/IITM Workshop HandsOn/Task/vibe_coded_submission/static/images/dashboard_page.png)

### 2. High-Contrast Analytics Grid (`/analytics`)
Displays a symmetric, balanced grid of charts (Weekly focus hours, Daily distractions, and Productivity trend) fitting elegantly into the screen.
![Analytics Dashboard](/Users/tejas/Documents/IITM Workshop HandsOn/Task/vibe_coded_submission/static/images/analytics_page.png)

### 3. Glassmorphic Landing Page (`/`)
A widescreen aesthetic landing page introducing study sprints, distraction metrics, and consistency locks with visual mock preview cards.
![Landing Page](/Users/tejas/Documents/IITM Workshop HandsOn/Task/vibe_coded_submission/static/images/landing_page.png)

### 4. Minimalist Register Screen (`/register`)
Futuristic split-screen registration layout designed with high readability, neon gradient inputs, and micro-focused branding.
![Register Screen](/Users/tejas/Documents/IITM Workshop HandsOn/Task/vibe_coded_submission/static/images/register_page.png)

---

## ⚡ Core Features

- **Widescreen Study Sprints**: Create focused sessions with custom titles, categories, and custom/preset sprint durations.
- **Interactive Focus Timer**: Live circular SVG progress ring, pause/resume state controls, distraction counter triggers, completion bell, and rapid keyboard shortcuts (`S` to Start, `P` to Pause, `D` to Log Distraction).
- **Post-Session Reflections**: Document mistakes, learnings, reflection notes, and revision points instantly.
- **Auto-Seeding Metrics**: Guarantees new users are greeted with gorgeous sample charts instantly, automatically seeding exactly 18 mock sessions across 8 days if they have `< 5` completed sessions.
- **Searchable History**: Filter, query, and search through previous sprints by category or completion status, with robust CSV exporting.
- **Dynamic Quotes Engine**: Capsule-themed motivation block with a dynamic quote refreshment cycle.

---

## 🛠️ Technology Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy (SQLite Database)
- **Frontend Logic**: Vanilla JavaScript, Chart.js (with curved wave chart nodes and customized y-axis ticks formatters)
- **Styling & UI**: HTML5 Semantic markup, HSL custom styling tokens, Google Fonts (`Inter`, `Space Grotesk`)
- **Assets**: Raw inline SVGs for responsive UI menus, Web Audio API synthesis for timer chime sound (no static media dependencies).

---

## 📂 Project Directory Structure

```text
vibe_coded_submission/
├── app.py                     # App entry point, SQLite DB, Flask extensions init
├── models.py                  # SQLAlchemy schemas (User, FocusSession, Seed mock data)
├── extensions.py              # Shared SQLAlchemy & LoginManager instances
├── routes/
│   ├── auth.py                # Registration, login, logout, & hashed credential keys
│   └── main.py                # Dashboard rendering, export, & auto-seed checks
├── templates/
│   ├── base.html              # Dynamic app grid frame, profile cards, and theme configs
│   ├── dashboard.html         # Real-time metrics, SVG progress widgets, and charts
│   ├── analytics.html         # Symmetric analytics chart containers
│   ├── history.html           # Searchable sprint tables and CSV downloads
│   ├── session.html           # SVG progress timers, short keys, and reflections
│   ├── session_create.html    # Create-a-sprint input cards
│   ├── index.html             # Premium landing page features
│   └── auth/                  # Login and register pages
├── static/
│   ├── css/
│   │   └── style.css          # Premium glassmorphic styling system (43KB)
│   ├── js/
│   │   ├── main.js            # Sun/Moon theme capsules, quotes, and sidebar logic
│   │   ├── dashboard.js       # Wave line charts & formatted ticks
│   │   ├── analytics.js       # Symmetrically styled analytics graphs
│   │   └── session.js         # Sound synthesis, short keys, and SVG rings
│   └── images/                # Copied high-fidelity screenshots
│       ├── landing_page.png
│       ├── register_page.png
│       ├── dashboard_page.png
│       └── analytics_page.png
├── instance/
│   └── database.db            # SQLite focus database file (auto-generated)
└── requirements.txt           # Python dependency lists
```

---

## 🚀 Setup & Execution

### 1. Activate Environment & Install Dependencies
Ensure you have Python 3.8+ installed. Navigate to the project root directory:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows

# Install Flask, SQLAlchemy, and dependencies
pip install -r requirements.txt
```

### 2. Start the App Server
```bash
python app.py
```
*Note: The Flask server runs on development mode with debug-reloads enabled. The SQLite database will be initialized automatically as `instance/database.db` upon the first request.*

### 3. Open the App in Your Browser
Navigate to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

### 4. Sample Seed Account
If you register a new account, the app **automatically seeds mock sessions** instantly upon landing on the dashboard for the first time. This guarantees beautiful weekly charts and metrics without manual entry!
