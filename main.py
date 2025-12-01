import tkinter as tk
from gui import InterfaceGrafica

def main():
    raiz = tk.Tk()
    aplicacao = InterfaceGrafica(raiz)
    raiz.mainloop()

if __name__ == "__main__":
    main()