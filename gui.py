from tkinter import *
from tkinter.ttk import *
from db_connection import Database

class GUI:

    #constructor to create gui
    def __init__(self):
        self.root = Tk()
        self.root.title("CRUD")
        self.root.minsize(width=360, height=175)

        #optional instruction label
        # self.instructions = Label(text="To make modifications, enter changes directly in entry box. Then click 'update'.")
        # self.instructions.grid(row=0,column=0)

        # self.space = Label(text="")
        # self.space.grid(row=1,column=0)

        self.frame = Frame(self.root)
        self.frame.grid(row=2,column=0)

        self.db = Database()
        self.data = self.db.return_data()

        # create table header
        self.id = Label(self.frame,text='ID',font=('Arial', 15, 'bold'))
        self.id.grid(row=0, column=0)

        self.name = Label(self.frame,text='Name',font=('Arial', 15, 'bold'))
        self.name.grid(row=0, column=1)

        self.age = Label(self.frame,text='Age',font=('Arial', 15, 'bold'))
        self.age.grid(row=0, column=2)

        self.e_grid_data = []

        #create table and populate with data pulled from postgres db
        if len(self.data) > 0:
            # i is rows
            for i in range(len(self.data)):
            # j is columns
                for j in range(len(self.data[0])):
                    self.e = Entry(self.frame,width=15,font=('Arial', 13))
                    self.e.grid(row=(i+1), column=j)
                    self.e.insert(0,self.data[i][j])

            id_entries = sorted(self.e.master.grid_slaves(column=0),key=lambda w: w.grid_info()['row'])
            for i in range(1,len(id_entries)):
                id_entries[i].configure(state=DISABLED)

        #create add button
        self.add = Button(self.frame, text="add", width=9, command=self.save_function)
        self.add.grid(row=(len(self.data)+1),column=0)

        #create update button
        self.update = Button(self.frame,text="update",width=9)
        self.update.bind("<Button-1>", self.update_function)
        self.update.grid(row=(len(self.data)+1),column=1)

        self.delete = Button(self.frame, text="delete", width=9, command=self.delete_function)
        self.delete.grid(row=(len(self.data)+1), column=2)

        self.root.mainloop()

    def update_function(self,event):
        widgets = []
        new_data = []
        for i in range(1,len(self.data)+1):
            widgets.append(sorted(self.e.master.grid_slaves(row=i),key=lambda w: w.grid_info()['column']))
            new_data.append(widgets[i - 1][1].get())
            new_data.append(widgets[i - 1][2].get())

        self.db.cursor.execute("delete from table1;")

        for i in range(0,len(new_data),2):
            self.db.cursor.execute("insert into table1 (id,name,age) values(%s,%s,%s);",
                                   (self.db.primary_key(),new_data[i],new_data[i+1]))

        self.db.submit()

        self.update_window = Tk()
        self.update_window.title("Update")
        self.update_window.minsize(width=150, height=50)

        self.update_id = Label(self.update_window,text="    Update succesful")
        self.update_id.grid(row=0,column=1)

        self.update_button = Button(self.update_window, text="Close", command=self.update_data)
        self.update_button.grid(row=3, column=0, columnspan=2)
        self.update_window.mainloop()

    def update_data(self):

        self.update_window.destroy()
        self.root.destroy()
        self.__init__()

    # def widgets_per_row(self,widget):
    #     row = widget.grid_info()['row']
    #     return sorted(widget.master.grid_slaves(row=row),
    #                   key=lambda w: w.grid_info()['column'])

    def delete_function(self):
        self.delete_window = Tk()
        self.delete_window.title("delete")
        self.delete_window.minsize(width=200, height=50)

        self.delete_id = Label(self.delete_window,text="ID to delete")
        self.delete_id.grid(row=0,column=0)

        self.delete_input = Entry(self.delete_window)
        self.delete_input.grid(row=0,column=1)

        self.delete_button = Button(self.delete_window, text="Submit", command=self.delete_data)
        self.delete_button.grid(row=1, column=0, columnspan=2)

        self.delete_window.mainloop()

    def delete_data(self):
        id = int(self.delete_input.get())
        self.delete_window.destroy()
        self.db.cursor.execute(
            f"delete from table1 where id={id}"
        )
        self.db.submit()

        for i in range(id,len(self.db.return_data())+1):
            self.db.cursor.execute(
                f"update table1 set id={i} where id={i+1}"
            )
            self.db.submit()
        self.root.destroy()
        self.__init__()

    #creates popup window when user clicks on the "add" button

    def save_function(self):
        self.save_window = Tk()
        self.save_window.title("Insert")
        self.save_window.minsize(width=200, height=50)

        self.save_name = Label(self.save_window, text='name')
        self.save_name.grid(row=0, column=0)
        self.save_age = Label(self.save_window, text='age')
        self.save_age.grid(row=1, column=0)

        self.name_input = Entry(self.save_window, width=10, font=('Arial', 14, 'bold'))
        self.name_input.grid(row=0, column=1)
        self.age_input = Entry(self.save_window, width=10, font=('Arial', 14, 'bold'))
        self.age_input.grid(row=1,column=1)

        self.save_button = Button(self.save_window, text="Submit", command=self.save_data)
        self.save_button.grid(row=3,column=0,columnspan=2)

        self.save_window.mainloop()

    #takes user input from save function window and inserts it into the postgres db
    def save_data(self):
        self.new_name = self.name_input.get()
        self.new_age = int(self.age_input.get())
        self.save_window.destroy()

        self.db.cursor.execute(
                "insert into table1 (id,name,age) values(%s,%s,%s);", (self.db.primary_key(), self.new_name, self.new_age)
            )
        self.db.submit()

        self.root.destroy()
        self.__init__()

    def close(self):
        self.db.terminate()
