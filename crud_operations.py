import mysql.connector
from mysql.connector import Error

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
            
            # Return the offers instead of printing them
            return offers
        
        except Error as e:
            print(f"Error: {e}")
            return []
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


# Function to update an existing offer
def update_offer(offer_id, bookmaker=None, category=None, money_in=None, money_out=None, status=None, offer_start_date=None, notes=None):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            updates = []
            params = []
            
            if bookmaker:
                updates.append("bookmaker = %s")
                params.append(bookmaker)
            if category:
                updates.append("category = %s")
                params.append(category)
            if money_in is not None:
                updates.append("money_in = %s")
                params.append(money_in)
            if money_out is not None:
                updates.append("money_out = %s")
                params.append(money_out)
            if status:
                updates.append("status = %s")
                params.append(status)
            if offer_start_date:
                updates.append("offer_start_date = %s")
                params.append(offer_start_date)
            if notes:
                updates.append("notes = %s")
                params.append(notes)
                
            if updates:
                query = f"UPDATE Offers SET {', '.join(updates)} WHERE offer_id = %s"
                params.append(offer_id)
                
                # Expanded Debugging: Print the full query and parameter list
                print(f"Executing Query: {query} with params {params}")
                
                cursor.execute(query, tuple(params))
                connection.commit()

                affected_rows = cursor.rowcount
                if affected_rows > 0:
                    print(f"Offer ID {offer_id} updated successfully.")
                else:
                    print(f"Offer ID {offer_id} not updated. No changes detected or issue with the query.")
            else:
                print("No updates provided for the offer.")
        
        except Error as e:
            print(f"Error during update: {e}")
        
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

def main():
    connection = create_connection()
    

    if connection:
        connection.close()
        print("MySQL connection is closed.")

if __name__ == "__main__":
    main()