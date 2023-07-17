# A simple application meant to hold you responsible to work targets you set.
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox

from data import get_stats, recalculate_stats, get_settings, set_settings, get_current_session, set_current_session, reset_current_session

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
        all_stats = get_stats()
        all_settings = get_settings()

        # Creating the widgets for the Session frame
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

        # Make field number only
        self.session_timer_entry = ttk.Entry(self.session_tab, width=15, justify=tk.CENTER)
        self.session_timer_entry.insert(0, all_settings['session_time'])
        self.session_timer_entry.pack(pady=(0, 30))

        self.start_session_btn = ttk.Button(self.session_tab, text="Start Session", command=self.start_session)
        self.start_session_btn.pack(pady=30)

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
        self.break_time_default_entry.pack(pady=(0, 10))

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

    def start_session(self):
        # When the start session button is clicked, then remove all the widgets from the session tab and add a clock progress bar. Show the target goal underneath. With a button to end the session early.
        # Remove all the widgets from the session tab
        self.target_goal = self.session_target_entry.get()
        self.session_time = round(float(self.session_timer_entry.get()) * 60)
        self.time_remaining = self.session_time

        for widget in self.session_tab.winfo_children():
            widget.destroy()

        self.name = ttk.Label(self.session_tab, text="Aim Assess Achieve", font=('Helvetica', 20, 'bold', 'underline'))
        self.name.pack(pady=10)

        self.settings_label = ttk.Label(self.session_tab, text="Session in Progress:", font=('Helvetica', 16, 'bold'))
        self.settings_label.pack(pady=10)

        # Time Remaining for the session
        self.time_remaining_lbl = ttk.Label(self.session_tab, text="Time Remaining:", font=('Helvetica', 12, 'bold'))
        self.time_remaining_lbl.pack(pady=(10, 0))

        self.time_remaining_val = ttk.Label(self.session_tab, text=f"{self.format_time_remaining()}", font=('Helvetica', 12))
        self.time_remaining_val.pack(pady=10)

        # Add a clock progress bar
        self.clock = ttk.Progressbar(self.session_tab, orient=tk.HORIZONTAL, length=1000, mode='determinate')
        self.clock.pack(pady=(10, 30))

        # Show the target goal underneath
        self.session_target = ttk.Label(self.session_tab, text=f"Target Goal:", font=('Helvetica', 12, 'bold'))
        self.session_target.pack(pady=(10, 0))

        self.session_target_val = ttk.Label(self.session_tab, text=f"{self.target_goal}", font=('Helvetica', 12))
        self.session_target_val.pack(pady=10)

        # With a button to end the session early.
        self.end_session_btn = ttk.Button(self.session_tab, text="End Session", command=self.end_session)
        self.end_session_btn.pack(pady=10)

        # Start the timer
        self.update_clock()

    def end_session(self):
        # Ask the user if they met their target goal
        # Ask for their focus level
        # Update the stats
        # Ask if they want to take a break or start a new session
        # If they want to take a break, then start a break session
        # Else reset the session tab
        pass

    def start_break(self):
        pass

    def end_break(self):
        pass

    def format_time_remaining(self):
        # Format the time to be in the format of mm:ss
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        return f"{minutes}:{seconds}"

    def update_clock(self):
        # Update the clock progress bar
        time_percent = (self.session_time - self.time_remaining) / self.session_time
        self.clock['value'] = time_percent * 100
        self.time_remaining -= 1
        self.time_remaining_val['text'] = self.format_time_remaining()
        if self.time_remaining > 0:
            self.root.after(1000, self.update_clock)

    def save_settings(self):
        set_settings(self.session_time_default_entry.get(), self.break_time_default_entry.get())

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
