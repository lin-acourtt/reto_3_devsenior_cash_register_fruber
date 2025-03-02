from tkinter import messagebox

# def InvalidNumberInput(exception):
#     """It handles errors in the application"""
#     #print(f"Error: {exception}")
class NoProductSelectedError(Exception):
    """ Excepcion when you dont select a product. """
    pass
        
class InvalidNumberInput(Exception):
    """It handles errors in the application"""
    pass    
    
def InvalidNumberInputHandler(exception):
    """Handle the InvalidNumberInput exception."""
    # print(f"Error: {exception}")    
    messagebox.showerror("Error", str(exception))
    
