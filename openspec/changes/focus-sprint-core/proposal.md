## Why

Modern productivity tools are often generic, boring, and disconnected from the real psychological hurdles of studying and interview preparation, such as distraction management and reflection. FocusSprint aims to solve this by providing a premium, highly immersive, dark-themed, and responsive web application tailored for students and candidates preparing for interviews, using structured focus sprints, live gamified distraction tracking, post-session reflections, and intuitive productivity analytics.

## What Changes

We will build a complete full-stack web application with the following key changes:
- **Project Structure**: Establish a clean Flask application layout using blueprints, templates, and static resources under `sdd_submission`.
- **Database Schema**: Implement SQLite with SQLAlchemy models for Users, FocusSessions, and Streaks.
- **User Authentication**: Add a secure login/registration system with hashed passwords and session management via Flask-Login.
- **Live Focus Timer**: Create an interactive canvas or SVG circular timer with keyboard shortcuts, audio cues (bell), and live distraction logging.
- **Interactive Dashboard**: Build a dark-theme, glassmorphism-styled main hub displaying real-time productivity statistics, streaks, and charts.
- **Session Notes & Reflections**: Enable users to document takeaways, revision points, and calculate a custom productivity score upon completing each session.
- **Analytics & History**: Add a detailed session history table with CSV export, search/filtering, and interactive Chart.js visualizations.
- **Settings**: Include user profile preferences and a dark/light mode toggle.

## Capabilities

### New Capabilities
- `user-auth`: Full user registration, secure login/logout, password hashing, and session persistence.
- `focus-core`: Core task sprint creation, a highly polished circular live timer, keyboard shortcuts, live distraction tracker, post-session notes, and streak calculations.
- `productivity-analytics`: History table, search/filter, CSV export, and rich data visualization charts for streaks, focus hours, and distraction patterns.
- `settings-preferences`: Theme customization (dark/light toggle) and user profile metadata settings.

### Modified Capabilities
*(None. This is a greenfield implementation of FocusSprint.)*

## Impact

- **Database**: Introduction of `database.db` with relational constraints.
- **Routes**: Blueprint-based routing to keep the Flask app clean and maintainable.
- **Assets**: Structured directories for modular CSS, JS, sound chimes, and images.
- **Third-Party Libraries**: Integration of Flask, SQLAlchemy, Flask-Login, and Chart.js.
