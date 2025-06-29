import tkinter as tk
from tkinter import ttk

# Tasas de cambio fijas
exchange_rates = {
    ("USD", "EUR"): 0.89, ("USD", "MXN"): 17.14, ("USD", "GBP"): 0.78,
    ("USD", "JPY"): 157.30, ("USD", "CAD"): 1.36, ("USD", "BRL"): 5.42, ("USD", "CHF"): 0.89,
    ("EUR", "USD"): 1 / 0.89, ("MXN", "USD"): 1 / 17.14, ("GBP", "USD"): 1 / 0.78,
    ("JPY", "USD"): 1 / 157.30, ("CAD", "USD"): 1 / 1.36, ("BRL", "USD"): 1 / 5.42, ("CHF", "USD"): 1 / 0.89,
    ("EUR", "MXN"): 19.25, ("EUR", "GBP"): 0.87, ("EUR", "JPY"): 170.50,
    ("EUR", "CAD"): 1.52, ("EUR", "BRL"): 6.10, ("EUR", "CHF"): 0.98,
    ("MXN", "EUR"): 1 / 19.25, ("GBP", "EUR"): 1 / 0.87, ("JPY", "EUR"): 1 / 170.50,
    ("CAD", "EUR"): 1 / 1.52, ("BRL", "EUR"): 1 / 6.10, ("CHF", "EUR"): 1 / 0.98,
}

class ConversorDeMonedas:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Monedas")
        self.root.configure(bg="#FFD1DC")  # 🎀 Fondo rosado pastel
        self.input_value = ""

        monedas = sorted(set([moneda for par in exchange_rates.keys() for moneda in par]))
        self.monedas = monedas

        self.from_currency = tk.StringVar(value="USD")
        self.to_currency = tk.StringVar(value="EUR")

        self.frame = tk.Frame(self.root, bg="#FFD1DC")
        self.frame.pack(expand=True)

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="From Currency").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.from_combo = ttk.Combobox(self.frame, textvariable=self.from_currency, values=self.monedas)
        self.from_combo.grid(row=0, column=1, pady=5)

        self.input_entry = tk.Entry(self.frame, font=("Arial", 18), justify="right", width=10)
        self.input_entry.grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Label(self.frame, text="To Currency").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.to_combo = ttk.Combobox(self.frame, textvariable=self.to_currency, values=self.monedas)
        self.to_combo.grid(row=2, column=1, pady=5)

        self.output_entry = tk.Entry(self.frame, font=("Arial", 18), justify="right", width=10)
        self.output_entry.grid(row=3, column=0, columnspan=2, pady=5)

        self.rate_label = tk.Label(self.frame, text="Rate: 1 USD = 0.89 EUR", bg="#FFD1DC", fg="black")
        self.rate_label.grid(row=4, column=0, columnspan=2, pady=5)

        keypad_frame = tk.Frame(self.frame, bg="#FFD1DC")
        keypad_frame.grid(row=5, column=0, columnspan=2)

        buttons = [
            "7", "8", "9", "C",
            "4", "5", "6", "←",
            "1", "2", "3", "=",
            "0", "00", ".", "↔"
        ]

        row = 0
        col = 0
        for button in buttons:
            action = lambda x=button: self.click(x)
            tk.Button(
                keypad_frame, text=button, width=5, height=2,
                command=action, bg="#00BFFF", fg="white", font=("Arial", 12),
                activebackground="#1E90FF", bd=0
            ).grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def click(self, key):
        if key == "C":
            self.input_value = ""
            self.input_entry.delete(0, tk.END)
            self.output_entry.delete(0, tk.END)
        elif key == "←":
            self.input_value = self.input_value[:-1]
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.input_value)
        elif key == "=":
            self.convert()
        elif key == "↔":
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()
            self.from_currency.set(to_curr)
            self.to_currency.set(from_curr)
        else:
            self.input_value += key
            self.input_entry.insert(tk.END, key)

    def convert(self):
        try:
            amount = float(self.input_entry.get())
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()
            if from_curr == to_curr:
                converted = amount
                rate = 1
            else:
                rate = exchange_rates.get((from_curr, to_curr), None)
                if rate is None:
                    self.output_entry.delete(0, tk.END)
                    self.output_entry.insert(0, "No rate")
                    return
                converted = round(amount * rate, 2)

            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, f"{converted}")
            self.rate_label.config(text=f"Rate: 1 {from_curr} = {round(rate, 4)} {to_curr}")
        except:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, "Error")

# Ejecutar aplicación
root = tk.Tk()
root.geometry("600x500")
app = ConversorDeMonedas(root)
root.mainloop()

