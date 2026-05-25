## ADDED Requirements

### Requirement: Session Creation
The system SHALL allow authenticated users to create a focus session by specifying a task title, category (e.g., Study, Coding, Revision, Design), duration (25, 45, 60 minutes, or custom), and description.

#### Scenario: Creating a Session
- **WHEN** the user selects or enters valid session details and clicks "Start Session"
- **THEN** the system SHALL initialize the focus session database entry and redirect the user to the active timer page

### Requirement: Live Timer Control
The system SHALL display an active circular progress ring and countdown timer, allowing the user to start, pause, resume, and reset the timer.

#### Scenario: Starting and Pausing Timer
- **WHEN** the user clicks "Start" or presses the 'S' key, and then clicks "Pause" or presses the 'P' key
- **THEN** the system SHALL transition the countdown state and visually pause/resume the countdown and progress ring

#### Scenario: Completing Timer
- **WHEN** the countdown reaches zero
- **THEN** the system SHALL play a digital bell chime sound and transition the state to "Completed", redirecting the user to the post-session reflection form

### Requirement: Distraction Tracking
The system SHALL provide an interactive "I Got Distracted" button and increment the distractions count for the session on each click/keyboard press.

#### Scenario: Tracking Distraction
- **WHEN** the user clicks the "I Got Distracted" button or presses the 'D' key during an active session
- **THEN** the system SHALL increment the distraction count by 1 and visually flash an alert/sound to remind the user to re-focus

### Requirement: Reflection & Productivity Score
Upon completing a session, the system SHALL prompt the user for post-session notes (learned, mistakes, revisions) and calculate the Productivity Score defined as: `Score = FocusMinutes - 2 * Distractions`.

#### Scenario: Submitting Reflection
- **WHEN** the user submits the reflection form with their notes
- **THEN** the system SHALL compute the productivity score, save the notes and score in the database, and redirect the user to the dashboard

### Requirement: Daily Streak Calculation
The system SHALL track consecutive daily study activity and increment or reset the streak count depending on active session dates.

#### Scenario: Consecutive Days Streak
- **WHEN** a user completes a focus session on the calendar day immediately following their last completed session
- **THEN** the system SHALL increment their streak by 1

#### Scenario: Missed Day Streak Reset
- **WHEN** a calendar day passes without any completed focus sessions
- **THEN** the system SHALL reset the streak to 0 or 1 upon their next session
