# Here we will store functions to process different operations in the CashRegisterApp class

import tkinter
from tkinter import ttk
from tkinter import messagebox
from exceptions import InvalidNumberInput, InvalidNumberInputHandler, NoProductSelectedError, InsuficientStockError, InsufficientStockErrorHandler



#### Windows' appearance
def centerWindow(window: tkinter, width: int, height: int):
    """Specify the window, width and height to center the given window"""

    # This gets the screen information
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # This specifies the position of the window
    window_post_x = int((screen_width - width)/2)
    window_post_y = int((screen_height - height)/2) 

    # Specify position and size of the window
    window.geometry(f"{width}x{height}+{window_post_x}+{window_post_y}")

#### Event handlers
def updateSelectedProductLabel(event, treeViewList: ttk.Treeview, labelToModify: ttk.Label):            
    id = treeViewList.selection()[0]
    newText = treeViewList.item(id)['values'][0]
    labelToModify.configure(text=newText)

def is_valid_number(input_value):
    if input_value == "":
        return True  # Allow empty value (for the user to clear the field)
    try:
        float(input_value)  # Try to convert the input to a float
        return True
    except ValueError:
        InvalidNumberInputHandler(InvalidNumberInput("Invalid entry, must be a number"))
        return False  # Return False if the input is not a valid number



