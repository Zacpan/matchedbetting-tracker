import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def open_offers():
    messagebox.showinfo("Navigation", "This will open the Offers screen.")

def open_stats():
    messagebox.showinfo("Navigation", "This will open the Stats screen.")

def open_settings():
    messagebox.showinfo("Navigation", "This will open the Settings screen.")

def create_main_screen():
    # Create the main window
    root = tk.Tk()
    root.title("Matched Betting Tracker - GT4 Style")
    root.geometry("600x400")
    root.configure(bg="#1e1e1e")  # Dark background

    # Set custom font styles
    heading_font = ("Eurostile", 24, "bold")  # Eurostile-like font
    button_font = ("Arial", 14, "bold")

    # Add a heading label with a futuristic font
    heading = tk.Label(root, text="Matched Betting Tracker", font=heading_font, fg="#ffffff", bg="#1e1e1e")
    heading.pack(pady=30)

    # Define button hover effect
    def on_enter(e, button):
        button['background'] = '#0057e7'
        button['foreground'] = 'white'

    def on_leave(e, button):
        button['background'] = '#0f0f0f'
        button['foreground'] = '#f0f0f0'

    # Frame for buttons (aligning them in the center)
    button_frame = tk.Frame(root, bg="#1e1e1e")
    button_frame.pack(pady=10)

    # Add buttons with dark theme and hover effect
    offers_button = tk.Button(button_frame, text="Offers", width=20, height=2, bg="#0f0f0f", fg="#f0f0f0", font=button_font, bd=0, relief="flat")
    offers_button.bind("<Enter>", lambda e: on_enter(e, offers_button))
    offers_button.bind("<Leave>", lambda e: on_leave(e, offers_button))
    offers_button.pack(pady=10)

    stats_button = tk.Button(button_frame, text="Stats", width=20, height=2, bg="#0f0f0f", fg="#f0f0f0", font=button_font, bd=0, relief="flat")
    stats_button.bind("<Enter>", lambda e: on_enter(e, stats_button))
    stats_button.bind("<Leave>", lambda e: on_leave(e, stats_button))
    stats_button.pack(pady=10)

    settings_button = tk.Button(button_frame, text="Settings", width=20, height=2, bg="#0f0f0f", fg="#f0f0f0", font=button_font, bd=0, relief="flat")
    settings_button.bind("<Enter>", lambda e: on_enter(e, settings_button))
    settings_button.bind("<Leave>", lambda e: on_leave(e, settings_button))
    settings_button.pack(pady=10)

    # Add a footer message like in GT4
    footer = tk.Label(root, text="© 2024 Matched Betting Tracker", font=("Arial", 10), fg="#f0f0f0", bg="#1e1e1e")
    footer.pack(side="bottom", pady=20)

    # Run the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    create_main_screen()
