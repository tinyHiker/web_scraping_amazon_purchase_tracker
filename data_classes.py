import sqlite3
import datetime

from exceptions import *

from typing import Optional

class AlreadyBought(Exception):
    """Raised when a customer tries to buy a product that is already bought"""
    def __init__(self):
        message = f"You have already bought this product"
        super().__init__(message)
    
        
        

class User:
    def __init__(self, id: int, name: str, master: Optional[int] = None):
        self.id = id
        self.name = name
        self.master = master
        
        
    def __str__(self):
        return f"User #{self.id} {self.name}"
        
        
    def create_new_user(self, user_name : str):
        """Creates User in the SQLite3 Database and returns associated User object"""
        query = "INSERT INTO users (name, master) VALUES (?, ?)"
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_name, self.id))
            conn.commit()
            new_user_id = cursor.lastrowid
            
        return User(id=new_user_id, name=user_name, master=self.id)
            
    
    def delete_all_products(self):
        query = "DELETE FROM products WHERE user_id = ?"
        
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (self.id, ))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise NoProductsDeleted("You do not have any products registered at the moment")
        return True
    
    def delete_bought_products(self):
        query = "DELETE FROM products WHERE user_id = ? AND bought = ?"
        
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (self.id, 1))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise NoProductsDeleted("You do not have any bought products registered at the moment")
        return True
        
        
    
        
            
        
class Product:
    def __init__(self, *args):
        self.args = args
        self.id: int = args[0] 
        self.name: str = args[1]
        self.price: float = args[2]
        self.bought: int = args[3] #Should be either 0 or 1
        self.user_id: int = args[4]
        self.rating: int = args[5] #Should be between 1 and 10 inclusive
    
    def __str__(self):
        return f"Product #{self.id} {self.name}"
    
    @staticmethod
    def create_new(title: str, final_price: float, date: datetime.date, user: User, rating: int):
        #Create new_entry using SQL
        query = "INSERT INTO products (name, price, user_id, rating) VALUES (?, ?, ?, ?)"
        
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (title, final_price, user.id, rating))   ### Catch exception for when rating is outside of range
            conn.commit()
            print(f"Product '{title}' added successfully with ID {cursor.lastrowid}.")
            
        return Product(*(cursor.lastrowid, title, final_price, 0, user.id, rating))
        
        

    def delete(self):
        # deletes the product entry using the current information of the object  # replace with your database file path
        query = "DELETE FROM products WHERE id = ?"
        
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
              # There is prorbably a built-in exception for when the sql query does not work. should try-catch it as an extra precaution even though we already check for the products existence with find_product()
            cursor.execute(query, (self.id, ))
            conn.commit()
            
        return True
    
    @staticmethod
    def delete_bought_products(user_id: int):
        query = "DELETE FROM products WHERE user_id = ? AND bought = ?"
        
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id, 1))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise NoProductsDeleted("You do not have any bought products registered at the moment")
        return True
        
                
    
    def change_rating(self, score: int):
        #updates rating in the database for this object
        self.rating = score 
        query = "UPDATE products SET rating = ? WHERE id = ?"
        
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (score, self.id))
            conn.commit()
            
        return True
    
    
    def buy(self):
        if self.bought == 0:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                query = "UPDATE products SET bought = ? WHERE id = ?"
                cursor.execute(query, (1, self.id))
                conn.commit()
        else:
            raise AlreadyBought()
    
    
    @staticmethod
    def list_products(user_id: int, bought_lookup: Optional[bool] = None):
        with sqlite3.connect('database.db') as conn:  # This will create a file named 'database.db'
            cursor = conn.cursor()
            if bought_lookup is None:
                query = "SELECT * FROM products"
                cursor.execute(query)
            elif bought_lookup == False:
                query = "SELECT * FROM products WHERE user_id = ? AND bought = ?"
                cursor.execute(query, (user_id, 0))
            else:
                query = "SELECT * FROM products WHERE user_id = ? AND bought = ?"
                cursor.execute(query, (user_id, 1))
                
            results = cursor.fetchall()
        
        return results
    
if __name__ == "__main__":
    pass
    
       