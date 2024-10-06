import tkinter as tk
from tkinter import messagebox
from crud_operations import create_offer, view_offers, update_offer, delete_offer
from bets import open_bets_screen 

def open_offers_screen(main_window=None):
    offers_window = tk.Toplevel()
    offers_window.title("Offers")
    offers_window.geometry("900x600")
    offers_window.configure(bg="#1e1e1e")

    if main_window:
        main_window.withdraw()

    heading_font = ("Eurostile", 20, "bold")
    button_font = ("Arial", 12)
    heading = tk.Label(offers_window, text="Manage Offers", font=heading_font, fg="#ffffff", bg="#1e1e1e")
    heading.pack(pady=20)

    list_frame = tk.Frame(offers_window, bg="#1e1e1e")
    list_frame.pack(pady=10)

    headers = ["Offer ID", "Bookmaker", "Category", "Money In", "Money Out", "Status", "Offer Start Date", "Notes", "Bets"]
    for col_num, header in enumerate(headers):
        tk.Label(list_frame, text=header, bg="#1e1e1e", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=col_num, padx=5, pady=5)

    def load_offers():
        for widget in list_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget.grid_info()['row'] > 0:
                widget.destroy()

        offers = view_offers()

        if offers:
            for row_num, offer in enumerate(offers, start=1):
                try:
                    offer_id = offer['offer_id']
                    bookmaker = offer['bookmaker']
                    category = offer['category']
                    money_in = str(offer['money_in'])
                    money_out = str(offer['money_out'])
                    status = offer['status']
                    offer_start_date = offer['offer_start_date'].strftime('%Y-%m-%d %H:%M:%S')
                    notes = offer['notes'] if offer['notes'] else ""

                    data = [offer_id, bookmaker, category, money_in, money_out, status, offer_start_date, notes]
                    for col_num, datum in enumerate(data):
                        tk.Label(list_frame, text=datum, bg="#1e1e1e", fg="white", font=("Arial", 10)).grid(row=row_num, column=col_num, padx=5, pady=5)

                    bets_button = tk.Button(list_frame, text="View Bets", command=lambda o_id=offer_id: open_bets_screen(o_id), bg="#0057e7", fg="white", font=("Arial", 10))
                    bets_button.grid(row=row_num, column=len(headers)-1, padx=5, pady=5)

                except Exception as e:
                    print(f"Error displaying offer: {e}")
        else:
            print("No offers found.")

    load_offers()

    def create_new_offer():
        def submit_offer():
            bookmaker = bookmaker_entry.get()
            category = category_entry.get()
            money_in = money_in_entry.get()
            money_out = money_out_entry.get()
            status = status_entry.get()
            offer_start_date = offer_start_date_entry.get()
            notes = notes_entry.get()

            if bookmaker and category and money_in and status and offer_start_date:
                try:
                    create_offer(bookmaker, category, float(money_in), float(money_out or 0), status, offer_start_date, notes)
                    messagebox.showinfo("Success", "Offer created successfully!")
                    create_offer_window.destroy()
                    load_offers()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create offer: {e}")
            else:
                messagebox.showerror("Error", "Please fill all required fields.")

        create_offer_window = tk.Toplevel(offers_window)
        create_offer_window.title("Create New Offer")
        create_offer_window.geometry("400x400")

        tk.Label(create_offer_window, text="Bookmaker:").pack(pady=5)
        bookmaker_entry = tk.Entry(create_offer_window)
        bookmaker_entry.pack(pady=5)

        tk.Label(create_offer_window, text="Category:").pack(pady=5)
        category_entry = tk.Entry(create_offer_window)
        category_entry.pack(pady=5)

        tk.Label(create_offer_window, text="Money In:").pack(pady=5)
        money_in_entry = tk.Entry(create_offer_window)
        money_in_entry.pack(pady=5)

        tk.Label(create_offer_window, text="Money Out (optional):").pack(pady=5)
        money_out_entry = tk.Entry(create_offer_window)
        money_out_entry.pack(pady=5)

        tk.Label(create_offer_window, text="Status:").pack(pady=5)
        status_entry = tk.Entry(create_offer_window)
        status_entry.pack(pady=5)

        tk.Label(create_offer_window, text="Offer Start Date:").pack(pady=5)
        offer_start_date_entry = tk.Entry(create_offer_window)
        offer_start_date_entry.pack(pady=5)

        tk.Label(create_offer_window, text="Notes:").pack(pady=5)
        notes_entry = tk.Entry(create_offer_window)
        notes_entry.pack(pady=5)

        submit_button = tk.Button(create_offer_window, text="Submit", command=submit_offer)
        submit_button.pack(pady=20)

    def update_selected_offer():
        selected_item = list_frame.grid_slaves(row=1)
        if not selected_item:
            messagebox.showerror("Error", "Please select an offer to update.")
            return

        offer_id = list_frame.grid_slaves(row=1)[0].cget("text")  # Get the offer ID
        offer_details = [widget.cget("text") for widget in list_frame.grid_slaves(row=1)]

        def submit_update():
            bookmaker = bookmaker_entry.get()
            category = category_entry.get()
            money_in = money_in_entry.get()
            money_out = money_out_entry.get()
            status = status_entry.get()
            offer_start_date = offer_start_date_entry.get()
            notes = notes_entry.get()

            update_offer(offer_id, status=status, money_out=float(money_out or 0))
            messagebox.showinfo("Success", "Offer updated successfully!")
            update_offer_window.destroy()
            load_offers() 

        update_offer_window = tk.Toplevel(offers_window)
        update_offer_window.title("Update Offer")
        update_offer_window.geometry("400x400")

        tk.Label(update_offer_window, text="Bookmaker:").pack(pady=5)
        bookmaker_entry = tk.Entry(update_offer_window)
        bookmaker_entry.insert(0, offer_details[1])
        bookmaker_entry.pack(pady=5)

        tk.Label(update_offer_window, text="Category:").pack(pady=5)
        category_entry = tk.Entry(update_offer_window)
        category_entry.insert(0, offer_details[2])
        category_entry.pack(pady=5)

        tk.Label(update_offer_window, text="Money In:").pack(pady=5)
        money_in_entry = tk.Entry(update_offer_window)
        money_in_entry.insert(0, offer_details[3])
        money_in_entry.pack(pady=5)

        tk.Label(update_offer_window, text="Money Out:").pack(pady=5)
        money_out_entry = tk.Entry(update_offer_window)
        money_out_entry.insert(0, offer_details[4])
        money_out_entry.pack(pady=5)

        tk.Label(update_offer_window, text="Status:").pack(pady=5)
        status_entry = tk.Entry(update_offer_window)
        status_entry.insert(0, offer_details[5])
        status_entry.pack(pady=5)

        tk.Label(update_offer_window, text="Offer Start Date:").pack(pady=5)
        offer_start_date_entry = tk.Entry(update_offer_window)
        offer_start_date_entry.insert(0, offer_details[6])
        offer_start_date_entry.pack(pady=5)

        tk.Label(update_offer_window, text="Notes:").pack(pady=5)
        notes_entry = tk.Entry(update_offer_window)
        notes_entry.insert(0, offer_details[7])
        notes_entry.pack(pady=5)

        submit_button = tk.Button(update_offer_window, text="Submit", command=submit_update)
        submit_button.pack(pady=20)


    def delete_selected_offer():
        selected_item = list_frame.grid_slaves(row=1)
        if not selected_item:
            messagebox.showerror("Error", "Please select an offer to delete.")
            return

        offer_id = list_frame.grid_slaves(row=1)[0].cget("text")

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this offer?"):
            delete_offer(offer_id)
            messagebox.showinfo("Success", "Offer deleted successfully!")
            load_offers()


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

    back_button = tk.Button(button_frame, text="Back", font=button_font, command=go_back)
    back_button.grid(row=0, column=3, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    open_offers_screen(root)
