## ADDED Requirements

### Requirement: Session History Table
The system SHALL display a paginated or scrollable table of all past sessions, showing the task name, duration, date/time, distraction count, status (completed/abandoned), and productivity score.

#### Scenario: Viewing Session History
- **WHEN** the authenticated user navigates to the History tab/page
- **THEN** the system SHALL retrieve past sessions from SQLite database and render them sorted in reverse chronological order

### Requirement: Search and Filter
The system SHALL provide search inputs and category filters that dynamically filter the displayed session list.

#### Scenario: Searching for a Task
- **WHEN** the user types a keyword into the search bar
- **THEN** the system SHALL display only the sessions matching the task title or description

### Requirement: CSV Data Export
The system SHALL enable users to export all their session records in standard CSV format.

#### Scenario: Exporting CSV
- **WHEN** the user clicks the "Export CSV" button
- **THEN** the backend SHALL generate a CSV file containing all their database session entries and prompt a browser download

### Requirement: Analytics Visualizations
The system SHALL render interactive charts using Chart.js to visualize focus hours, distraction frequencies, and overall productivity trends.

#### Scenario: Loading Analytics Dashboard
- **WHEN** the user navigates to the Analytics page
- **THEN** the system SHALL query aggregate data (e.g., daily focus sums, distraction counts) and render matching bar/line/wave charts using Chart.js
