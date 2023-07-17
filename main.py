# A simple application meant to hold you responsible to work targets you set.
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox
import datetime
from plyer import notification
import uuid

from data import get_stats, get_settings, set_settings, get_current_session, set_current_session, end_current_session, reset_current_session

class AimAssessAccomplish(tk.Frame):
    def __init__(self, root, master=None):
        super().__init__(master)
        self.root = root
        self.root.title("Aim Assess Achieve")
        logo_small = tk.PhotoImage(file = 'aim_assess_achieve_logo_small.png')
        self.root.iconphoto(False, logo_small)
        self.root.geometry("1500x1000")

        # Toggle between light and dark mode
        self.root.tk.call("source", "azure.tcl")
        self.root.tk.call("set_theme", "dark")

        # Creating the notebook widget
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Creating the frames for the notebook
        self.session_tab = ttk.Frame(self.notebook)
        self.stats_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)

        # Adding the frames to the notebook
        self.notebook.add(self.session_tab, text="Session")
        self.notebook.add(self.stats_tab, text="Stats")
        self.notebook.add(self.settings_tab, text="Settings")

        # Get Data from data.py
        current_session = get_current_session()
        all_stats = get_stats()
        all_settings = get_settings()

        # Creating the widgets for the Session frame
        self.met_goal = tk.IntVar()
        self.default_session_gui()

        # Creating the widgets for the Stats frame
        self.name = ttk.Label(self.stats_tab, text="Aim Assess Achieve", font=('Helvetica', 20, 'bold', 'underline'))
        self.name.pack(pady=10)

        self.stats_label = ttk.Label(self.stats_tab, text="Stats:", font=('Helvetica', 16, 'bold'))
        self.stats_label.pack(pady=10)

        self.sessions_completed = ttk.Label(self.stats_tab, text=f"Number of sessions completed: {all_stats['sessions_completed']}", font=('Helvetica', 12, 'bold'))
        self.sessions_completed.pack(pady=(0, 20))

        self.goal_met = ttk.Label(self.stats_tab, text=f"Number of times target goal met: {all_stats['goals_met']}", font=('Helvetica', 12, 'bold'))
        self.goal_met.pack(pady=20)

        self.longest_streak = ttk.Label(self.stats_tab, text=f"Longest streak of sessions completed with target goal met: {all_stats['longest_streak']}", font=('Helvetica', 12, 'bold'))
        self.longest_streak.pack(pady=20)

        self.current_streak = ttk.Label(self.stats_tab, text=f"Current streak of sessions completed with target goal met: {all_stats['current_streak']}", font=('Helvetica', 12, 'bold'))
        self.current_streak.pack(pady=20)

        # Creating the widgets for the Settings frame
        self.name = ttk.Label(self.settings_tab, text="Aim Assess Achieve", font=('Helvetica', 20, 'bold', 'underline'))
        self.name.pack(pady=10)

        self.settings_label = ttk.Label(self.settings_tab, text="Settings:", font=('Helvetica', 16, 'bold'))
        self.settings_label.pack(pady=10)

        self.session_time_default = ttk.Label(self.settings_tab, text="Set the default session time in mins:", font=('Helvetica', 12))
        self.session_time_default.pack(pady=10)

        self.session_time_default_entry = ttk.Entry(self.settings_tab, width=15, justify=tk.CENTER)
        self.session_time_default_entry.insert(0, all_settings['session_time'])
        self.session_time_default_entry.pack(pady=(0, 30))

        self.break_time_default = ttk.Label(self.settings_tab, text="Set the default break time in mins:", font=('Helvetica', 12))
        self.break_time_default.pack(pady=10)

        self.break_time_default_entry = ttk.Entry(self.settings_tab, width=15, justify=tk.CENTER)
        self.break_time_default_entry.insert(0, all_settings['break_time'])
        self.break_time_default_entry.pack(pady=(0, 30))

        self.notify_time_default = ttk.Label(self.settings_tab, text="Set the default notification update in mins:", font=('Helvetica', 12))
        self.notify_time_default.pack(pady=10)

        self.notify_time_default_entry = ttk.Entry(self.settings_tab, width=15, justify=tk.CENTER)
        self.notify_time_default_entry.insert(0, all_settings['notification_time'])
        self.notify_time_default_entry.pack(pady=(0, 10))

        self.save_settings_btn = ttk.Button(self.settings_tab, text="Save Settings", command=self.save_settings)
        self.save_settings_btn.pack(pady=(5, 30))

        self.theme_select = ttk.Label(self.settings_tab, text="Choose Theme:", font=('Helvetica', 12))
        self.theme_select.pack(pady=10)
        # Change the theme of the application
        self.theme_button = ttk.Button(self.settings_tab, text="Toggle Light/Dark Mode", command=self.toggle_mode)
        self.theme_button.pack(pady=5)

        # Creating the menu bar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.session_id = str(uuid.uuid4())

        # If the user has a current session, then update the session tab to show the current session.
        if current_session['session_start_time']:
            self.target_goal = current_session['target_goal']
            self.session_time = int(current_session['session_end_time'] - current_session['session_start_time'])
            self.time_remaining = int(current_session['session_end_time'] - datetime.datetime.now().timestamp())
            if self.time_remaining <= 0:
                self.time_remaining = 0
            if current_session['is_break']:
                self.start_break(auto=True)
            else:
                self.start_session(auto=True)


    def reset_session_gui(self):
        # Remove all the widgets from the session tab
        for widget in self.session_tab.winfo_children():
            widget.destroy()


    def timer_gui(self, is_break=False):
        self.reset_session_gui()

        # Generate an id
        self.session_id = str(uuid.uuid4())

        self.name = ttk.Label(self.session_tab, text="Aim Assess Achieve", font=('Helvetica', 20, 'bold', 'underline'))
        self.name.pack(pady=10)

        self.settings_label = ttk.Label(self.session_tab, text="Session in Progress:" if not is_break else "Taking a Break!", font=('Helvetica', 16, 'bold'))
        self.settings_label.pack(pady=10)

        # Time Remaining for the session
        self.time_remaining_lbl = ttk.Label(self.session_tab, text="Time Remaining:", font=('Helvetica', 12, 'bold'))
        self.time_remaining_lbl.pack(pady=(10, 0))

        self.time_remaining_val = ttk.Label(self.session_tab, text=f"{self.format_time_remaining()}", font=('Helvetica', 12))
        self.time_remaining_val.pack(pady=10)

        # Add a clock progress bar
        self.clock = ttk.Progressbar(self.session_tab, orient=tk.HORIZONTAL, length=1000, mode='determinate')
        self.clock.pack(pady=(10, 30))
        time_percent = (self.session_time - self.time_remaining) / self.session_time
        self.clock['value'] = time_percent * 100

        # Show the target goal underneath
        self.session_target = ttk.Label(self.session_tab, text=f"Target Goal:", font=('Helvetica', 12, 'bold'))
        self.session_target.pack(pady=(10, 0))

        self.session_target_val = ttk.Label(self.session_tab, text=f"{self.target_goal}", font=('Helvetica', 12))
        self.session_target_val.pack(pady=10)

        # With a button to end the session early.
        self.end_session_btn = ttk.Button(self.session_tab, text=f"End {'Break' if is_break else 'Session'} Early", command=self.end_session_gui)
        self.end_session_btn.pack(pady=10)

        # Start the timer
        self.update_clock(self.session_id)

        # Start the notification timer
        self.update_notifications(self.session_id)


    def start_session(self, auto=False):
        # When the start session button is clicked, then remove all the widgets from the session tab and add a clock progress bar. Show the target goal underneath. With a button to end the session early.
        # Remove all the widgets from the session tab
        if not auto:
            self.target_goal = self.session_target_entry.get()
            self.session_time = round(float(self.session_timer_entry.get()) * 60)
            self.time_remaining = self.session_time

            # Update the session
            set_current_session(self.target_goal, datetime.datetime.now() + datetime.timedelta(seconds=self.session_time), False)

        # Create the timer GUI
        self.timer_gui()


    def end_session_gui(self):
        # Ask the user if they met their target goal
        # Ask for their focus level
        # Disable the end session button
        current_session = get_current_session()
        if current_session['is_break']:
            self.notify("Aim Assess Achieve", "Your break has ended.")
            self.end_session()
        else:
            self.notify("Aim Assess Achieve", "Your session has ended. Please assess your progress.")
            self.end_session_btn['state'] = 'disabled'

            self.end_session_window = tk.Toplevel(self.root)
            self.end_session_window.title("End Session")
            self.end_session_window.geometry("500x500")
            self.name = ttk.Label(self.end_session_window, text="Aim Assess Achieve", font=('Helvetica', 20, 'bold', 'underline'))
            self.name.pack(pady=10)

            self.settings_label = ttk.Label(self.end_session_window, text="Session Ended", font=('Helvetica', 16, 'bold'))
            self.settings_label.pack(pady=10)

            self.end_session_lbl = ttk.Label(self.end_session_window, text="Did you meet your target goal?", font=('Helvetica', 16, 'bold'))
            self.end_session_lbl.pack(pady=10)

            self.end_session_goal = ttk.Label(self.end_session_window, text=f"Goal: {self.target_goal}", font=('Helvetica', 12, 'bold'))
            self.end_session_goal.pack(pady=10)

            self.check_button = ttk.Checkbutton(self.end_session_window, text="Yes", variable=self.met_goal)
            self.check_button.pack(pady=10)

            self.focus_level_lbl = ttk.Label(self.end_session_window, text="What was your focus level (1-10)?", font=('Helvetica', 16, 'bold'))
            self.focus_level_lbl.pack(pady=10)

            self.focus_level_entry = ttk.Entry(self.end_session_window, width=15, justify=tk.CENTER)
            self.focus_level_entry.pack(pady=(10, 30))

            self.continue_button = ttk.Button(self.end_session_window, text="Continue", command=self.end_session)
            self.continue_button.pack(pady=10)
            self.break_button = ttk.Button(self.end_session_window, text="Take a Break", command=self.start_break)
            self.break_button.pack(pady=10)


    def update_session(self):
        # Update the stats
        current_session = get_current_session()
        if not current_session['is_break']:
            end_current_session(bool(self.met_goal.get()), int(self.focus_level_entry.get()) if self.focus_level_entry.get() else None)

            # Close the end session window
            self.end_session_window.destroy()
        else:
            reset_current_session()

        # Reset the session_id
        self.session_id = str(uuid.uuid4())


    def end_session(self):
        # Add the current session to the session history and update the stats
        self.update_session()

        # Reset the session tab
        self.reset_session_gui()
        self.default_session_gui()


    def default_session_gui(self):
        all_settings = get_settings()
        self.name = ttk.Label(self.session_tab, text="Aim Assess Achieve", font=('Helvetica', 20, 'bold', 'underline'))
        self.name.pack(pady=10)

        self.session_label = ttk.Label(self.session_tab, text="Session:", font=('Helvetica', 16, 'bold'))
        self.session_label.pack(pady=10)

        self.session_target = ttk.Label(self.session_tab, text="Set a target goal:", font=('Helvetica', 12))
        self.session_target.pack(pady=10)

        self.session_target_entry = ttk.Entry(self.session_tab, width=150, justify=tk.CENTER)
        self.session_target_entry.pack(pady=(0, 30))

        self.session_timer = ttk.Label(self.session_tab, text="Set a timer in mins:", font=('Helvetica', 12))
        self.session_timer.pack(pady=10)

        self.session_timer_entry = ttk.Entry(self.session_tab, width=15, justify=tk.CENTER)
        self.session_timer_entry.insert(0, all_settings['session_time'])
        self.session_timer_entry.pack(pady=(0, 5))

        self.start_session_btn = ttk.Button(self.session_tab, text="Start Session", command=self.start_session)
        self.start_session_btn.pack(pady=10)


    def start_break(self, reset=False, auto=False):
        if not auto:
            # Add the current session to the session history and update the stats
            self.update_session()

            # Set the target goal and session time
            all_settings = get_settings()
            self.target_goal = 'Take a Break!'
            self.session_time = round(all_settings['break_time'] * 60)
            self.time_remaining = self.session_time

            # Update the session
            set_current_session(self.target_goal, datetime.datetime.now() + datetime.timedelta(seconds=self.session_time), True)

        # Create the timer GUI
        self.timer_gui(is_break=True)
        

    def format_time_remaining(self):
        # Format the time to be in the format of mm:ss
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        if seconds < 10:
            seconds = f"0{seconds}"
        return f"{minutes}:{seconds}"


    def update_clock(self, id):
        # Check if the session has been ended
        if self.session_id != id:
            return

        # Update the clock progress bar
        time_percent = (self.session_time - self.time_remaining) / self.session_time
        try:
            self.clock['value'] = time_percent * 100
            self.time_remaining -= 1
            self.time_remaining_val['text'] = self.format_time_remaining()
            if self.time_remaining > 0:
                self.root.after(1000, self.update_clock, id)
            else:
                self.end_session_gui()
        except tk.TclError:
            pass


    def update_notifications(self, id):
        # Check if the session has been ended
        if self.session_id != id:
            return
        
        all_settings = get_settings()
        msg = f"Time remaining: {self.format_time_remaining()}"
        self.notify("Aim Assess Achieve", msg)
        if self.time_remaining > 0:
            self.root.after(int(all_settings['notification_time']*60*1000), self.update_notifications, id)


    def save_settings(self):
        set_settings(self.session_time_default_entry.get(), self.break_time_default_entry.get(), self.notify_time_default_entry.get())


    def notify(self, title, message):
        notification.notify(
            title=title,
            message=message,
            timeout=10  # The notification will automatically close after 10 seconds
        )


    def toggle_mode(self):
        # NOTE: The theme's real name is azure-<mode>
        if self.root.tk.call("ttk::style", "theme", "use") == "azure-dark":
            # Set light theme
            self.root.tk.call("set_theme", "light")
        else:
            # Set dark theme
            self.root.tk.call("set_theme", "dark")


def main():
    root = tk.Tk()
    app = AimAssessAccomplish(root)
    root.mainloop()


if __name__ == '__main__':
    main()