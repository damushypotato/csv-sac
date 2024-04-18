import tkinter as tk
from tkinter import ttk
import datetime
import csv

coffees = {
    "Flat White": 2.5,
    "Cappuccino": 3.5,
    "Short Black": 2,
    "Latte": 3,
}

size_options = {
    "Small": 0,
    "Regular": 0.5,
    "Large": 1,
}

milk_options = {
    "Full Cream Milk": 0,
    "Skim Milk": 0.5,
    "Soy Milk": 1,
}

sugar_options = {
    "No Sugar": 0,
    "1 Sugar": 0.1,
    "2 Sugars": 0.2,
} 

def calculate_price(coffee, size, milk, sugar):
    return coffees[coffee] + size_options[size] + milk_options[milk] + sugar_options[sugar]

def save_order(name, date, cost, coffee, size, milk, sugar):
    #validate the input
    if name == "" or coffee == "" or size == "" or milk == "" or sugar == "":
        return
    
    try:
        datetime.datetime.strptime(date, "%Y/%m/%d")
    except ValueError:
        return

    with open("orders.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["Name", "Date", "Cost", "Coffee", "Size", "Milk", "Sugar"])
        writer.writerow([name, date, cost, coffee, size, milk, sugar])

def App():

    root = tk.Tk()
    root.title("Coffee Order")

    frame = tk.Frame(root)
    frame.grid(column=0, row=0, padx=25, pady=25)

    ttk.Label(frame, text="Coffee Shop", font=("Copperplate Gothic Bold", 20)).grid(column=0, row=0, pady=25)

    form=ttk.Frame(frame)
    form.grid(column=0, row=1, padx=25)

    name = tk.StringVar()
    date = tk.StringVar()
    coffee = tk.StringVar()
    size = tk.StringVar()
    milk = tk.StringVar()
    sugar = tk.StringVar()
    preview = tk.StringVar()

    def update_preview():
        c_ = coffee.get()
        s_ = size.get()
        m_ = milk.get()
        su_ = sugar.get()
        
        if c_ == "" or s_ == "" or m_ == "" or su_ == "":
            return
        
        cost = "{:.2f}".format(calculate_price(c_, s_, m_, su_))
        
        preview.set(f"Order:\n\n{c_}\n{s_}\n{m_}\n{su_}\n\n${cost}")

    def submit_order():
        n_ = name.get()
        d_ = date.get()
        c_ = coffee.get()
        s_ = size.get()
        m_ = milk.get()
        su_ = sugar.get()

        if c_ == "" or s_ == "" or m_ == "" or su_ == "":
            preview.set("Please select all options.")
            return
        
        if n_ == "":
            preview.set("Please enter customer name.")
            return
        
        cost = calculate_price(c_, s_, m_, su_)

        save_order(n_, d_, cost, c_, s_, m_, su_)

        preview.set("Order submitted.")

        name.set("")

    def view_orders():
        #open the orders.csv file and display the contents in a treeview, with a option to search for a specific order
        orders = tk.Tk()
        orders.title("Orders")

        tree = ttk.Treeview(orders)
        tree["columns"] = ("Name", "Date", "Cost", "Coffee", "Size", "Milk", "Sugar")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Name", anchor=tk.W, width=100)
        tree.column("Date", anchor=tk.W, width=100)
        tree.column("Cost", anchor=tk.W, width=100)
        tree.column("Coffee", anchor=tk.W, width=100)
        tree.column("Size", anchor=tk.W, width=100)
        tree.column("Milk", anchor=tk.W, width=100)
        tree.column("Sugar", anchor=tk.W, width=100)
        
        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("Name", text="Name", anchor=tk.W)
        tree.heading("Date", text="Date", anchor=tk.W)
        tree.heading("Cost", text="Cost", anchor=tk.W)
        tree.heading("Coffee", text="Coffee", anchor=tk.W)
        tree.heading("Size", text="Size", anchor=tk.W)
        tree.heading("Milk", text="Milk", anchor=tk.W)
        tree.heading("Sugar", text="Sugar", anchor=tk.W)

        with open("orders.csv", "r") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    continue
                tree.insert("", tk.END, values=row)

        tree.pack()

        def search_orders():
            search_query = search_entry.get()
            if search_query == "":
                with open("orders.csv", "r") as f:
                    reader = csv.reader(f)
                    for row in tree.get_children():
                        tree.delete(row)
                    for i, row in enumerate(reader):
                        if i == 0:
                            continue
                        tree.insert("", tk.END, values=row)
            else:
                with open("orders.csv", "r") as f:
                    reader = csv.reader(f)
                    for row in tree.get_children():
                        tree.delete(row)
                    for i, row in enumerate(reader):
                        if i == 0:
                            continue
                        if search_query in row:
                            tree.insert("", tk.END, values=row)
                            
        ttk.Label(orders, text="Search:", font=("Arial",12)).pack()
        search_entry = ttk.Entry(orders)
        search_entry.pack()
        ttk.Button(orders, text="Search", command=search_orders).pack()


        orders.mainloop()



    ttk.Label(form, text="Name:", font=("Arial",12)).grid(column=0, row=0, pady=10, sticky="E")
    name_entry = ttk.Entry(form, textvariable=name)
    name_entry.grid(column=1, row=0, pady=10, sticky="W")

    date.set(datetime.date.today().strftime("%Y/%m/%d"))
    ttk.Label(form, text="Date:", font=("Arial",12)).grid(column=0, row=1, pady=10, sticky="E")
    date_entry = ttk.Entry(form, textvariable=date)
    date_entry.grid(column=1, row=1, pady=10, sticky="W")

    preview.set("Your order will appear here")

    #options as radio buttons that update the preview
    ttk.Label(form, text="Coffee:", font=("Arial",12)).grid(column=0, row=2, pady=10, sticky="E")
    c_frame = ttk.Frame(form)
    c_frame.grid(column=1, row=2, sticky="W")
    for i, c_ in enumerate(coffees):
        ttk.Radiobutton(c_frame, text=c_, variable=coffee, value=c_, command=update_preview).grid(column=i, row=2, padx=10, pady=10, sticky="W")

    ttk.Label(form, text="Size:", font=("Arial",12)).grid(column=0, row=3, pady=10, sticky="E")
    s_frame = ttk.Frame(form)
    s_frame.grid(column=1, row=3, sticky="W")
    for i, s_ in enumerate(size_options):
        ttk.Radiobutton(s_frame, text=s_, variable=size, value=s_, command=update_preview).grid(column=i, row=3, padx=10, pady=10, sticky="W")

    ttk.Label(form, text="Milk:", font=("Arial",12)).grid(column=0, row=4, pady=10, sticky="E")
    m_frame = ttk.Frame(form)
    m_frame.grid(column=1, row=4, sticky="W")
    for i, m_ in enumerate(milk_options):
        ttk.Radiobutton(m_frame, text=m_, variable=milk, value=m_, command=update_preview).grid(column=i, row=4, padx=10, pady=10, sticky="W")

    ttk.Label(form, text="Sugar:", font=("Arial",12)).grid(column=0, row=5, pady=10, sticky="E")
    su_frame = ttk.Frame(form)
    su_frame.grid(column=1, row=5, sticky="W")
    for i, su_ in enumerate(sugar_options):
        ttk.Radiobutton(su_frame, text=su_, variable=sugar, value=su_, command=update_preview).grid(column=i, row=5, padx=10, pady=10, sticky="W")

    ttk.Label(frame, textvariable=preview, font=("Consolas", 11)).grid(column=0, row=6, pady=10)

    ttk.Button(frame, text="Submit Order", command=lambda: submit_order(), padding=5).grid(column=0, row=7, pady=10)

    ttk.Button(frame, text="View Orders", command=lambda: view_orders(), padding=5).grid(column=0, row=8, pady=10)

    root.mainloop()

App()