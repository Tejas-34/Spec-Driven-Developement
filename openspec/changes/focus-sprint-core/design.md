## Context

The "FocusSprint" application is a premium productivity hub designed to help students and professionals running focused study blocks. Unlike generic calendar or todo apps, this system prioritizes deep-work metrics: active focus time, streaks, distraction logging, and structured post-session reflections. This design doc maps the technical implementation using a secure, responsive, blueprint-driven Flask structure with SQLite/SQLAlchemy, Jinja2, vanilla JS, and Chart.js.

## Goals / Non-Goals

**Goals:**
- Provide secure user session management (Flask-Login) and encrypted credentials (Werkzeug).
- Implement a responsive glassmorphism web interface optimized for mobile and desktop screens.
- Build an animated SVG-based circular focus timer with local state, keyboard shortcuts, and distraction logging.
- Track daily streaks and compute custom productivity scores (`Minutes - 2 × Distractions`).
- Visualize statistics (weekly hours, distraction patterns, score trends) using Chart.js.
- Allow dynamic filtering and search, plus CSV export for historical session data.

**Non-Goals:**
- Real-time collaborative sessions or multiplayer study rooms.
- Advanced third-party integrations (Google Calendar, Outlook).
- Direct mobile app compilation (strictly a web app).

## Decisions

### 1. Database Model Design
We will use SQLAlchemy ORM with two primary tables:
- **`User`**: Handles authentication details, registration date, and persistent streak metadata.
- **`FocusSession`**: Stores title, category, duration, distraction count, productivity score, status, reflection text columns, and relational user mapping.

### 2. Frontend Layout & Theme System
- **Core Aesthetic**: Dark theme with high-vibrancy neon accent glows (purple, cyan, pink), responsive sidebar, and semi-transparent glassmorphic cards (`backdrop-filter: blur(12px)`).
- **Theme Switcher**: Supported using global CSS variables and local storage persistence.
- **Visual Performance**: SVG-based stroke-dasharray animation for the circular countdown timer to ensure fluid frame rates without rendering lag.
- **Bell Chime**: We will use a dual-approach—a generated tone using the HTML5 Web Audio API Synthesizer (which requires zero asset files and plays flawlessly) backed by a classic chime file fallback.

### 3. Productivity Score & Streak Mechanics
- **Productivity Score Formula**: `FocusMinutes - 2 × Distractions`.
- **Daily Streak Logic**: Upon completing a session:
  - If `last_completed` date is today: Keep current streak.
  - If `last_completed` date is yesterday: Increment `streak` by 1.
  - If `last_completed` date is older: Reset `streak` to 1.
  - Store this metadata in the `User` table to avoid querying aggregate records on every page load.

### 4. RESTful Routing & Blueprints
To keep the code clean and maintainable, routes are segmented into logical modules:
- `/auth`: Registration, Login, Logout.
- `/dashboard`: Analytics overview, streak info, recent sessions list, quotes.
- `/session`: Timer, active session states, distraction clicks, and reflections.
- `/history`: CSV export, full list, search/filter endpoints.

## Risks / Trade-offs

- **[Risk] Browser Audio Restrictions:** Modern browsers block autoplaying audio unless a user gesture occurs.
  - *Mitigation:* The user triggers a gesture when clicking "Start Focus Session" or interacting with the timer, resolving the browser block.
- **[Risk] State Loss on Page Refresh:** If a user accidentally reloads during a 60-minute session, timer state could be lost.
  - *Mitigation:* We will store the active session start timestamp and countdown duration in `localStorage` so that refreshing the page seamlessly restores and resynchronizes the countdown.
