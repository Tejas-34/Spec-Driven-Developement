import random
from datetime import datetime, date, timedelta
from extensions import db
from models import FocusSession, User

MOCK_TASKS = [
    ("LeetCode Medium Array Problems", "Coding"),
    ("System Design Database Sharding", "Design"),
    ("Read Cal Newport Deep Work", "Study"),
    ("Mock Interview Behavioural Prep", "Revision"),
    ("Implement React Router V6", "Coding"),
    ("Study Operating Systems Virtual Memory", "Study"),
    ("UX Wireframing Dashboard Card UI", "Design"),
    ("Revise DBMS Indexing B-Trees", "Revision"),
    ("LeetCode Hard Dynamic Programming", "Coding"),
    ("Read Chapter 3 of Clean Code", "Study"),
    ("API Error Handler Middleware", "Coding"),
    ("Write System Architecture Specs", "Design")
]

MOCK_NOTES_LEARNED = [
    "Understood how index scans work compared to sequential scans. B-trees reduce lookup time.",
    "Solved the subset sum DP problem by drawing the 2D grid first. Saved 30 minutes of bug hunting.",
    "Cal Newport's theory of attentional residue explains why phone checking kills productivity.",
    "Discovered that Flask extension objects should not be loaded on app instantiation to avoid circular imports.",
    "Learned that rounded margins and dynamic shadows improve the premium feel of glassmorphic panels.",
    "Memorized the four ACID properties and how write-ahead logging (WAL) prevents SQLite locks."
]

MOCK_NOTES_MISTAKES = [
    "Checked phone immediately after starting the timer because of a message notification.",
    "Wrote code without creating tests first, which led to a logic regression on nested values.",
    "Spent too much time designing the color scheme instead of finishing the SQL constraints.",
    "Forgot to handle edge cases where the list returned None."
]

MOCK_NOTES_REVISION = [
    "Re-run sorting benchmarks tomorrow to verify performance benefits.",
    "Practice behavioral STAR method answers: Focus on conflict resolution.",
    "Review dynamic programming space optimization techniques.",
    "Double check database foreign key constraints in Flask migrations."
]

def seed_user_data(user):
    """
    Automatically seeds 18 mock sessions spread across the past 8 days.
    Also calculates and sets a beautiful starting streak for the user.
    """
    # Verify if sessions already exist to prevent duplicate seeding
    if FocusSession.query.filter_by(user_id=user.id).first():
        return
        
    today = date.today()
    total_sessions_created = 0
    
    # We will seed sessions spread over the past 8 days (from 7 days ago to today)
    for day_offset in range(7, -1, -1):
        target_date = today - timedelta(days=day_offset)
        
        # Decide how many sessions to generate on this day
        # Ensure at least 1-3 sessions per day to build a perfect 8-day streak
        sessions_today = random.randint(1, 3)
        if total_sessions_created + sessions_today > 18:
            sessions_today = 18 - total_sessions_created
            if sessions_today <= 0 and day_offset == 0:
                sessions_today = 1 # Ensure at least 1 on the last day for the active streak!
                
        for _ in range(sessions_today):
            task_name, category = random.choice(MOCK_TASKS)
            duration = random.choice([25, 45, 60])
            distractions = random.randint(0, 4)
            score = duration - (2 * distractions)
            
            # Formulate genuine reflection notes
            learned = random.choice(MOCK_NOTES_LEARNED)
            mistakes = random.choice(MOCK_NOTES_MISTAKES)
            revision = random.choice(MOCK_NOTES_REVISION)
            
            # Spread times throughout the day
            hour = random.randint(9, 21)
            minute = random.randint(0, 59)
            session_time = datetime.combine(target_date, datetime.min.time()) + timedelta(hours=hour, minutes=minute)
            
            new_session = FocusSession(
                user_id=user.id,
                title=task_name,
                category=category,
                duration=duration,
                distractions=distractions,
                score=score,
                notes_learned=learned,
                notes_mistakes=mistakes,
                notes_revision=revision,
                status='completed',
                created_at=session_time
            )
            db.session.add(new_session)
            total_sessions_created += 1
            
    # Set User Streak metadata to 8 because we just completed sessions across 8 consecutive days
    user.streak = 8
    user.last_activity_date = today
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
