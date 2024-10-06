import tkinter as tk
from tkinter import messagebox
from crud_operations import view_bets_for_offer, create_bet, update_bet, delete_bet

def open_bets_screen(offer_id):
    # Create the bets window
    bets_window = tk.Toplevel()
    bets_window.title(f"Bets for Offer ID {offer_id}")
    bets_window.geometry("900x600")
    bets_window.configure(bg="#1e1e1e")

    # Heading
    heading_font = ("Eurostile", 20, "bold")
    button_font = ("Arial", 12)
    heading = tk.Label(bets_window, text=f"Bets for Offer ID {offer_id}", font=heading_font, fg="#ffffff", bg="#1e1e1e")
    heading.pack(pady=20)

    # Frame for the bets list
    list_frame = tk.Frame(bets_window, bg="#1e1e1e")
    list_frame.pack(pady=10)

    # Define headers for the bets table
    headers = ["Bet ID", "Settle Datetime", "Status", "Category", "BM Win/Loss", "MB Lose/Win", "Winning Side", "Notes"]
    for col_num, header in enumerate(headers):
        tk.Label(list_frame, text=header, bg="#1e1e1e", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=col_num, padx=5, pady=5)

    # Function to load bets into labels
    def load_bets():
        # Clear previous bets if any
        for widget in list_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget.grid_info()['row'] > 0:
                widget.destroy()

        bets = view_bets_for_offer(offer_id)  # Fetch bets from the database

        if bets:
            for row_num, bet in enumerate(bets, start=1):
                try:
                    # Convert Decimal and datetime types to strings for proper display
                    bet_id = bet['bet_id']
                    settle_datetime = bet['settle_datetime'].strftime('%Y-%m-%d %H:%M:%S')
                    status = bet['status']
                    category = bet['category']
                    bmwinwinloss = str(bet['bmwinwinloss'])
                    mblosewinloss = str(bet['mblosewinloss'])
                    winning_side = bet['winning_side']
                    notes = bet['notes'] if bet['notes'] else ""

                    # Create labels for each piece of data
                    data = [bet_id, settle_datetime, status, category, bmwinwinloss, mblosewinloss, winning_side, notes]
                    for col_num, datum in enumerate(data):
                        tk.Label(list_frame, text=datum, bg="#1e1e1e", fg="white", font=("Arial", 10)).grid(row=row_num, column=col_num, padx=5, pady=5)

                except Exception as e:
                    print(f"Error displaying bet: {e}")
        else:
            print("No bets found for this offer.")
    
    # Load bets on window open
    load_bets()

    # Function to handle creating a new bet
    def create_new_bet():
        def submit_bet():
            settle_datetime = settle_datetime_entry.get()
            status = status_entry.get()
            category = category_entry.get()
            bmwinwinloss = bmwinwinloss_entry.get()
            mblosewinloss = mblosewinloss_entry.get()
            winning_side = winning_side_entry.get()
            notes = notes_entry.get()

            # Ensure required fields are filled
            if settle_datetime and status and category and bmwinwinloss and mblosewinloss and winning_side:
                try:
                    # Call the create_bet function from CRUD
                    create_bet(offer_id, settle_datetime, status, category, float(bmwinwinloss), float(mblosewinloss), winning_side, notes)
                    messagebox.showinfo("Success", "Bet created successfully!")
                    create_bet_window.destroy()  # Close the create bet window
                    load_bets()  # Reload the bets
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create bet: {e}")
            else:
                messagebox.showerror("Error", "Please fill all required fields.")

        # Create a new window for inputting bet details
        create_bet_window = tk.Toplevel(bets_window)
        create_bet_window.title("Create New Bet")
        create_bet_window.geometry("400x400")

        # Form to input bet details
        tk.Label(create_bet_window, text="Settle Datetime:").pack(pady=5)
        settle_datetime_entry = tk.Entry(create_bet_window)
        settle_datetime_entry.pack(pady=5)

        tk.Label(create_bet_window, text="Status:").pack(pady=5)
        status_entry = tk.Entry(create_bet_window)
        status_entry.pack(pady=5)

        tk.Label(create_bet_window, text="Category:").pack(pady=5)
        category_entry = tk.Entry(create_bet_window)
        category_entry.pack(pady=5)

        tk.Label(create_bet_window, text="BM Win/Loss:").pack(pady=5)
        bmwinwinloss_entry = tk.Entry(create_bet_window)
        bmwinwinloss_entry.pack(pady=5)

        tk.Label(create_bet_window, text="MB Lose/Win:").pack(pady=5)
        mblosewinloss_entry = tk.Entry(create_bet_window)
        mblosewinloss_entry.pack(pady=5)

        tk.Label(create_bet_window, text="Winning Side:").pack(pady=5)
        winning_side_entry = tk.Entry(create_bet_window)
        winning_side_entry.pack(pady=5)

        tk.Label(create_bet_window, text="Notes:").pack(pady=5)
        notes_entry = tk.Entry(create_bet_window)
        notes_entry.pack(pady=5)

        submit_button = tk.Button(create_bet_window, text="Submit", command=submit_bet)
        submit_button.pack(pady=20)

    # Function to delete a selected bet
    def delete_selected_bet():
        selected_item = list_frame.grid_slaves(row=1)
        if not selected_item:
            messagebox.showerror("Error", "Please select a bet to delete.")
            return

        bet_id = list_frame.grid_slaves(row=1)[0].cget("text")  # Get the bet ID

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this bet?"):
            delete_bet(bet_id)
            messagebox.showinfo("Success", "Bet deleted successfully!")
            load_bets()  # Reload the bets

    # Buttons for creating and deleting bets
    button_frame = tk.Frame(bets_window, bg="#1e1e1e")
    button_frame.pack(pady=20)

    create_button = tk.Button(button_frame, text="Create New Bet", font=button_font, command=create_new_bet)
    create_button.grid(row=0, column=0, padx=10)

    delete_button = tk.Button(button_frame, text="Delete Selected Bet", font=button_font, command=delete_selected_bet)
    delete_button.grid(row=0, column=1, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    open_bets_screen(1)  # Example usage with offer_id=1
    root.mainloop()
