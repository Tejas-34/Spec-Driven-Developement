# FocusSprint

FocusSprint is a full-stack study and productivity tracker designed specifically for students and candidates preparing for intense technical interviews. The application helps users run timed study blocks, count how many times they checked their phone, preserve daily study streaks, and analyze focus metrics.

This entire application was built systematically using Spec-Driven Development (SDD) principles via the OpenSpec framework. Every model, blueprint route, and UI element was designed, specified, and reviewed conceptually before any source code was generated. 

A humorous reminder for the distracted developer: This app includes an auto-seeding engine that populates 18 study sessions across 8 days upon registration. Why? Because looking at empty analytics charts is clinically proven to make developers cry, and we wanted you to see our beautiful graphs immediately without having to pretend you studied for 8 days straight first.

---

## Technical Architecture

The application is structured cleanly using professional Flask blueprints:
- **Extensions**: Manages database instances and login configurations.
- **Database Models**: Users (streaks, last activity records) and FocusSessions (duration, distractions, reflections, scores) stored locally via SQLite.
- **Authentication**: Fully secured login and registration powered by Flask-Login and Werkzeug password hashing.
- **Timer Engine**: Features a circular SVG progress countdown timer. It saves state in LocalStorage so a page refresh does not reset your active session.
- **Audio Synthesizer**: Utilizes the browser Web Audio API to play digital harmonic chimes upon session completion (meaning no audio file assets to lose or break).
- **Analytics & History**: Implements Chart.js dynamic wave graphs and scrollable history tables with client-side keyword search, category filtering, and raw CSV data exports.

---

## Application Screenshots

Here is what the application looks like when pushed to production. Please ensure you place your screenshots inside the `static/images/` directory before pushing to Git so they render correctly on GitHub.

### Landing Page
Path: `static/images/landing_page.png`
![Landing Page](static/images/landing_page.png)

### Dashboard Screen
Path: `static/images/dashboard_page.png`
![Dashboard Page](static/images/dashboard_page.png)

### Focus Analytics
Path: `static/images/analytics_page.png`
![Analytics Page](static/images/analytics_page.png)

### Register Page
Path: `static/images/register_page.png`
![Register Page](static/images/register_page.png)

---

## How to Set Up and Launch

Follow these steps to run the application on your local machine:

1. Create a Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the application dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask server:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to `http://127.0.0.1:5000` to begin sprinting.
