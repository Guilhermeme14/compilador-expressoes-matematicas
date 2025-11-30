import tkinter as tk
from gui import InterfaceGrafica

def principal():
    """Função principal"""
    raiz = tk.Tk()
    aplicacao = InterfaceGrafica(raiz)
    raiz.mainloop()

if __name__ == "__main__":
    principal()