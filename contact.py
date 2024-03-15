from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3 as sq
root= tk.Tk()
root.title("create contact")
root.geometry("400x400")
con= sq.connect('phone.db')
c=con.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS CONTACTS (
            SLNO INTEGER PRIMARY KEY AUTOINCREMENT ,
            NAME CHAR(100) NOT NULL,
            PHONENUMBER INTEGER(10),
            EMAIL TEXT NOT NULL
)""")
def delete():
    con= sq.connect('phone.db')
    c=con.cursor()
    c.execute("DELETE from CONTACTS WHERE SLNO="+dele.get())
    dele.delete(0,END) 
    
    con.commit()
    con.close()

def add():
    root2=Tk()
    root2.title("details")
    root2.geometry("350x200")
    firstname=Label(root2,text="First name").grid(row=0,column=0,pady=5)
    lastname=Label(root2,text="Last name").grid(row=1,column=0,pady=5)
    phlabel=Label(root2,text="Phone number").grid(row=2,column=0,pady=5)
    emaillabel=Label(root2,text="EmailID").grid(row=3,column=0,pady=5)

    def submit():
        con= sq.connect('phone.db')
        c=con.cursor()
        if  len(fname.get())==0:
            label2=Label(root2,text="*enter first name").grid(row=0,column=2,padx=20)
        elif len(lname.get())==0:
            label3=Label(root2,text="*enter last name").grid(row=1,column=2,padx=20)
        elif len(ph.get())!=10:
            label4=Label(root2,text="*invalid ph.no").grid(row=2,column=2,padx=20)
        elif len(email.get())==0:
            label5=Label(root2,text="*invalid emialID").grid(row=3,column=2,padx=20)
        else:
            c.execute("INSERT INTO CONTACTS(NAME,PHONENUMBER,EMAIL) VALUES(?|| ?,?,?)",(fname.get(),lname.get(),ph.get(),email.get()))
            root2.destroy()

    
        con.commit()
        con.close()

        fname.delete(0,END)
        lname.delete(0,END)
        ph.delete(0,END)
        email.delete(0,END)
    
        
    b1=Button(root2,text="submit",command=submit).grid(row=4,column=0,columnspan=2,pady=5,padx=10)
    
    fname=Entry(root2)
    fname.grid(row=0,column=1)
    lname=Entry(root2)
    lname.grid(row=1,column=1)
    ph=Entry(root2)
    ph.grid(row=2,column=1)
    email=Entry(root2) 
    email.grid(row=3,column=1)
    
    root2.mainloop()
 

con= sq.connect('phone.db')
c=con.cursor()
c.execute("SELECT * from CONTACTS")
records=c.fetchall()
global count
count=0
for x in records:
    print(x)
printrecord =''
for x in records:
    printrecord += str(x[0]) +"  "+str(x[1]) + "\n"
def table():
    root=tk.Tk()
    root.title("CONTACTS")
    root.geometry("700x500")
    tree=ttk.Treeview(root) 
    tree["columns"]=(1,2,3,4)
    tree.heading(1,text="SLNO")
    tree.heading(2,text="NAME")
    tree.heading(3,text="PHONENUMBER")
    tree.heading(4,text="EMAIL")
    tree.column("#0",width=0,stretch=NO)
    tree.column("1",width=50)
    tree.column("3",width=150)
    cursor=con.execute("SELECT * from CONTACTS")
    i=0
    for row in cursor:
        tree.insert('',i,text= str(row[0]),values=(row[0],row[1],row[2],row[3]))
        i+=1
    tree.pack()
display=tk.Button(root,text="show contacts",command=lambda:table()).grid(row=9,pady=5)

dele=Entry(root)
dele.grid(row=3,column=1,padx=0)
label=Label(root,text="Contact").grid(row=0,column=0,sticky=NW)
b3=Button(root,text="delete",command=delete).grid(row=3,column=2,columnspan=2,pady=7,padx=20,sticky=NW)
d=Label(root,text="Enter row no").grid(row=3,column=0,padx=30)
b4=Button(root,text="Create new contact",command=add).grid(row=1,column=0,columnspan=2,pady=5,padx=40,sticky=NW)


root.mainloop()


