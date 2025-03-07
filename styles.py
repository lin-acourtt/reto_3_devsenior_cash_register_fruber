import tkinter as tk
from tkinter import ttk


def apply_Treeview_styles(style):
    # style = ttk.Style()
    
    style.configure("Treeview",
                    background="papaya whip",  # Fondo de las filas
                    foreground="black",        # Color del texto
                    fieldbackground="lightgray",  # Fondo de las celdas
                    font=("Arial", 10),        # Tipo de fuente
                    rowheight=20)             # Alto de las filas

    style.configure("Treeview.Heading",
                    background="lightblue",  # Fondo de las cabeceras
                    foreground="maroon",     # Color del texto en las cabeceras
                    font=("Helvetica", 12, "bold"),  # Fuente de las cabeceras
                    relief="solid",          # Borde alrededor de las cabeceras
                    anchor="center")         # Alinear al centro

    # style.map("Treeview",
    #             background=[("selected", "navajo white")])
    
    
def apply_Frame_styles(style):
        style.configure("TFrame",
                # background="white",  # Fondo del marco
                relief="flat",   
                padding=20)   

def apply_Label_styles(style):
        style.configure("TLabel",
                foreground="green4",      # Color del texto
                font=("Arial", 14, "italic"))
        
def apply_Entry_styles(style):
            style.configure("TEntry",

                foreground="brown",      # Color del texto
                font=("Courier", 12),    # Fuente del texto
                padding=5,               # Espaciado dentro del campo
                relief="raised")      
            
def apply_Button_styles(style):
            style.configure("TButton", background="green2",
                        foreground="deep pink",
                        font=("Helvetica", 12, "bold"),  # Fuente y tamaño de texto
                        padding=10,
                        )
        
            style.map("TButton",
                background=[("active","darkgreen"), 
                            ("pressed","lightgreen" )])            