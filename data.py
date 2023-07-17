# Data Controller for AimAssessAccomplish
import json
import os
import datetime

# Check if stats file exists, if not create it
if not os.path.isfile('stats.json'):
    with open('stats.json', 'w') as stats_file:
        json.dump({'sessions_completed': 0, 'goals_met': 0, 'longest_streak': 0, 'current_streak': 0}, stats_file)

# Check if settings file exists, if not create it
if not os.path.isfile('settings.json'):
    with open('settings.json', 'w') as settings_file:
        json.dump({'session_time': 30, 'break_time': 10, 'notification_time': 5}, settings_file)

# Check if current_session file exists, if not create it
if not os.path.isfile('current_session.json'):
    with open('current_session.json', 'w') as current_session_file:
        json.dump({'target_goal': '', 'session_start_time': None, 'session_end_time': None, 'is_break': False}, current_session_file)


# Read all files
with open('stats.json', 'r') as stats_file:
    stats = json.load(stats_file)

with open('settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

with open('current_session.json', 'r') as current_session_file:
    current_session = json.load(current_session_file)

# Make getters and setters for all data
def get_stats():
    return stats

def recalculate_stats(goal_met):
    stats['sessions_completed'] = stats['sessions_completed'] + 1
    if goal_met:
        stats['goals_met'] = stats['goals_met'] + 1
        stats['current_streak'] = stats['current_streak'] + 1
        if stats['current_streak'] > stats['longest_streak']:
            stats['longest_streak'] = stats['current_streak']
    else:
        stats['current_streak'] = 0
    with open('stats.json', 'w') as stats_file:
        json.dump(stats, stats_file)

def get_settings():
    return settings

def set_settings(new_session_time, new_break_time, new_notification_time):
    settings['session_time'] = float(new_session_time)
    settings['break_time'] = float(new_break_time)
    settings['notification_time'] = float(new_notification_time)
    with open('settings.json', 'w') as settings_file:
        json.dump(settings, settings_file)

def get_current_session():
    return current_session

def set_current_session(new_target_goal, new_session_end_time, new_is_break):
    current_session['target_goal'] = new_target_goal
    current_session['session_start_time'] = int(datetime.datetime.now().timestamp())
    current_session['session_end_time'] = int(new_session_end_time.timestamp())
    current_session['is_break'] = new_is_break
    with open('current_session.json', 'w') as current_session_file:
        json.dump(current_session, current_session_file)

def end_current_session(goal_met, focus_level):
    # Save session data to all_sessions folder
    # Check that all sessions folder exists, if not create it
    if not os.path.isdir('all_sessions'):
        os.mkdir('all_sessions')

    # Name the file so it starts with the date and time of the session
    session_start_time = datetime.datetime.fromtimestamp(current_session['session_start_time'])
    session_start_time_string = session_start_time.strftime('%Y-%m-%d_%H-%M-%S')
    
    # Create the file
    with open('all_sessions/' + session_start_time_string + '.json', 'w') as session_file:
        session_copy = current_session.copy()
        session_copy['goal_met'] = goal_met
        session_copy['focus_level'] = focus_level
        json.dump(session_copy, session_file)

    # Update stats
    recalculate_stats(goal_met)

    # Reset current session
    reset_current_session()

def reset_current_session():
    current_session['target_goal'] = ''
    current_session['session_start_time'] = ''
    current_session['session_end_time'] = ''
    current_session['is_break'] = False
    with open('current_session.json', 'w') as current_session_file:
        json.dump(current_session, current_session_file)
