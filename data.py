# Data Controller for AimAssessAccomplish
import json
import os

# Check if stats file exists, if not create it
if not os.path.isfile('stats.json'):
    with open('stats.json', 'w') as stats_file:
        json.dump({'sessions_completed': 0, 'goals_met': 0, 'longest_streak': 0, 'current_streak': 0}, stats_file)

# Check if settings file exists, if not create it
if not os.path.isfile('settings.json'):
    with open('settings.json', 'w') as settings_file:
        json.dump({'session_time': 30, 'break_time': 10}, settings_file)

# Check if current_session file exists, if not create it
if not os.path.isfile('current_session.json'):
    with open('current_session.json', 'w') as current_session_file:
        json.dump({'target_goal': '', 'session_end_time': ''}, current_session_file)


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

def recalculate_stats(new_session, new_goal_met):
    stats['sessions_completed'] = stats['sessions_completed'] + 1
    if new_goal_met:
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

def set_settings(new_session_time, new_break_time):
    settings['session_time'] = new_session_time
    settings['break_time'] = new_break_time
    with open('settings.json', 'w') as settings_file:
        json.dump(settings, settings_file)

def get_current_session():
    return current_session

def set_current_session(new_target_goal, new_session_end_time):
    current_session['target_goal'] = new_target_goal
    current_session['session_end_time'] = new_session_end_time
    with open('current_session.json', 'w') as current_session_file:
        json.dump(current_session, current_session_file)

def reset_current_session():
    current_session['target_goal'] = ''
    current_session['session_end_time'] = ''
    with open('current_session.json', 'w') as current_session_file:
        json.dump(current_session, current_session_file)
