from os import error, name, write
from tkinter import Button, Label, LabelFrame, PhotoImage, Tk ,W,E,N,S,Entry,END,StringVar,Scrollbar,Toplevel
from tkinter import ttk
import sqlite3
import pandas as pd




class Accounts:
    db_filename = 'C:/Users/lenovo/Desktop/Space Invaders GAME/projects/app/App.db'
    
    def __init__(self,root):
        self.root = root
        self.create_gui()
        ttk.Style = ttk.Style()
        ttk.Style.configure("Treeview",font=('helvetica',10))
        ttk.Style.configure("Treeview.Heading",font=('helvetica',11,'bold'))
    
    def execute_db_query(self,query,parameters=()):
        with sqlite3.connect(self.db_filename) as conn:
            print(conn)
            print('you have successfully connected to the Database')
            self.cursor = conn.cursor()
            query_result = self.cursor.execute(query,parameters)
            conn.commit()   
        return query_result
    
    def create_gui(self):
        #self.create_left_icon()
        self.create_label_frame()
        self.create_tree_view()
        self.create_scrollbar()
        self.view_accounts()
        self.create_message_area()
        self.create_button_buttons()

    def create_button_buttons(self):
        Button(text='Delet Selected',command=self.on_delet_selected_button_clicked,bg='red',fg='white').grid(row=8,column=0,sticky=W,pady=10)
        Button(text='Edit selected',command=self.on_modify_selected_button_clicked,bg='purple',fg='white').grid(row=8,column=1,sticky=W)

            
    def create_tree_view(self):
        self.tree = ttk.Treeview(height=10,style="Treeview")
        self.tree.grid(row=6,column=0,columnspan=3)
        self.tree.heading('#0',text='Name',anchor=W)
        

        
    def create_scrollbar(self):
        self.scrollbar = Scrollbar(orient='vertical',command=self.tree.yview)
        self.scrollbar.grid(row=6,column=2,columnspan=3,rowspan=10,sticky="sn")

    def create_message_area(self):
        self.message = Label(text='',fg='red')
        self.message.grid(row=3,column=0,sticky=W)


    def create_label_frame(self) :
        labelframe = LabelFrame(self.root, text='Add account', bg="sky blue", font="helvetica 10")
        labelframe.grid(row=0, column=0, padx=8, pady=8, sticky='ew')
        Label(labelframe, text='Name : ', bg="green", fg="white").grid(row=1, column=1, sticky=W, pady=2, padx=15)
        self.namefield = Entry(labelframe)
        self.namefield.grid(row=1, column=2, sticky=W, padx=5,)
        Button(labelframe, text="Add account", command=self.Add_account, bg="blue", fg="white").grid(row=4, column=2, sticky=E, padx=5, pady=5) 

    def Add_account(self):
        if self.add_account_v():
            s = self.namefield.get().strip().replace(" ","_")
            query = 'CREATE TABLE {} ("no"	INTEGER,"Credit"	NUMERIC,"Debit"	INTEGER,"Date"	date,PRIMARY KEY("no" AUTOINCREMENT))'.format(s)
            self.execute_db_query(query)
            query = 'INSERT INTO Main(name) VALUES("{}")'.format(self.namefield.get())
            
            self.execute_db_query(query)
            self.message['text'] = 'New account {} added'.format(self.namefield.get())
            self.namefield.delete(0, END)
            self.view_accounts()
        else:
            self.message['text'] = 'name can not be blank'
            self.view_accounts()
            
            
    def view_accounts(self):
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        query = 'SELECT * FROM Main ORDER BY name desc'
        contact_entries = self.execute_db_query(query)
        for row in contact_entries:
                self.tree.insert('', 0, text=row[0])
            
    def add_account_v(self):
        return len(self.namefield.get()) != 0
            
    def delete_account(self):
        self.message['text']=''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM Main Where name = ?'
        self.execute_db_query(query,(name,))
        query = 'drop table {}'.format(name.replace(" ","_"))
        self.execute_db_query(query)
        
        self.message['text']='Account for {} deleted'.format(name)
        self.view_accounts()

    def on_delet_selected_button_clicked(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']='No item selected to delete'
            return
        self.delete_account()
            
    def open_modify_window(self):
        name = (self.tree.item(self.tree.selection())["text"])
        self.root.destroy()
        self.window = Tk()
        self.window.title('{}'.format(name))
        
        self.tree = ttk.Treeview(height=10 , columns=(1,2),style="Treeview")
        labelframe = LabelFrame(self.window, text='{}'.format(name), bg="sky blue", font="helvetica 10")
        labelframe.grid(row=0, column=0, padx=8, pady=8, sticky='ew')
        Label(labelframe, text='Date : ', bg="green", fg="white").grid(row=1, column=1, sticky=W, pady=2, padx=15)
        self.namefield = Entry(labelframe)
        self.namefield.grid(row=1, column=2)
        self.namefield.grid(row=1, column=2, sticky=W, padx=5,)
        Label(labelframe, text='Credit : ', bg="green", fg="white").grid(row=2, column=1, sticky=W, pady=2, padx=15)
        self.creditfield = Entry(labelframe)
        self.creditfield.grid(row=2, column=2, sticky=W, padx=5,)
        Label(labelframe, text='Debit : ', bg="green", fg="white").grid(row=3, column=1, sticky=W, pady=2, padx=15)
        self.Debitfield = Entry(labelframe)
        self.Debitfield.grid(row=3, column=2, sticky=W, padx=5,)
        
        Button(self.window, text='update', command=lambda: self.update_account(
            self.creditfield.get(), self.Debitfield.get(),self.namefield.get(),name.replace(" ","_")), bg = "blue",fg="white").grid(row=3, column=0, sticky=E)
        

        
        self.tree.grid(row=6,column=0,columnspan=3)
        self.tree.heading('#0',text='Credit',anchor=W)
        self.tree.heading("1",text="Debit",anchor=W)
        self.tree.heading("2",text="Date",anchor=W)
        
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        query = 'SELECT * FROM {} order by Date desc'.format(name.replace(" ","_"))
        contact_entries = self.execute_db_query(query)
        for row in contact_entries:
                self.tree.insert('',0,text = row[1], values=(row[2],row[3],row[0],row[1]))
                
        Button(text='Delete Selected',command=lambda: self.delete_data(name.replace(" ","_")),bg='red',fg='white').grid(row=8,column=0,sticky=W,pady=10,padx=10)
        Button(text='Edit selected',command=lambda: self.open_modify(name.replace(" ","_")),bg='purple',fg='white').grid(row=8,column=1,sticky=W)
        Button(text='Exoprt to Excel',command=lambda: self.export_to_exel(name.replace(" ","_")),bg='blue',fg='white').grid(row=9,column=1,sticky=W)
    
    def open_modify(self,name):
        index = self.tree.item(self.tree.selection())['values'][2]
        credit = self.tree.item(self.tree.selection())['values'][3]
        Date = self.tree.item(self.tree.selection())['values'][1]
        Debit = self.tree.item(self.tree.selection())['values'][0]
        self.window = Toplevel()
        self.window.title('Update Contact')
        Label(self.window,text='Credit:').grid(row=0,column=1)
        c = Entry(self.window, textvariable=StringVar(self.window, value=credit))
        c.grid(row=0, column=2)
        Label(self.window, text='Date:').grid(row=1, column=1)
        date = Entry(self.window, textvariable=StringVar(self.window, value=Date))
        date.grid(row=1, column=2)
        Label(self.window, text='Debit:').grid(row=2, column=1)
        d = Entry(self.window,textvariable=StringVar(self.window, value=Debit))
        d.grid(row=2, column=2)


        Button(self.window, text='Update Contact', command=lambda: self.update_contacts(
            d.get(),date.get(), c.get(),index,name)).grid(row=3, column=2, sticky=E)
        

        self.window.mainloop()

    def update_contacts(self, d, date,c,index,name):
        query = 'UPDATE {0} SET credit = ? , debit = ? , date = ? where no = {1}'.format(name,index)
        parameters = (c, d, date)
        self.execute_db_query(query, parameters)
        self.window.destroy()
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        query = 'SELECT * FROM {} order by Date desc'.format(name.replace(" ","_"))
        contact_entries = self.execute_db_query(query)
        for row in contact_entries:
                self.tree.insert('',0,text = row[1], values=(row[2],row[3],row[0],row[1]))
        
    def update_account(self, c, d,date,name):
        query = 'INSERT INTO {}(Credit,Debit,Date) VALUES(?,?,?)'.format(name)
        Parameter = (c,d,date)
        self.execute_db_query(query,Parameter)
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        query = 'SELECT * FROM {} order by Date desc'.format(name.replace(" ","_"))
        contact_entries = self.execute_db_query(query)
        for row in contact_entries:
                self.tree.insert('',0,text = row[1], values=(row[2],row[3],row[0],row[1]))
        self.namefield.delete(0, END)
        self.creditfield.delete(0, END)
        self.Debitfield.delete(0, END)         


    def on_modify_selected_button_clicked(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']='No item selected to modify'
            return
        self.open_modify_window()

    def delete_data(self,name):
        index = self.tree.item(self.tree.selection())['values'][2]
        query = 'DELETE FROM {0} Where no = {1}'.format(name,index)
        self.execute_db_query(query)
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        query = 'SELECT * FROM {} order by Date desc'.format(name)
        contact_entries = self.execute_db_query(query)
        for row in contact_entries:
                self.tree.insert('',0,text = row[1], values=(row[2],row[3],row[0],row[1]))
                
    def export_to_exel(self,name):
        #filepath = "C:/Users/lenovo/Desktop/Space Invaders GAME/projects/{}.xlsx".format(name)
        conn = sqlite3.connect('C:/Users/lenovo/Desktop/Space Invaders GAME/projects/app/App.db')
        
        df = pd.read_sql("SELECT * FROM {}".format(name),conn)
        writer = pd.ExcelWriter("C:/Users/lenovo/Documents/app_data/{}.xlsx".format(name))
        
        df.to_excel(writer)
        
        writer.save()

        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        query = 'SELECT * FROM {} order by Date desc'.format(name)
        contact_entries = self.execute_db_query(query)
        for row in contact_entries:
                self.tree.insert('',0,text = row[1], values=(row[2],row[3],row[0],row[1]))
            
                
        
        
            
            
            

if __name__ == '__main__':
    root =Tk()
    root.title('Your Accountant')
    application = Accounts(root)
    root.geometry("350x450")
    root.resizable(width=False, height=False)
    root.mainloop()
     