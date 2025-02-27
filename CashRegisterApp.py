import tkinter
from tkinter import ttk
from tkinter import messagebox
from operations import centerWindow, updateSelectedProductLabel

### Obtain product ID from selecction on TreeViewList
# treeViewList.selection()[0]

### Obtain values from TreeViewList
# treeViewList.item(id)['values'][0] --> Name
# treeViewList.item(id)['values'][1] --> Price
# treeViewList.item(id)['values'][2] --> Stock

class CashRegisterApp():
    # Used to identify which items were part of the same purchase
    purchaseID = 1 #purchaseCounter
    
    # Used to store the history of all sells
    salesHistory = {} # Structure will be: {purchaseID: ID, productId: id, name: ProductName, unitPrice: UnitPrice, totalItems: TotalItems, totalPrice: TotalPrice }
    
    # Used to store items added to the shopping card
    shoppingCart = {} # Structure will be: {purchaseID: ID, productId: id, name: ProductName, unitPrice: UnitPrice, totalItems: TotalItems, totalPrice: TotalPrice }

    def openCashRegisterMainWindow(self,listOfProducts): 
        # Opening the app's main window

        # Create Window
        self.cashRegisterAppMainWindow = tkinter.Tk()
        # Set parameters
        self.cashRegisterAppMainWindow.title("Shopping")

        # This will be the size of the Window
        window_width = 600
        window_height = 600

        centerWindow(self.cashRegisterAppMainWindow,window_width,window_height)

        self.labelSelectProductTitle = ttk.Label(self.cashRegisterAppMainWindow,text="Please select a product to shop: ")
        self.labelSelectProductTitle.pack()

        # Adding the TreeView to display the products
        # Doing only this, will create an empty heading
        self.listOfItems = ttk.Treeview(self.cashRegisterAppMainWindow, columns=("Name", "Price", "Stock"), show="headings")
        # It is necessary to add the name of each column
        self.listOfItems.heading("Name", text="Name")
        self.listOfItems.heading("Price", text="Price")
        self.listOfItems.heading("Stock", text="Stock")
        self.listOfItems.pack()

        # Now the Treeview object will be filled with the products information
        for prodID in listOfProducts:
            self.listOfItems.insert("","end",iid=prodID,values=(listOfProducts[prodID]["name"],f"$ {listOfProducts[prodID]["price"]:.2f}",listOfProducts[prodID]["stock"]))
        
        # Label to display the product that will be added to the cart
        self.labelSelectedProduct = ttk.Label(self.cashRegisterAppMainWindow,text="Selected item")
        self.labelSelectedProduct.pack()

        # On button release, the label of selectedProductLabel will be updated with the selected product
        self.listOfItems.bind("<ButtonRelease-1>", lambda event:updateSelectedProductLabel(event,self.listOfItems, self.labelSelectedProduct))

        # Entry to specify the amount of items to be added to the shopping cart
        self.entryAmountToBuy = ttk.Entry(self.cashRegisterAppMainWindow,text="0")
        self.entryAmountToBuy.pack()

        # Button to add product to shopping cart 
        self.buttonAddProduct = ttk.Button(self.cashRegisterAppMainWindow,text="Add item to shopping cart",command=self.addItemToShoppingCart)
        self.buttonAddProduct.pack()

        self.buttonViewShoppingCart = ttk.Button(self.cashRegisterAppMainWindow,text="View shopping cart",command=self.openShoppingCartWindow)
        self.buttonViewShoppingCart.pack()

        self.buttonViewSalesHistory = ttk.Button(self.cashRegisterAppMainWindow,text="View sales history",command=self.openSalesHistoryWindow)
        self.buttonViewSalesHistory.pack()
        
        self.cashRegisterAppMainWindow.mainloop()

    def addItemToShoppingCart(self):
        # The class variable "shoppingCart" will be updated with this method

        # Obtain the selected product's ID
        id = self.listOfItems.selection()[0]

        # Obtain product's name
        name = self.listOfItems.item(id)['values'][0]

        # Obtain product's price
        priceStr = self.listOfItems.item(id)['values'][1]
        price = float(priceStr[2:len(priceStr)])

        # Obtain total items to buy
        totalItems = int(self.entryAmountToBuy.get())

        # Add item to the Shopping Cart
        self.updateShoppingCart(id, name, price, totalItems)
        
        # Update View Shopping Cart button
        self.buttonViewShoppingCart['text'] = f"View shopping cart ({len(CashRegisterApp.shoppingCart)})"

    def openShoppingCartWindow(self):
        # Open a new window with the shopping cart's contents

        self.shoppingCartWindow = tkinter.Tk()
        self.shoppingCartWindow.title("Shopping Cart Info")

        # This will be the size of the Window
        window_width = 500
        window_height = 400

        centerWindow(self.shoppingCartWindow,window_width,window_height)

        self.listOfItemsShoppingCart = ttk.Treeview(self.shoppingCartWindow, columns=("Name", "Amount", "Total_Price"), show="headings")
        # It is necessary to add the name of each column
        self.listOfItemsShoppingCart.heading("Name", text="Name")
        self.listOfItemsShoppingCart.heading("Amount", text="Amount")
        self.listOfItemsShoppingCart.heading("Total_Price", text="Total Price")
        
        self.listOfItemsShoppingCart.pack()

        for product in CashRegisterApp.shoppingCart:
            self.listOfItemsShoppingCart.insert("","end",iid=product,values=(CashRegisterApp.shoppingCart[product]["name"],CashRegisterApp.shoppingCart[product]["totalItems"],f"$ {CashRegisterApp.shoppingCart[product]["totalPrice"]:.2f}"))
        
        self.buttonConfirmPurchase = ttk.Button(self.shoppingCartWindow,text="Buy", command=self.buy)
        self.buttonConfirmPurchase.pack()

        self.buttonCancelPurchase = ttk.Button(self.shoppingCartWindow,text="Cancel", command=self.cancelPurchase)
        self.buttonCancelPurchase.pack()

        self.shoppingCartWindow.mainloop()

    def buy(self):
        
        # Sales history has to be updated
        for itemInShoppingCart in CashRegisterApp.shoppingCart:
            productID, purchaseID, name, unitPrice, totalItems, totalPrice = self.obtainItemFromShoppingCart(itemInShoppingCart)
            self.updateSalesHistory(productID, purchaseID, name, unitPrice, totalItems, totalPrice)
            
            # Stock has to be updated in the table
            currentStock = self.listOfItems.item(productID)['values'][2] # <--- CurrentStock
            self.listOfItems.item(productID, values=(name,f"$ {unitPrice:.2f}",currentStock-totalItems))

        # Purchase ID has to be updated    
        CashRegisterApp.purchaseID += 1
        
        # Shopping cart has to be cleaned.
        CashRegisterApp.shoppingCart = {}
        
        # View Shopping cart button has to be updated
        self.buttonViewShoppingCart['text'] = "View shopping cart"
        
        # Shopping cart window has to be closed
        self.shoppingCartWindow.destroy()
        messagebox.showinfo("Purchase complete", f"Purchase with Receipt ID {purchaseID} completed. Please check the sales history for details.")

        # Pending: show receipt details


    def cancelPurchase(self):
        
        # Shopping cart has to be cleaned.
        CashRegisterApp.shoppingCart = {}

        # View Shopping cart button has to be updated
        self.buttonViewShoppingCart['text'] = "View shopping cart"
        
        # Shopping cart window has to be closed
        self.shoppingCartWindow.destroy()

        messagebox.showinfo("Purchase cancelled", f"Purchase has been aborted. Items from shopping card were removed.")
        
        
    def openSalesHistoryWindow(self):

        # Pending, create separate funcion for this
        salesHistoryStrings = []
        salesHistoryStrings.append("----------------------")
        salesHistoryStrings.append("Receipt ID - Product - Unit Price - Total Items - Total Price")
        for itemInSaleHistory in CashRegisterApp.salesHistory:
            productID, purchaseID, name, unitPrice, totalItems, totalPrice = self.obtainItemFromSalesHistory(itemInSaleHistory)
            salesHistoryStrings.append(f"\n{purchaseID} - {name} - {unitPrice} - {totalItems} - {totalPrice}")
        salesHistoryStrings.append("\n----------------------")
        
        self.salesHistoryWindow = tkinter.Tk()
        self.salesHistoryWindow.title("Sales History Information")

        # This will be the size of the Window
        window_width = 500
        window_height = 400

        centerWindow(self.salesHistoryWindow,window_width,window_height)

        self.textSalesHistoryText = tkinter.Label(self.salesHistoryWindow, text=salesHistoryStrings)
        self.textSalesHistoryText.pack()

        self.buttonOkSales = ttk.Button(self.salesHistoryWindow,text="Ok", command=self.salesHistoryWindow.destroy)
        self.buttonOkSales.pack()

        self.salesHistoryWindow.mainloop()

    @classmethod
    def obtainItemFromShoppingCart(cls, id):
        productID = CashRegisterApp.shoppingCart[id]["productID"]
        purchaseID = CashRegisterApp.shoppingCart[id]["purchaseID"]
        name = CashRegisterApp.shoppingCart[id]["name"]
        unitPrice = CashRegisterApp.shoppingCart[id]["unitPrice"]
        totalItems = CashRegisterApp.shoppingCart[id]["totalItems"]
        totalPrice = CashRegisterApp.shoppingCart[id]["totalPrice"]
        return productID, purchaseID, name, unitPrice, totalItems, totalPrice
    
    @classmethod
    def obtainItemFromSalesHistory(cls, id):
        productID = CashRegisterApp.salesHistory[id]["productID"]
        purchaseID = CashRegisterApp.salesHistory[id]["purchaseID"]
        name = CashRegisterApp.salesHistory[id]["name"]
        unitPrice = CashRegisterApp.salesHistory[id]["unitPrice"]
        totalItems = CashRegisterApp.salesHistory[id]["totalItems"]
        totalPrice = CashRegisterApp.salesHistory[id]["totalPrice"]
        return productID, purchaseID, name, unitPrice, totalItems, totalPrice

    @classmethod
    def updateShoppingCart(cls, id, name: str, price: float, totalItems: int):
        # Method to add elements to the shopping cart
        CashRegisterApp.shoppingCart.update({len(CashRegisterApp.shoppingCart)+1:{
            "purchaseID": CashRegisterApp.purchaseID,
            "productID": id,
            "name": name,
            "unitPrice": price,
            "totalItems": totalItems,
            "totalPrice": totalItems * price
        }})

    @classmethod
    def updateSalesHistory(cls, productID, purchaseID, name, unitPrice, totalItems, totalPrice):
        CashRegisterApp.salesHistory.update({(len(CashRegisterApp.salesHistory)+1):{
                 "purchaseID": purchaseID, 
                 "productID": productID,
                 "name": name, 
                 "unitPrice": unitPrice, 
                 "totalItems": totalItems, 
                 "totalPrice": totalPrice 
             }})