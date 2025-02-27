# cashRegisterApp.py
import tkinter
from tkinter import ttk
from tkinter import messagebox
from operations import CashierAppOperations
from products import listOfProducts



class CashierApp:

    # Used to identify which items were part of the same purchase
    purchaseCounter = 1
    # Used to store the history of all sells
    salesHistory = {} # Structure will be: {purchaseID: ID, productId: id, name: ProductName, unitPrice: UnitPrice, totalItems: TotalItems, totalPrice: TotalPrice }
    # Used to store items added to the shopping card
    shoppingCart = {} # Structure will be: {purchaseID: ID, name: ProductName, TotalItems, totalPrice: TotalPrice } 


    def createShoppingWindow(self,listOfProducts):
        # Create Window
        self.windowShoppingApp = tkinter.Tk()
        # Set parameters
        self.windowShoppingApp.title("Shopping")

        # This will be the size of the Window
        window_width = 600
        window_height = 600

        # This gets the screen information
        screen_width = self.windowShoppingApp.winfo_screenwidth()
        screen_height = self.windowShoppingApp.winfo_screenheight()

        # This specifies the position of the window
        window_post_x = int((screen_width - window_width)/2)
        window_post_y = int((screen_height - window_height)/2) 

        # Specify position and size of the window
        self.windowShoppingApp.geometry(f"{window_width}x{window_height}+{window_post_x}+{window_post_y}")

        # Optional
        self.label1 = ttk.Label(self.windowShoppingApp,text="Select a product: ")
        self.label1.pack()

        # Adding the table to display the products
        # Doing this will create an empty heading
        self.items = ttk.Treeview(self.windowShoppingApp, columns=("Name", "Price", "Stock"), show="headings")
        # It is necessary to add the name of each column
        self.items.heading("Name", text="Name")
        self.items.heading("Price", text="Price")
        self.items.heading("Stock", text="Stock")
        #self.items.pack(pady=10, fill="both",expand=True)
        self.items.pack()


        for prodID in listOfProducts:
            self.items.insert("","end",iid=prodID,values=(listOfProducts[prodID]["name"],f"$ {listOfProducts[prodID]["price"]:.2f}",listOfProducts[prodID]["stock"]))
        
        # Label to display the product that will be added to the cart
        self.selectedProductLabel = ttk.Label(self.windowShoppingApp,text="Selected item")
        self.selectedProductLabel.pack()
        
        def updateSelectedProductLabel(event):            
            id = self.items.selection()[0]
            self.selectedProductLabel.configure(text=listOfProducts[int(id)]['name'])

        # On button release, the label of selectedProductLabel will be updated with the selected product
        self.items.bind("<ButtonRelease-1>", updateSelectedProductLabel)

        self.amountToBuy = ttk.Entry(self.windowShoppingApp,text="0")
        self.amountToBuy.pack()

        # Button to add product to shopping cart 
        self.addButton = ttk.Button(self.windowShoppingApp,text="Add item to shopping cart",command=self.addItemToShoppingCart)
        self.addButton.pack()

        self.viewShoppingCartButton = ttk.Button(self.windowShoppingApp,text="View shopping cart",command=self.viewShoppingCart)
        self.viewShoppingCartButton.pack()

        self.vieSalesHistoryButton = ttk.Button(self.windowShoppingApp,text="View sales history",command=self.displaySalesHistory)
        self.vieSalesHistoryButton.pack()

        self.windowShoppingApp.mainloop()
        
    def addItemToShoppingCart(self):
        # Agregar productos al carrito de compras }}}
        id = self.items.selection()[0]
        price = float(listOfProducts[int(id)]['price'])
        
        print(f"ID: {id}")
        print(f"Item: {self.selectedProductLabel['text']}")
        print(f"Cantidad: {self.amountToBuy.get()}")
        print(f"precio: {price}")

    def viewShoppingCart(self):
        # Ver los productos en el carrito
        print(CashierApp.shoppingCart)
        self.viewShoppingCartWindow = tkinter.Tk()
        self.viewShoppingCartWindow.title("Shopping Cart Info")

        # This will be the size of the Window
        window_width = 500
        window_height = 400

        # This gets the screen information
        screen_width = self.windowShoppingApp.winfo_screenwidth()
        screen_height = self.windowShoppingApp.winfo_screenheight()

        # This specifies the position of the window
        window_post_x = int((screen_width - window_width)/2)
        window_post_y = int((screen_height - window_height)/2) 

        # Specify position and size of the window
        self.viewShoppingCartWindow.geometry(f"{window_width}x{window_height}+{window_post_x}+{window_post_y}")

        self.itemsShoppingCart = ttk.Treeview(self.viewShoppingCartWindow, columns=("Name", "Amount", "Total_Price"), show="headings")
        # It is necessary to add the name of each column
        self.itemsShoppingCart.heading("Name", text="Name")
        self.itemsShoppingCart.heading("Amount", text="Amount")
        self.itemsShoppingCart.heading("Total_Price", text="Total Price")
        #self.items.pack(pady=10, fill="both",expand=True)
        self.itemsShoppingCart.pack()

        for product in self.shoppingCart:
            self.itemsShoppingCart.insert("","end",iid=product,values=(self.shoppingCart[product]["name"],self.shoppingCart[product]["totalItems"],f"$ {self.shoppingCart[product]["totalPrice"]:.2f}"))
        
        self.confirmPurchase = ttk.Button(self.viewShoppingCartWindow,text="Buy", command=self.buy)
        self.confirmPurchase.pack()

        self.cancelPurchase = ttk.Button(self.viewShoppingCartWindow,text="Cancel", command=self.cancelPurchase)
        self.cancelPurchase.pack()

        self.viewShoppingCartWindow.mainloop()
        ...

    
    def cancelPurchase(self):
        # Cancelar la compra y limpiar el carrito }}}}
        print("Canceling")
        print("clean shopping cart")
        self.viewShoppingCartButton['text'] = "View shopping cart"
        self.viewShoppingCartWindow.destroy()
        print(f"New shopping cart (It should be empty): {CashierApp.shoppingCart}")

    def displaySalesHistory(self):
        # Mostrar el historial de ventas
        salesHistoryStrings = []
        salesHistoryStrings.append("----------------------")
        salesHistoryStrings.append("Receipt ID - Product - Unit Price - Total Items - Total Price")
        for itemInSaleHistory in CashierApp.salesHistory:
            productID = CashierApp.salesHistory[itemInSaleHistory]["productID"]
            purchaseID = CashierApp.salesHistory[itemInSaleHistory]["purchaseID"]
            name = CashierApp.salesHistory[itemInSaleHistory]["name"]
            unitPrice = CashierApp.salesHistory[itemInSaleHistory]["unitPrice"]
            totalItems = CashierApp.salesHistory[itemInSaleHistory]["totalItems"]
            totalPrice = CashierApp.salesHistory[itemInSaleHistory]["totalPrice"]
            salesHistoryStrings.append(f"\n{purchaseID} - {name} - {unitPrice} - {totalItems} - {totalPrice}")
        salesHistoryStrings.append("\n----------------------")
        
        self.viewSalesHistoryWindow = tkinter.Tk()
        self.viewSalesHistoryWindow.title("Sales History Information")

        # This will be the size of the Window
        window_width = 500
        window_height = 400

        # This gets the screen information
        screen_width = self.windowShoppingApp.winfo_screenwidth()
        screen_height = self.windowShoppingApp.winfo_screenheight()

        # This specifies the position of the window
        window_post_x = int((screen_width - window_width)/2)
        window_post_y = int((screen_height - window_height)/2) 

        # Specify position and size of the window
        self.viewSalesHistoryWindow.geometry(f"{window_width}x{window_height}+{window_post_x}+{window_post_y}")

        self.salesHistoryText = tkinter.Label(self.viewSalesHistoryWindow, text=salesHistoryStrings)
        self.salesHistoryText.pack()

        self.okSalesButton = ttk.Button(self.viewSalesHistoryWindow,text="Ok", command=self.viewSalesHistoryWindow.destroy)
        self.okSalesButton.pack()

        self.viewSalesHistoryWindow.mainloop()

# Creación de la aplicación
myApp = CashierApp()
myApp.createShoppingWindow(listOfProducts)        