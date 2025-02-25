from tkinter import messagebox
from CashRegisterApp import CashierApp

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
    def buy():
        # Actualizar historial y stock
        for itemInShoppingCart in CashierApp.shoppingCart:
            productID = CashierApp.shoppingCart[itemInShoppingCart]["productID"]
            purchaseID = CashierApp.shoppingCart[itemInShoppingCart]["purchaseID"]
            name = CashierApp.shoppingCart[itemInShoppingCart]["name"]
            unitPrice = CashierApp.shoppingCart[itemInShoppingCart]["unitPrice"]
            totalItems = CashierApp.shoppingCart[itemInShoppingCart]["totalItems"]
            totalPrice = CashierApp.shoppingCart[itemInShoppingCart]["totalPrice"]

            CashierApp.salesHistory.update({len(CashierApp.salesHistory) + 1: {
                "purchaseID": purchaseID,
                "productID": productID,
                "name": name,
                "unitPrice": unitPrice,
                "totalItems": totalItems,
                "totalPrice": totalPrice
            }})

        CashierApp.purchaseCounter += 1
        CashierApp.shoppingCart = {}

        messagebox.showinfo("Purchase complete", f"Purchase with Receipt ID {purchaseID} completed. Please check the sales history for details.")

    @staticmethod
    def cancelPurchase():
        # Cancelar compra y limpiar el carrito
        CashierApp.shoppingCart = {}
        messagebox.showinfo("Purchase cancelled", f"Purchase has been aborted. Items from shopping card were removed.")