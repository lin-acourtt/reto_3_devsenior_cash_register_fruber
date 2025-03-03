import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter.constants import DISABLED, NORMAL 
from operations import centerWindow, updateSelectedProductLabel, is_valid_number
from exceptions import InvalidNumberInput, InvalidNumberInputHandler, NoProductSelectedError, InsuficientStockError, InsufficientStockErrorHandler

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
    
    # Used to store the total of each purschase
    salesHistoryTotal = {} # Structure will be {purchaseID: ID, total: total}

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

        # Create a tkinter string variable to hold the input value in the entry box for the amount of products
        input_validation = tkinter.StringVar(self.cashRegisterAppMainWindow)

        # Create a validation command that will call is_valid_number
        vcmd = (self.cashRegisterAppMainWindow.register(is_valid_number), '%P')
        
        frameEntry = ttk.Frame(self.cashRegisterAppMainWindow)
        frameEntry.pack(pady=10)
        
        self.labelAmount = ttk.Label(frameEntry, text="amount: ")
        self.labelAmount.grid(row=0, column=0, padx=5)

        # Create the Entry widget with validation        
        self.entryAmountToBuy = ttk.Entry(frameEntry, textvariable=input_validation, validate="key", validatecommand=vcmd)
        self.entryAmountToBuy.grid(row=0, column=1, padx=5)

        # Button to add product to shopping cart 
        self.buttonAddProduct = ttk.Button(self.cashRegisterAppMainWindow,text="Add item to shopping cart",command=self.addItemToShoppingCart)
        self.buttonAddProduct.pack()

        # Button to open a new Window to the shopping cart
        self.buttonViewShoppingCart = ttk.Button(self.cashRegisterAppMainWindow,text="View shopping cart",command=self.openShoppingCartWindow, state=DISABLED)
        self.buttonViewShoppingCart.pack()

        # Button to open a new Window to the see the sales history
        self.buttonViewSalesHistory = ttk.Button(self.cashRegisterAppMainWindow,text="View sales history",command=self.openSalesHistoryWindow, state=DISABLED)
        self.buttonViewSalesHistory.pack()
        
        # Button to exit the application        
        self.buttonExit = ttk.Button(self.cashRegisterAppMainWindow, text="Exit", command=self.exitApplication, style="Exit.TButton")
        self.buttonExit.pack(pady=20)
        
        self.cashRegisterAppMainWindow.mainloop()
        
    def exitApplication(self):
        # Close the main window
        self.cashRegisterAppMainWindow.destroy() 

    def addItemToShoppingCart(self):
        
        try:     
            selected_item = self.listOfItems.selection()

            if not selected_item:
                # messagebox.showerror("no product(s) selected", "Please, select a product before adding to the shopping cart .")
                raise NoProductSelectedError("no product(s) selected", "Please, select a product before adding to the shopping cart.")

            # Obtain the selected product's ID
            id = selected_item[0]

            # Check if the same item is already in the shopping cart
            try:
                totalItems = CashRegisterApp.shoppingCart[id]['totalItems']
            except:
                # If the item is not in the shopping cart, consider its initial amount as 0
                totalItems = 0
            
            # Obtain product's name
            name = self.listOfItems.item(id)['values'][0]

            # Obtain product's price
            priceStr = self.listOfItems.item(id)['values'][1]
            # Remove the first portion of the string "$ "
            price = float(priceStr[2:len(priceStr)])

            # Obtain the stock value
            stock = int(self.listOfItems.item(id)['values'][2])

            # Calculate the total item to assign to the shopping cart
            totalItems = totalItems + int(self.entryAmountToBuy.get())

            if totalItems > stock:
                raise InsuficientStockError(name, stock)

            if totalItems <= 0:
                messagebox.showerror("Invalid Quantity", "The quantity must be greater than 0.")
                return        

            # Add item to the Shopping Cart
            self.updateShoppingCart(id, name, price, totalItems)

            # Update View Shopping Cart button
            self.buttonViewShoppingCart['text'] = f"View shopping cart ({len(CashRegisterApp.shoppingCart)})"

            # Change state of the button only if the state is disabled
            if (self.buttonViewShoppingCart['state'].string == 'disabled'):
                self.buttonViewShoppingCart['state'] = NORMAL

        except NoProductSelectedError as e:
        # Manejar la excepción de no selección de producto
            InvalidNumberInputHandler(e)
    
        except InvalidNumberInput as e:
        # Manejar la excepción de cantidad inválida
            InvalidNumberInputHandler(e)
        
        except InsuficientStockError  as e:
            InsufficientStockErrorHandler(e)    
            
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
        
        # Add the total price of the items in the shopping cart
        # Add total of last purchase
        purchaseTotal = self.calculateTotalPrice()
        self.listOfItemsShoppingCart.insert("", "end", values=("Total", "", f"$ {purchaseTotal:.2f}"))

        self.buttonConfirmPurchase = ttk.Button(self.shoppingCartWindow,text="Buy", command=self.buy)
        self.buttonConfirmPurchase.pack()

        self.buttonCancelPurchase = ttk.Button(self.shoppingCartWindow,text="Cancel", command=self.cancelPurchase)
        self.buttonCancelPurchase.pack()

        self.shoppingCartWindow.mainloop()

    def buy(self):
        # The string to print the receipt details is created
        receipt_details = []
        
        # Sales history has to be updated
        for itemInShoppingCart in CashRegisterApp.shoppingCart:
            productID, purchaseID, name, unitPrice, totalItems, totalPrice = self.obtainItemFromShoppingCart(itemInShoppingCart)
            self.updateSalesHistory(productID, purchaseID, name, unitPrice, totalItems, totalPrice)
            
            receipt_details.append(f"{name} - $ {unitPrice:.2f} x {totalItems} = $ {totalPrice:.2f}")
            
            # Stock has to be updated in the table
            currentStock = int(self.listOfItems.item(productID)['values'][2]) # <--- CurrentStock
            self.listOfItems.item(productID, values=(name,  f"$ {unitPrice:.2f}",currentStock-totalItems))

        total = self.calculateTotalPrice()
        receipt_message = "\n".join(receipt_details)
        receipt_message += f"\n\nTotal Purchase: ${total:.2f}"
        
        # Update salesHistoryTotal
        self.updateSalesHistoryTotal(purchaseID, total)

        # Change state of View Sales History button
        if (self.buttonViewSalesHistory['state'].string == 'disabled'):
            self.buttonViewSalesHistory['state'] = NORMAL

        # Purchase ID has to be updated    
        CashRegisterApp.purchaseID += 1
        
        # Shopping cart has to be cleaned.
        CashRegisterApp.shoppingCart = {}
        
        # View Shopping cart button has to be updated
        self.buttonViewShoppingCart['text'] = "View shopping cart"

        # Change state of the button
        self.buttonViewShoppingCart['state'] = DISABLED

        # Shopping cart window has to be closed
        self.shoppingCartWindow.destroy()
        # messagebox.showinfo("Purchase complete", f"Purchase with Receipt ID {purchaseID} completed. Please check the sales history for details.")
    
        messagebox.showinfo("Purchase complete", f"Purchase with Receipt ID {CashRegisterApp.purchaseID - 1} completed.\n\n{receipt_message}")

    def calculateTotalPrice(self):
        # Calculate the total cost of the purchase
        total_price = 0.0
        for itemInShoppingCart in CashRegisterApp.shoppingCart:
            item = CashRegisterApp.shoppingCart[itemInShoppingCart]
            total_price += item["totalPrice"]
            
        return total_price

    def cancelPurchase(self):
        
        # Shopping cart has to be cleaned.
        CashRegisterApp.shoppingCart = {}

        # View Shopping cart button has to be updated
        self.buttonViewShoppingCart['text'] = "View shopping cart"

        # Change state of the button
        self.buttonViewShoppingCart['state'] = DISABLED
        
        # Shopping cart window has to be closed
        self.shoppingCartWindow.destroy()

        messagebox.showinfo("Purchase cancelled", f"Purchase has been aborted. Items from shopping card were removed.")
        
        
    def openSalesHistoryWindow(self):

        self.salesHistoryWindow = tkinter.Tk()
        self.salesHistoryWindow.title("Sales History Information")

        # This will be the size of the Window
        window_width = 500
        window_height = 400

        centerWindow(self.salesHistoryWindow,window_width,window_height)
        
        self.listOfSalesHistory = ttk.Treeview(self.salesHistoryWindow, columns=("Receipt ID", "Product", "Unit Price", "Total Items", "Total Price"), show="headings")

        # Name the columns
        self.listOfSalesHistory.heading("Receipt ID", text="Receipt ID")
        self.listOfSalesHistory.heading("Product", text="Product")
        self.listOfSalesHistory.heading("Unit Price", text="Unit Price")
        self.listOfSalesHistory.heading("Total Items", text="Total Items")
        self.listOfSalesHistory.heading("Total Price", text="Total Price")

        # Adjust column's width
        self.listOfSalesHistory.column("Receipt ID", width=100)
        self.listOfSalesHistory.column("Product", width=150)
        self.listOfSalesHistory.column("Unit Price", width=100)
        self.listOfSalesHistory.column("Total Items", width=100)
        self.listOfSalesHistory.column("Total Price", width=100)

        # Add the treeview to window
        self.listOfSalesHistory.pack(expand=True, fill=tkinter.BOTH)

        # Get a list of the purschase IDs in salesHistoryTotal
        listOfPurchaseIDs = []
        for itemInSalesHistoryTotal in CashRegisterApp.salesHistoryTotal:
            listOfPurchaseIDs.append(CashRegisterApp.salesHistoryTotal[itemInSalesHistoryTotal]['purchaseID'])

        # Get detail of current (1st) purchase ID
        currentPurchaseID = listOfPurchaseIDs[0]

        # Fill the treeview with the SalesHistory
        for itemInSaleHistory in CashRegisterApp.salesHistory:
            # Obtain details for each item
            productID, purchaseID, name, unitPrice, totalItems, totalPrice = self.obtainItemFromSalesHistory(itemInSaleHistory)

            if purchaseID == currentPurchaseID:
                self.listOfSalesHistory.insert("", "end", values=(purchaseID, name, f"$ {unitPrice:.2f}", totalItems, f"$ {totalPrice:.2f}"))
            else:
                # This means that there is a new purschase ID in the list
                # Add the detail of total for the previous purchase
                purchaseTotal = CashRegisterApp.salesHistoryTotal[currentPurchaseID]['total']
                self.listOfSalesHistory.insert("", "end", values=("", "", "", "Total", f"$ {purchaseTotal:.2f}"))

                # Update value of currentPurchaseID
                currentPurchaseID = purchaseID

                # Insert data of the current purchase
                self.listOfSalesHistory.insert("", "end", values=(purchaseID, name, f"$ {unitPrice:.2f}", totalItems, f"$ {totalPrice:.2f}"))

        # Add total of last purchase
        purchaseTotal = CashRegisterApp.salesHistoryTotal[currentPurchaseID]['total']
        self.listOfSalesHistory.insert("", "end", values=("", "", "", "Total", f"$ {purchaseTotal:.2f}"))

        # Button to close the window
        self.buttonOkSales = ttk.Button(self.salesHistoryWindow, text="Ok", command=self.salesHistoryWindow.destroy)
        self.buttonOkSales.pack()    

        self.salesHistoryWindow.mainloop()

    @classmethod
    def obtainItemFromShoppingCart(cls, id):
        # Obtain details from item in shopping cart by its ID
        productID = CashRegisterApp.shoppingCart[id]["productID"]
        purchaseID = CashRegisterApp.shoppingCart[id]["purchaseID"]
        name = CashRegisterApp.shoppingCart[id]["name"]
        unitPrice = CashRegisterApp.shoppingCart[id]["unitPrice"]
        totalItems = CashRegisterApp.shoppingCart[id]["totalItems"]
        totalPrice = CashRegisterApp.shoppingCart[id]["totalPrice"]
        return productID, purchaseID, name, unitPrice, totalItems, totalPrice
    
    @classmethod
    def obtainItemFromSalesHistory(cls, id):
        # Obtain details from item in shopping cart by its ID
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
        # CashRegisterApp.shoppingCart.update({len(CashRegisterApp.shoppingCart)+1:{
        CashRegisterApp.shoppingCart[id] =   {  
            
            "purchaseID": CashRegisterApp.purchaseID,
            "productID": id,
            "name": name,
            "unitPrice": price,
            "totalItems": totalItems,
            "totalPrice": totalItems * price
        }
        # })

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
        
    @classmethod
    def updateSalesHistoryTotal(cls, purchaseID, total):
        CashRegisterApp.salesHistoryTotal.update({purchaseID:{
                "purchaseID": purchaseID, 
                "total": total
            }}
        )
        
    
        
        