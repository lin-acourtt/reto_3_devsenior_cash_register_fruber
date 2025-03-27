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

class InsuficientStockError(Exception):
    """Excepción para cuando no hay suficiente stock."""
    def __init__(self, product_name, stock_available):
        self.product_name = product_name
        self.stock_available = stock_available
        self.message = f"Insufficient stock for {product_name}. Available stock: {stock_available}."
        super().__init__(self.message)
    
def InvalidNumberInputHandler(exception):
    """Handle the InvalidNumberInput exception."""
    # print(f"Error: {exception}")    
    messagebox.showerror("Error", str(exception))
    
def InsufficientStockErrorHandler(exception):
    """ Maneja la excepción InsufficientStockError mostrando un mensaje de error. """
    messagebox.showerror("Insufficient Stock", str(exception))    
    
