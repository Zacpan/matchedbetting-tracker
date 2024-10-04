import mysql.connector
from mysql.connector import Error

# Function to connect to the database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='MatchedBetting'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to create a new offer
def create_offer(bookmaker, category, money_in, money_out, status, offer_start_date, notes=""):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO Offers (bookmaker, category, money_in, money_out, status, offer_start_date, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (bookmaker, category, money_in, money_out, status, offer_start_date, notes))
            connection.commit()
            print("Offer created successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Function to create a new bet
def create_bet(offer_id, settle_datetime, status, category, bmwinwinloss, mblosewinloss, winning_side, notes=""):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO Bets (offer_id, settle_datetime, status, category, bmwinwinloss, mblosewinloss, winning_side, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (offer_id, settle_datetime, status, category, bmwinwinloss, mblosewinloss, winning_side, notes))
            connection.commit()
            print("Bet created successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Example Usage:
#create_offer('Bet365', 'sports_signup', 100.00, 0.00, 'active', '2024-10-04 12:00:00', 'Initial offer for Bet365')
#create_bet(1, '2024-10-05 14:30:00', 'placed', 'qual_bet', 50.00, -50.00, 'bookmaker', 'First qualifying bet')


# Function to retrieve and display all offers
def view_offers(status=None, category=None):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM Offers"
            params = []
            
            # Adding filters based on status and category if provided
            if status or category:
                query += " WHERE"
                if status:
                    query += " status = %s"
                    params.append(status)
                if category:
                    if status:
                        query += " AND"
                    query += " category = %s"
                    params.append(category)
            
            cursor.execute(query, tuple(params))
            offers = cursor.fetchall()
            
            if offers:
                print("Offers:")
                for offer in offers:
                    print(offer)
            else:
                print("No offers found with the given criteria.")
        
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Function to retrieve and display all bets for a specific offer
def view_bets_for_offer(offer_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM Bets WHERE offer_id = %s"
            cursor.execute(query, (offer_id,))
            bets = cursor.fetchall()
            
            if bets:
                print(f"Bets for Offer ID {offer_id}:")
                for bet in bets:
                    print(bet)
            else:
                print(f"No bets found for Offer ID {offer_id}.")
        
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Example Usage:
#view_offers(status='active', category='sports_signup')
#view_bets_for_offer(1)


# Function to update an existing offer
def update_offer(offer_id, status=None, money_out=None, notes=None):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            updates = []
            params = []
            
            if status:
                updates.append("status = %s")
                params.append(status)
            if money_out is not None:
                updates.append("money_out = %s")
                params.append(money_out)
            if notes:
                updates.append("notes = %s")
                params.append(notes)
                
            if updates:
                query = f"UPDATE Offers SET {', '.join(updates)} WHERE offer_id = %s"
                params.append(offer_id)
                cursor.execute(query, tuple(params))
                connection.commit()
                
                print(f"Offer ID {offer_id} updated successfully.")
            else:
                print("No updates provided for the offer.")
        
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Function to update an existing bet
def update_bet(bet_id, status=None, bmwinwinloss=None, mblosewinloss=None, notes=None):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            updates = []
            params = []
            
            if status:
                updates.append("status = %s")
                params.append(status)
            if bmwinwinloss is not None:
                updates.append("bmwinwinloss = %s")
                params.append(bmwinwinloss)
            if mblosewinloss is not None:
                updates.append("mblosewinloss = %s")
                params.append(mblosewinloss)
            if notes:
                updates.append("notes = %s")
                params.append(notes)
                
            if updates:
                query = f"UPDATE Bets SET {', '.join(updates)} WHERE bet_id = %s"
                params.append(bet_id)
                cursor.execute(query, tuple(params))
                connection.commit()
                
                print(f"Bet ID {bet_id} updated successfully.")
            else:
                print("No updates provided for the bet.")
        
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Example Usage:
update_offer(1, status='complete', money_out=150.00, notes='Offer completed successfully.')
update_bet(1, status='completed', bmwinwinloss=20.00, mblosewinloss=-20.00, notes='Bet settled.')



# Function to delete an offer and its associated bets
def delete_offer(offer_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            delete_query = "DELETE FROM Offers WHERE offer_id = %s"
            cursor.execute(delete_query, (offer_id,))
            connection.commit()
            print(f"Offer ID {offer_id} and its associated bets have been deleted.")
        
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Function to delete a specific bet
def delete_bet(bet_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            delete_query = "DELETE FROM Bets WHERE bet_id = %s"
            cursor.execute(delete_query, (bet_id,))
            connection.commit()
            print(f"Bet ID {bet_id} has been deleted.")
        
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Example Usage:
delete_offer(1)  # Deletes offer with offer_id 1 and all its associated bets
delete_bet(1)    # Deletes bet with bet_id 1


def main():
    # Create the connection
    connection = create_connection()
    
    # Perform any database operations here
    # For now, just close the connection
    if connection:
        connection.close()
        print("MySQL connection is closed.")

if __name__ == "__main__":
    main()