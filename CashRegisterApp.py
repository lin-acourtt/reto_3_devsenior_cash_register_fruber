import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter.constants import DISABLED, NORMAL 
from operations import centerWindow, updateSelectedProductLabel, is_valid_number
from exceptions import InvalidNumberInput, InvalidNumberInputHandler, NoProductSelectedError, InsuficientStockError, InsufficientStockErrorHandler
from styles import apply_Treeview_styles, apply_Label_styles, apply_Frame_styles, apply_Entry_styles, apply_Button_styles


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
        
        # Applying styles
        style = ttk.Style(self.cashRegisterAppMainWindow)
        apply_Treeview_styles(style)
        apply_Frame_styles(style)
        apply_Label_styles(style)
        apply_Entry_styles(style)
        apply_Button_styles(style)
        
        # Set parameters
        self.cashRegisterAppMainWindow.title("Shopping")

        # This will be the size of the Window
        window_width = 600
        window_height = 600

        centerWindow(self.cashRegisterAppMainWindow,window_width,window_height)
        self.cashRegisterAppMainWindow.resizable(False,False)

        # Create Label
        self.labelSelectProductTitle = ttk.Label(self.cashRegisterAppMainWindow,text="Please select a product to shop: ")
        self.labelSelectProductTitle.pack()
        
        # Adding a frame to place the treeview and its corresponding scrollbar
        self.frameTreeview = ttk.Frame(self.cashRegisterAppMainWindow)
        self.frameTreeview.pack()
        
        # Adding the TreeView to display the products
        # Doing only this, will create an empty heading
        self.listOfItems = ttk.Treeview(self.frameTreeview, columns=("Name", "Price", "Stock"), show="headings")
        # It is necessary to add the name of each column
        self.listOfItems.heading("Name", text="Name")
        self.listOfItems.heading("Price", text="Price")
        self.listOfItems.heading("Stock", text="Stock")
        # Now the Treeview object will be filled with the products information
        for prodID in listOfProducts:
            self.listOfItems.insert("","end",iid=prodID,values=(listOfProducts[prodID]["name"],f"$ {listOfProducts[prodID]["price"]:.2f}",listOfProducts[prodID]["stock"]))
        
        self.listOfItems.column("Name",width=150)
        self.listOfItems.column("Price",width=150)
        self.listOfItems.column("Stock",width=150)

        self.listOfItems.grid(row=0,column=0)
        
        # Constructing vertical scrollbar with treeview
        self.verscrlbar = ttk.Scrollbar(self.frameTreeview, orient ="vertical", command = self.listOfItems.yview)
        
        # Placing the scrollback into the Frame's grid.
        self.verscrlbar.grid(row=0,column=1,sticky="nesw") #nesw
        
        # Configuring treeview with the yscroll command
        self.listOfItems.configure(yscrollcommand = self.verscrlbar.set)

        # Create Frame to contain the remaining widgets
        self.frameWidgets = ttk.Frame(self.cashRegisterAppMainWindow, style="TFrame")
        self.frameWidgets.pack(pady=15)
        self.frameWidgets.rowconfigure(2,minsize=100)
        self.frameWidgets.columnconfigure(1,minsize=50)
        
        # Label to display the product that will be added to the cart
        self.labelSelectedProduct = ttk.Label(self.frameWidgets,text="Selected item")
        self.labelSelectedProduct.grid(row=0,column=0)

        # On button release, the label of selectedProductLabel will be updated with the selected product
        self.listOfItems.bind("<ButtonRelease-1>", lambda event:updateSelectedProductLabel(event,self.listOfItems, self.labelSelectedProduct))

        # Create a tkinter string variable to hold the input value in the entry box for the amount of products
        input_validation = tkinter.StringVar(self.cashRegisterAppMainWindow)

        # Create a validation command that will call is_valid_number
        vcmd = (self.cashRegisterAppMainWindow.register(is_valid_number), '%P')
        
        self.frameLabelEntry = ttk.Frame(self.frameWidgets)
        self.frameLabelEntry.grid(row=1,column=0)

        self.labelAmount = ttk.Label(self.frameLabelEntry, text="Amount: ")
        self.labelAmount.grid(row=0, column=0, padx=5)

        # Create the Entry widget with validation        
        self.entryAmountToBuy = ttk.Entry(self.frameLabelEntry, textvariable=input_validation, validate="key", validatecommand=vcmd)
        self.entryAmountToBuy.grid(row=0, column=1, padx=5)
        
        # Button to add product to shopping cart 
        self.buttonAddProduct = ttk.Button(self.frameWidgets,text="Add item to shopping cart",
                                        command=self.addItemToShoppingCart, style="TButton")
        self.buttonAddProduct.grid(row=2,column=0)

        # Button to open a new Window to the shopping cart
        self.buttonViewShoppingCart = ttk.Button(self.frameWidgets,text="View shopping cart",command=self.openShoppingCartWindow, state=DISABLED)
        self.buttonViewShoppingCart.grid(row=0,column=2)

        # Button to open a new Window to the see the sales history
        self.buttonViewSalesHistory = ttk.Button(self.frameWidgets,text="View sales history",command=self.openSalesHistoryWindow, state=DISABLED)
        self.buttonViewSalesHistory.grid(row=2,column=2)
        
        style.configure("Exit.TButton",
                        background="red3",  # Red bg
                        foreground="brown4",  # White text
                        font=("Arial", 10, "bold"))  # Fontsize
                        #padding=10)  # Padding

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

        except ValueError as e:  
            messagebox.showerror("Error", "Invalid input")
            
    def openShoppingCartWindow(self):
        
        # Open a new window with the shopping cart's contents
        self.shoppingCartWindow = tkinter.Tk()
        self.shoppingCartWindow.title("Shopping Cart Info")
        self.shoppingCartWindow.resizable(False,False)

        # This will be the size of the Window
        window_width = 500
        window_height = 400

        centerWindow(self.shoppingCartWindow,window_width,window_height)
        
        style = ttk.Style(self.shoppingCartWindow)
        apply_Treeview_styles(style)
        apply_Button_styles(style)

        # Adding a frame to place the treeview and its corresponding scrollbar
        self.frameTreeviewShoppingCart = ttk.Frame(self.shoppingCartWindow)
        self.frameTreeviewShoppingCart.pack(pady=10)
        
        self.listOfItemsShoppingCart = ttk.Treeview(self.frameTreeviewShoppingCart, columns=("Name", "Amount", "Total_Price"), show="headings")
        # It is necessary to add the name of each column
        self.listOfItemsShoppingCart.heading("Name", text="Name")
        self.listOfItemsShoppingCart.heading("Amount", text="Amount")
        self.listOfItemsShoppingCart.heading("Total_Price", text="Total Price")
        self.listOfItemsShoppingCart.column("Name",width=100)
        self.listOfItemsShoppingCart.column("Amount",width=100)
        self.listOfItemsShoppingCart.column("Total_Price",width=100)
        
        self.listOfItemsShoppingCart.grid(row=0,column=0)

        for product in CashRegisterApp.shoppingCart:
            self.listOfItemsShoppingCart.insert("","end",iid=product,values=(CashRegisterApp.shoppingCart[product]["name"],CashRegisterApp.shoppingCart[product]["totalItems"],f"$ {CashRegisterApp.shoppingCart[product]["totalPrice"]:.2f}"))
        
        # Add the total price of the items in the shopping cart
        # Add total of last purchase
        purchaseTotal = self.calculateTotalPrice()
        self.listOfItemsShoppingCart.insert("", "end", values=("Total", "", f"$ {purchaseTotal:.2f}"))
        
        # Constructing vertical scrollbar with treeview
        self.scrlShoppingCart = ttk.Scrollbar(self.frameTreeviewShoppingCart, orient ="vertical", command = self.listOfItemsShoppingCart.yview)
        
        # Placing the scrollback into the Frame's grid.
        self.scrlShoppingCart.grid(row=0,column=1,sticky="nesw") #nesw
        
        # Configuring treeview with the yscroll command
        self.listOfItemsShoppingCart.configure(yscrollcommand = self.scrlShoppingCart.set)

        self.buttonConfirmPurchase = ttk.Button(self.shoppingCartWindow,text="Buy", command=self.buy)
        self.buttonConfirmPurchase.pack(pady=10)

        self.buttonCancelPurchase = ttk.Button(self.shoppingCartWindow,text="Cancel", command=self.cancelPurchase)
        self.buttonCancelPurchase.pack(pady=10)

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
        self.salesHistoryWindow.resizable(False,False)

        # This will be the size of the Window
        window_width = 600
        window_height = 400

        centerWindow(self.salesHistoryWindow,window_width,window_height)
        style = ttk.Style(self.salesHistoryWindow)
        apply_Treeview_styles(style)
        apply_Button_styles(style)

        # Adding a frame to place the treeview and its corresponding scrollbar
        self.frameTreeviewSalesHistory = ttk.Frame(self.salesHistoryWindow)
        self.frameTreeviewSalesHistory.pack(pady=10)
        
        self.listOfSalesHistory = ttk.Treeview(self.frameTreeviewSalesHistory, columns=("Receipt ID", "Product", "Unit Price", "Total Items", "Total Price"), show="headings")

        # Name the columns
        self.listOfSalesHistory.heading("Receipt ID", text="Receipt ID")
        self.listOfSalesHistory.heading("Product", text="Product")
        self.listOfSalesHistory.heading("Unit Price", text="Unit Price")
        self.listOfSalesHistory.heading("Total Items", text="Total Items")
        self.listOfSalesHistory.heading("Total Price", text="Total Price")

        # Adjust column's width
        self.listOfSalesHistory.column("Receipt ID", width=100)
        self.listOfSalesHistory.column("Product", width=100)
        self.listOfSalesHistory.column("Unit Price", width=100)
        self.listOfSalesHistory.column("Total Items", width=100)
        self.listOfSalesHistory.column("Total Price", width=100)

        # Add the treeview to window
        self.listOfSalesHistory.grid(row=0,column=0)

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

        # Constructing vertical scrollbar with treeview
        self.scrlSalesHistory = ttk.Scrollbar(self.frameTreeviewSalesHistory, orient ="vertical", command = self.listOfSalesHistory.yview)
        
        # Placing the scrollback into the Frame's grid.
        self.scrlSalesHistory.grid(row=0,column=1,sticky="nesw") #nesw
        
        # Configuring treeview with the yscroll command
        self.listOfSalesHistory.configure(yscrollcommand = self.scrlSalesHistory.set)

        # Button to close the window
        self.buttonOkSales = ttk.Button(self.salesHistoryWindow, text="Ok", command=self.salesHistoryWindow.destroy)
        self.buttonOkSales.pack(pady=10)    

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
        
    
        
        