# cashRegisterApp.py
import tkinter
from tkinter import ttk
from tkinter import messagebox
from operations import CashierAppOperations


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
        