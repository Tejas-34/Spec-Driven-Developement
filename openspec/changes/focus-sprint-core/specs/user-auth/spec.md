## ADDED Requirements

### Requirement: User Registration
The system SHALL allow a new user to register using an email, username, and password. The system SHALL hash the password prior to saving it in the database and display a success message upon successful registration.

#### Scenario: Successful Registration
- **WHEN** the user provides a unique email, username, password, and matching password confirmation, then submits the registration form
- **THEN** the system SHALL hash the password, save the new user record in the SQLite database, display a success flash message, and redirect the user to the login page

#### Scenario: Registration with Duplicate Email
- **WHEN** the user submits the registration form with an email that is already registered in the system
- **THEN** the system SHALL display an error flash message and prompt the user to try again or log in

### Requirement: User Login
The system SHALL authenticate registered users using their email and password, utilizing Flask-Login for secure session management and persistence.

#### Scenario: Successful Login
- **WHEN** the user submits valid email and password credentials
- **THEN** the system SHALL establish an active session, display a success flash message, and redirect the user to the main dashboard

#### Scenario: Invalid Login Credentials
- **WHEN** the user submits an incorrect email or password
- **THEN** the system SHALL display an error flash message and keep the user on the login page

### Requirement: User Logout
The system SHALL terminate the user's active session upon request.

#### Scenario: Successful Logout
- **WHEN** an authenticated user clicks the logout button
- **THEN** the system SHALL destroy the session, display a success flash message, and redirect the user to the landing page
