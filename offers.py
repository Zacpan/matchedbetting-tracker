import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from crud_operations import create_offer, view_offers, update_offer, delete_offer
from bets import open_bets_screen

def open_offers_screen(main_window=None):
    offers_window = tk.Toplevel()
    offers_window.title("Offers")
    offers_window.geometry("900x600")
    offers_window.configure(bg="#1e1e1e")

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", 
                    background="#333333",
                    foreground="white",
                    rowheight=25,
                    fieldbackground="#333333",
                    font=("Arial", 10))
    style.map("Treeview", 
              background=[('selected', '#0057e7')],
              foreground=[('selected', 'white')])

    style.configure("Treeview.Heading", 
                    background="#0057e7", 
                    foreground="white", 
                    font=("Arial", 12, "bold"))

    if main_window:
        main_window.withdraw()

    heading_font = ("Eurostile", 20, "bold")
    button_font = ("Arial", 12)
    heading = tk.Label(offers_window, text="Manage Offers", font=heading_font, fg="#ffffff", bg="#1e1e1e")
    heading.pack(pady=20)

    columns = ["offer_id", "bookmaker", "category", "money_in", "money_out", "status", "offer_start_date", "notes"]
    tree = ttk.Treeview(offers_window, columns=columns, show="headings", height=15)

    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=100)

    tree.pack(pady=10)

    scrollbar = ttk.Scrollbar(offers_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def load_offers():
        tree.delete(*tree.get_children())
        offers = view_offers()

        if offers:
            for offer in offers:
                try:
                    offer_id = offer['offer_id']
                    bookmaker = offer['bookmaker']
                    category = offer['category']
                    money_in = str(offer['money_in'])
                    money_out = str(offer['money_out'])
                    status = offer['status']
                    offer_start_date = offer['offer_start_date'].strftime('%Y-%m-%d %H:%M:%S')
                    notes = offer['notes'] if offer['notes'] else ""

                    tree.insert("", "end", values=(offer_id, bookmaker, category, money_in, money_out, status, offer_start_date, notes))

                except Exception as e:
                    print(f"Error displaying offer: {e}")
        else:
            print("No offers found.")

    def auto_refresh():
        load_offers()
        offers_window.after(5000, auto_refresh)

    load_offers()
    offers_window.after(5000, auto_refresh)

    def create_new_offer():
        def submit_offer():
            bookmaker = bookmaker_entry.get()
            category = category_combobox.get()
            money_in = money_in_entry.get()
            money_out = money_out_entry.get()
            status = status_combobox.get()
            offer_date = offer_start_date_entry.get_date().strftime('%Y-%m-%d')
            offer_time = f"{hour_combobox.get()}:{minute_combobox.get()}:00"
            offer_start_datetime = f"{offer_date} {offer_time}"
            notes = notes_entry.get()

            if bookmaker and category and money_in and status and offer_start_datetime:
                try:
                    create_offer(bookmaker, category, float(money_in), float(money_out or 0), status, offer_start_datetime, notes)
                    messagebox.showinfo("Success", "Offer created successfully!")
                    create_offer_window.destroy()
                    load_offers()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create offer: {e}")
            else:
                messagebox.showerror("Error", "Please fill all required fields.")

        create_offer_window = tk.Toplevel()
        create_offer_window.title("Create New Offer")
        create_offer_window.geometry("400x550")

        tk.Label(create_offer_window, text="Bookmaker:").pack(pady=5)
        bookmaker_entry = tk.Entry(create_offer_window)
        bookmaker_entry.pack(pady=5)

        tk.Label(create_offer_window, text="Category:").pack(pady=5)
        category_combobox = ttk.Combobox(create_offer_window, values=["sports_signup", "casino_signup", "sports_reload", "casino_reload", "other"], state="readonly")
        category_combobox.pack(pady=5)

        tk.Label(create_offer_window, text="Money In:").pack(pady=5)
        money_in_entry = tk.Entry(create_offer_window)
        money_in_entry.pack(pady=5)

        tk.Label(create_offer_window, text="Money Out (optional):").pack(pady=5)
        money_out_entry = tk.Entry(create_offer_window)
        money_out_entry.pack(pady=5)

        tk.Label(create_offer_window, text="Status:").pack(pady=5)
        status_combobox = ttk.Combobox(create_offer_window, values=["sign_up/livechat", "active", "complete"], state="readonly")
        status_combobox.pack(pady=5)

        tk.Label(create_offer_window, text="Offer Start Date:").pack(pady=5)
        offer_start_date_entry = DateEntry(create_offer_window, date_pattern='yyyy-mm-dd', state="readonly")
        offer_start_date_entry.pack(pady=5)

        tk.Label(create_offer_window, text="Offer Start Time:").pack(pady=5)
        time_frame = tk.Frame(create_offer_window)
        time_frame.pack(pady=5)

        hour_combobox = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(24)], width=3, state="readonly")
        hour_combobox.set("12")
        hour_combobox.pack(side="left", padx=5)

        tk.Label(time_frame, text=":").pack(side="left")

        minute_combobox = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(60)], width=3, state="readonly")
        minute_combobox.set("00")
        minute_combobox.pack(side="left", padx=5)

        tk.Label(create_offer_window, text="Notes:").pack(pady=5)
        notes_entry = tk.Entry(create_offer_window)
        notes_entry.pack(pady=5)

        submit_button = tk.Button(create_offer_window, text="Submit", command=submit_offer)
        submit_button.pack(pady=20)

    def update_selected_offer():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an offer to update.")
            return

        selected_offer = tree.item(selected_item)['values']
        offer_id = selected_offer[0]

        def submit_update():
            bookmaker = bookmaker_entry.get()
            category = category_combobox.get()
            money_in = money_in_entry.get()
            money_out = money_out_entry.get()
            status = status_combobox.get()
            offer_date = offer_start_date_entry.get_date().strftime('%Y-%m-%d')
            offer_time = f"{hour_combobox.get()}:{minute_combobox.get()}:00"
            offer_start_datetime = f"{offer_date} {offer_time}"
            notes = notes_entry.get()

            if bookmaker and category and money_in and offer_start_datetime:
                try:
                    update_offer(offer_id, bookmaker=bookmaker, category=category, money_in=float(money_in), money_out=float(money_out or 0), status=status, offer_start_date=offer_start_datetime, notes=notes)
                    messagebox.showinfo("Success", "Offer updated successfully!")
                    update_offer_window.destroy()
                    load_offers()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update offer: {e}")
            else:
                messagebox.showerror("Error", "Please fill all required fields.")

        update_offer_window = tk.Toplevel(offers_window)
        update_offer_window.title("Update Offer")
        update_offer_window.geometry("400x550")

        tk.Label(update_offer_window, text="Bookmaker:").pack(pady=5)
        bookmaker_entry = tk.Entry(update_offer_window)
        bookmaker_entry.insert(0, selected_offer[1])
        bookmaker_entry.pack(pady=5)

        tk.Label(update_offer_window, text="Category:").pack(pady=5)
        category_combobox = ttk.Combobox(update_offer_window, values=["sports_signup", "casino_signup", "sports_reload", "casino_reload", "other"], state="readonly")
        category_combobox.set(selected_offer[2])
        category_combobox.pack(pady=5)

        tk.Label(update_offer_window, text="Money In:").pack(pady=5)
        money_in_entry = tk.Entry(update_offer_window)
        money_in_entry.insert(0, selected_offer[3])
        money_in_entry.pack(pady=5)

        tk.Label(update_offer_window, text="Money Out:").pack(pady=5)
        money_out_entry = tk.Entry(update_offer_window)
        money_out_entry.insert(0, selected_offer[4])
        money_out_entry.pack(pady=5)

        tk.Label(update_offer_window, text="Status:").pack(pady=5)
        status_combobox = ttk.Combobox(update_offer_window, values=["sign_up/livechat", "active", "complete"], state="readonly")
        status_combobox.set(selected_offer[5])
        status_combobox.pack(pady=5)

        tk.Label(update_offer_window, text="Offer Start Date:").pack(pady=5)
        offer_start_date_entry = DateEntry(update_offer_window, date_pattern='yyyy-mm-dd', state="readonly")
        offer_start_date_entry.set_date(selected_offer[6].split()[0])
        offer_start_date_entry.pack(pady=5)

        tk.Label(update_offer_window, text="Offer Start Time:").pack(pady=5)
        time_frame = tk.Frame(update_offer_window)
        time_frame.pack(pady=5)

        offer_start_time = selected_offer[6].split()[1].split(':')
        hour_combobox = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(24)], width=3, state="readonly")
        hour_combobox.set(offer_start_time[0])
        hour_combobox.pack(side="left", padx=5)

        tk.Label(time_frame, text=":").pack(side="left")

        minute_combobox = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(60)], width=3, state="readonly")
        minute_combobox.set(offer_start_time[1])
        minute_combobox.pack(side="left", padx=5)

        tk.Label(update_offer_window, text="Notes:").pack(pady=5)
        notes_entry = tk.Entry(update_offer_window)
        notes_entry.insert(0, selected_offer[7])
        notes_entry.pack(pady=5)

        submit_button = tk.Button(update_offer_window, text="Submit", command=submit_update)
        submit_button.pack(pady=20)

    def delete_selected_offer():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an offer to delete.")
            return

        offer_id = tree.item(selected_item)['values'][0]

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this offer?"):
            delete_offer(offer_id)
            messagebox.showinfo("Success", "Offer deleted successfully!")
            load_offers()

    def open_bets_for_offer():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an offer to view bets.")
            return

        offer_id = tree.item(selected_item)['values'][0]
        open_bets_screen(offer_id)

    def go_back():
        offers_window.destroy()
        if main_window:
            main_window.deiconify()

    button_frame = tk.Frame(offers_window, bg="#1e1e1e")
    button_frame.pack(pady=20)

    create_button = tk.Button(button_frame, text="Create New Offer", font=button_font, command=create_new_offer)
    create_button.grid(row=0, column=0, padx=10)

    update_button = tk.Button(button_frame, text="Update Selected Offer", font=button_font, command=update_selected_offer)
    update_button.grid(row=0, column=1, padx=10)

    delete_button = tk.Button(button_frame, text="Delete Selected Offer", font=button_font, command=delete_selected_offer)
    delete_button.grid(row=0, column=2, padx=10)

    bets_button = tk.Button(button_frame, text="View Bets", font=button_font, command=open_bets_for_offer)
    bets_button.grid(row=0, column=3, padx=10)

    back_button = tk.Button(button_frame, text="Back", font=button_font, command=go_back)
    back_button.grid(row=0, column=4, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    open_offers_screen(root)
    root.mainloop()
