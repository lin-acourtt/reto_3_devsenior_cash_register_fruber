from CashRegisterApp import CashierApp
from products import listOfProducts

def main():
    myApp = CashierApp()
    myApp.createShoppingWindow(listOfProducts)

if __name__ == "__main__":
    main()