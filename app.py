import json
import os

class Product:
    def __init__(self, product_id, name, quantity):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
    
    def convert_to_dict(self):
        return {"product_id": self.product_id, "name": self.name, "quantity": self.quantity}
    
    @staticmethod
    def read_from_dict(data):
        return Product(data["product_id"], data["name"], data["quantity"])

class InventoryManager:
    INVENTORY_FILE = "inventorydb.json"
    
    def __init__(self):
        self.inventory = self.load_inventory_db()
    
    def load_inventory_db(self):
        #load the json database 
        if not os.path.exists(self.INVENTORY_FILE):
            return {}
        with open(self.INVENTORY_FILE, "r") as file:
            data = json.load(file)
            return {pid: Product.read_from_dict(details) for pid, details in data.items()}
    
    def save_inventory(self):
        with open(self.INVENTORY_FILE, "w") as file:
            json.dump({pid: product.convert_to_dict() for pid, product in self.inventory.items()}, file, indent=4)

    def check_if_number(self, prompt):
        while True:
            value = input(prompt)
            if value.isdigit():
                return int(value)
            else:
                print("--> Invalid input! Please enter a valid number.")
    
    def create_new_product(self):
        product_id = self.check_if_number("Enter Product ID (only number): ")
        
        product_id = str(product_id)
        if product_id in self.inventory:
            print("--> Product already exists!")
        else:
            name = input("Enter Product Name: ")
            quantity = self.check_if_number("Enter Initial Quantity: ")
            self.inventory[product_id] = Product(product_id, name, quantity)
            self.save_inventory()
            print("--> Product added successfully!")
    
    def add_product_qty(self):
        product_id = self.check_if_number("Enter Product ID: ")
        product_id = str(product_id)
        if product_id in self.inventory:
            quantity = self.check_if_number("Enter Quantity to Add: ")
            self.inventory[product_id].quantity += quantity
            self.save_inventory()
            print("--> Stock updated successfully!")
        else:
            print("--> Product not found!")
    
    def reduce_product_qty(self):
        product_id = self.check_if_number("Enter Product ID: ")
        product_id = str(product_id)

        if product_id in self.inventory:
            quantity = self.check_if_number("Enter Quantity to Reduce: ")
            if self.inventory[product_id].quantity >= quantity:
                self.inventory[product_id].quantity -= quantity
                self.save_inventory()
                print("--> Stock reduced successfully!")
            else:
                print("--> Not enough stock!")
        else:
            print("--> Product not found!")
    
    def check_product_stock(self):
        product_id = self.check_if_number("Enter Product ID: ")
        product_id = str(product_id)
        
        if product_id in self.inventory:
            product = self.inventory[product_id]
            print(f"--> Product: {product.name}, Quantity: {product.quantity}")
        else:
            print("--> Product not found!")
    
    def display_products(self):
        if not self.inventory:
            print("--> No products in the Inventory!")
        else:
            print("\nProducts in the Inventory:")
            for product in self.inventory.values():
                print(f"ID: {product.product_id}, Name: {product.name}, Quantity: {product.quantity}")
    
    def menu(self):
        while True:
            print("\n:: Inventory Management System ::")
            print(" ")
            print("* To continue, please choose from menus *")
            print(" ")
            print("1. Create a Product")
            print("2. Add Product to Inventory")
            print("3. Reduce Product Qty")
            print("4. Check Product Stock")
            print("5. Products List")
            print("6. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                self.create_new_product()
            elif choice == "2":
                self.add_product_qty()
            elif choice == "3":
                self.reduce_product_qty()
            elif choice == "4":
                self.check_product_stock()
            elif choice == "5":
                self.display_products()
            elif choice == "6":
                print("Thank you. See you soon!")
                break
            else:
                print("Invalid menu! Please try again")

if __name__ == "__main__":
    inventory_manager = InventoryManager()
    inventory_manager.menu()