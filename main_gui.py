import tkinter as tk
from tkinter import messagebox
import pygame  
from offers import open_offers_screen

def open_offers():
    open_offers_screen() 

def open_stats():
    messagebox.showinfo("Navigation", "This will open the Stats screen.")

def open_settings():
    messagebox.showinfo("Navigation", "This will open the Settings screen.")

def play_background_music():
    pygame.mixer.init()
    pygame.mixer.music.load("menu_theme.mp3")
    pygame.mixer.music.play(loops=-1)

def create_main_screen():
    root = tk.Tk()
    root.title("Matched Betting Tracker - Version 0.2")
    root.geometry("700x500")
    root.configure(bg="#1e1e1e") 

    play_background_music()


    heading_font = ("Eurostile", 24, "bold")
    button_font = ("Arial", 14, "bold")

    heading = tk.Label(root, text="Matched Betting Tracker", font=heading_font, fg="#ffffff", bg="#1e1e1e")
    heading.pack(pady=30)

    def on_enter(e, button):
        button['background'] = '#0057e7'
        button['foreground'] = 'white'

    def on_leave(e, button):
        button['background'] = '#0f0f0f'
        button['foreground'] = '#f0f0f0'

    button_frame = tk.Frame(root, bg="#1e1e1e")
    button_frame.pack(pady=10)

    offers_button = tk.Button(button_frame, text="Offers", width=20, height=2, bg="#0f0f0f", fg="#f0f0f0", font=button_font, bd=0, relief="flat", command=open_offers)
    offers_button.bind("<Enter>", lambda e: on_enter(e, offers_button))
    offers_button.bind("<Leave>", lambda e: on_leave(e, offers_button))
    offers_button.pack(pady=10)
    

    stats_button = tk.Button(button_frame, text="Stats", width=20, height=2, bg="#0f0f0f", fg="#f0f0f0", font=button_font, bd=0, relief="flat", command=open_stats)
    stats_button.bind("<Enter>", lambda e: on_enter(e, stats_button))
    stats_button.bind("<Leave>", lambda e: on_leave(e, stats_button))
    stats_button.pack(pady=10)

    settings_button = tk.Button(button_frame, text="Settings", width=20, height=2, bg="#0f0f0f", fg="#f0f0f0", font=button_font, bd=0, relief="flat", command=open_settings)
    settings_button.bind("<Enter>", lambda e: on_enter(e, settings_button))
    settings_button.bind("<Leave>", lambda e: on_leave(e, settings_button))
    settings_button.pack(pady=10)

    footer = tk.Label(root, text="© 2024 Matched Betting Tracker", font=("Arial", 10), fg="#f0f0f0", bg="#1e1e1e")
    footer.pack(side="bottom", pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_main_screen()
