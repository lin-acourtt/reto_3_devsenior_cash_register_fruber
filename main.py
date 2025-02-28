from CashRegisterApp import CashRegisterApp
from products import listOfProducts

if __name__ == "__main__":
    myApp = CashRegisterApp()

    myApp.openCashRegisterMainWindow(listOfProducts)