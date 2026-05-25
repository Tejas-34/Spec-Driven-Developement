## ADDED Requirements

### Requirement: Theme Toggle
The system SHALL provide a dynamic, persistent toggle that switches between a futuristic dark theme and a clean light theme.

#### Scenario: Swiping Theme Switcher
- **WHEN** the user clicks the theme toggle button
- **THEN** the system SHALL switch the CSS classes on the body element, updating the primary colors, and store the preference in LocalStorage to persist across refreshes

### Requirement: Profile Settings Page
The system SHALL let the user update their profile details (e.g. username, revision goals) or view their total focus achievements.

#### Scenario: Updating Profile Name
- **WHEN** the user modifies their username in the Profile settings and clicks "Save"
- **THEN** the system SHALL validate the input, update the user record in the SQLite database, and flash a success message

### Requirement: Motivational Quotes API
The system SHALL dynamically fetch or display motivational quotes on the dashboard to inspire focus.

#### Scenario: Generating Dashboard Quote
- **WHEN** the dashboard page loads
- **THEN** the system SHALL load a random motivational quote and display it in the header banner
