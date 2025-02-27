from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3 as sq
from tkinter import messagebox

def connect_db():
    return sq.connect('app.db')

# Create database and contacts table
def create_table():
    con = connect_db()
    c = con.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS CONTACTS (
                SLNO INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME CHAR(100) NOT NULL,
                PHONENUMBER TEXT NOT NULL,
                EMAIL TEXT NOT NULL
    )""")
    con.commit()
    con.close()

# Function to refresh the contacts table
def refresh_contacts():
    for item in tree.get_children():
        tree.delete(item)
    
    for widget in button_frame.winfo_children():
        widget.destroy()

    con = connect_db()
    c = con.cursor()
    c.execute("SELECT * FROM CONTACTS ORDER BY SLNO")
    contacts = c.fetchall()
    con.close()

    for i, row in enumerate(contacts):
        tree.insert('', 'end', values=(i + 1, row[1], row[2], row[3]))
        create_action_buttons(i + 1, row[0], row[1], row[2], row[3])

def delete_contact(slno):
    con = connect_db()
    c = con.cursor()
    
    try:
        c.execute("DELETE FROM CONTACTS WHERE SLNO=?", (slno,))
        con.commit()

        c.execute("SELECT ROWID, * FROM CONTACTS ORDER BY SLNO")
        contacts = c.fetchall()

        for i, contact in enumerate(contacts, start=1):
            c.execute("UPDATE CONTACTS SET SLNO=? WHERE ROWID=?", (i, contact[0]))

        con.commit()
        refresh_contacts()
        messagebox.showinfo("Success", "Contact deleted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting contact: {e}")
    finally:
        con.close()

def update_contact(slno, name, phone, email):
    update_window = Toplevel()
    update_window.title("Update Contact")
    update_window.geometry("350x200")

    Label(update_window, text="Name").grid(row=0, column=0, pady=5)
    Label(update_window, text="Phone Number").grid(row=1, column=0, pady=5)
    Label(update_window, text="Email").grid(row=2, column=0, pady=5)

    name_entry = Entry(update_window)
    name_entry.grid(row=0, column=1)
    name_entry.insert(0, name)

    phone_entry = Entry(update_window)
    phone_entry.grid(row=1, column=1)
    phone_entry.insert(0, phone)

    email_entry = Entry(update_window)
    email_entry.grid(row=2, column=1)
    email_entry.insert(0, email)

    def submit_update():
        con = connect_db()
        c = con.cursor()
        try:
            if not (name_entry.get() and phone_entry.get() and email_entry.get()):
                raise ValueError("All fields are required!")
            if len(phone_entry.get()) != 10 or not phone_entry.get().isdigit():
                raise ValueError("Phone number must be 10 digits long!")

            c.execute("UPDATE CONTACTS SET NAME=?, PHONENUMBER=?, EMAIL=? WHERE SLNO=?",
                      (name_entry.get(), phone_entry.get(), email_entry.get(), slno))
            con.commit()
            messagebox.showinfo("Success", "Contact updated successfully!")
            update_window.destroy()
            refresh_contacts()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            con.close()

    Button(update_window, text="Update", command=submit_update).grid(row=3, column=0, columnspan=2, pady=10)

def add_contact():
    add_window = Toplevel()
    add_window.title("Add Contact")
    add_window.geometry("350x200")

    Label(add_window, text="First Name").grid(row=0, column=0, pady=5)
    Label(add_window, text="Last Name").grid(row=1, column=0, pady=5)
    Label(add_window, text="Phone Number").grid(row=2, column=0, pady=5)
    Label(add_window, text="Email").grid(row=3, column=0, pady=5)

    fname_entry = Entry(add_window)
    fname_entry.grid(row=0, column=1)
    lname_entry = Entry(add_window)
    lname_entry.grid(row=1, column=1)
    phone_entry = Entry(add_window)
    phone_entry.grid(row=2, column=1)
    email_entry = Entry(add_window)
    email_entry.grid(row=3, column=1)

    def submit():
        con = connect_db()
        c = con.cursor()
        try:
            if not (fname_entry.get() and lname_entry.get() and phone_entry.get() and email_entry.get()):
                raise ValueError("All fields are required!")
            if len(phone_entry.get()) != 10 or not phone_entry.get().isdigit():
                raise ValueError("Phone number must be 10 digits long!")

            full_name = f"{fname_entry.get()} {lname_entry.get()}"
            c.execute("INSERT INTO CONTACTS (NAME, PHONENUMBER, EMAIL) VALUES (?, ?, ?)",
                      (full_name, phone_entry.get(), email_entry.get()))
            con.commit()
            messagebox.showinfo("Success", "Contact added successfully!")
            add_window.destroy()
            refresh_contacts()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            con.close()

    Button(add_window, text="Submit", command=submit).grid(row=4, column=0, columnspan=2, pady=5, padx=10)

def create_action_buttons(index, slno, name, phone, email):
    row_frame = Frame(button_frame)
    row_frame.grid(row=index, column=0, sticky="w", pady=0) 

    delete_btn = Button(row_frame, text="Delete", command=lambda: delete_contact(slno), width=5,fg="red")
    delete_btn.pack(side=LEFT, padx=5)

    update_btn = Button(row_frame, text="Update", command=lambda: update_contact(slno, name, phone, email), width=7)
    update_btn.pack(side=LEFT)

root = tk.Tk()
root.title("Contact Manager")
root.geometry("800x500")  
root.minsize(800, 400)

Label(root, text="Contact Manager", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

main_frame = Frame(root)
main_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

table_frame = Frame(main_frame)
table_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

button_frame = Frame(main_frame)
button_frame.grid(row=0, column=2, sticky="ns", padx=10, pady=25)  

columns = ("SLNO", "NAME", "PHONENUMBER", "EMAIL")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")

tree.heading("SLNO", text="SLNO")
tree.heading("NAME", text="NAME")
tree.heading("PHONENUMBER", text="PHONENUMBER")
tree.heading("EMAIL", text="EMAIL")

tree.column("SLNO", width=50, anchor=CENTER)
tree.column("NAME", width=150, anchor=W)
tree.column("PHONENUMBER", width=100, anchor=CENTER)
tree.column("EMAIL", width=200, anchor=W)

tree.pack(expand=True, fill=BOTH)

refresh_contacts()

Button(root, text="Add Contact", command=add_contact).grid(row=2, column=0, columnspan=2, pady=10)

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
