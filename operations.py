from tkinter import messagebox
from CashRegisterApp import CashierApp
from products import listOfProducts 


class CashierAppOperations:
    @staticmethod
    def addItemToShoppingCart(id, price, amount, selectedProductLabel):
        CashierApp.shoppingCart.update({len(CashierApp.shoppingCart) + 1: {
            "purchaseID": CashierApp.purchaseCounter,
            "productID": id,
            "name": selectedProductLabel['text'],
            "unitPrice": price,
            "totalItems": int(amount),
            "totalPrice": float(amount) * price
        }})

    @staticmethod
    def buy(self):
        print("Buying")
        
        print("History has to be updated")
        print("\nStock has to be updated (processing)")

        for itemInShoppingCart in CashierApp.shoppingCart:
            productID = CashierApp.shoppingCart[itemInShoppingCart]["productID"]
            purchaseID = CashierApp.shoppingCart[itemInShoppingCart]["purchaseID"]
            name = CashierApp.shoppingCart[itemInShoppingCart]["name"]
            unitPrice = CashierApp.shoppingCart[itemInShoppingCart]["unitPrice"]
            totalItems = CashierApp.shoppingCart[itemInShoppingCart]["totalItems"]
            totalPrice = CashierApp.shoppingCart[itemInShoppingCart]["totalPrice"]
            CashierApp.salesHistory.update({(len(CashierApp.salesHistory)+1):{
                 "purchaseID": purchaseID, 
                 "productID": productID,
                 "name": name, 
                 "unitPrice": unitPrice, 
                 "totalItems": totalItems, 
                 "totalPrice": totalPrice 
             }})
            print(f"Receipt: {CashierApp.shoppingCart[itemInShoppingCart]["purchaseID"]} - ID: {CashierApp.shoppingCart[itemInShoppingCart]["productID"]} - {CashierApp.shoppingCart[itemInShoppingCart]["name"]} - {CashierApp.shoppingCart[itemInShoppingCart]["unitPrice"]} - {CashierApp.shoppingCart[itemInShoppingCart]["totalItems"]} - {CashierApp.shoppingCart[itemInShoppingCart]["totalPrice"]}")
            print(f"Current stock: {listOfProducts[int(productID)]["stock"]}")
            print(f"Total items to buy: {totalItems}")
            currentStock = self.items.item(productID)['values'][2] # <--- CurrentStock
            self.items.item(productID, values=(name,f"$ {unitPrice:.2f}",currentStock-totalItems))
            
        print("\nCashierApp.purchaseCounter has to be updated")
        CashierApp.purchaseCounter += 1
        print(f"New purchaseCounter: {CashierApp.purchaseCounter}")

        print("\nself.shoppingCart has to be cleaned")
        CashierApp.shoppingCart = {}
        self.viewShoppingCartButton['text'] = "View shopping cart"
        print(CashierApp.shoppingCart)

        print("\Close window")
        self.viewShoppingCartWindow.destroy()
        messagebox.showinfo("Purchase complete", f"Purchase with Receipt ID {purchaseID} completed. Please check the sales history for details.")

    @staticmethod
    def cancelPurchase():
        # Cancelar compra y limpiar el carrito
        CashierApp.shoppingCart = {}
        messagebox.showinfo("Purchase cancelled", f"Purchase has been aborted. Items from shopping card were removed.")