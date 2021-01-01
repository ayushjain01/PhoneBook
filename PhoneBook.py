from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

# Developed by AYUSH JAIN(Codangle)
# Follow @codangle on Instagram

# _______________________________CLASS_________________________________#


class PhoneBook:
    def __init__(self, window, con):
        self.con = con
        self.cursor = self.con.cursor()
        #__________________WINDOW SETTINGS____________________#
        self.window = window
        self.window.title("PhoneBook")
        self.clear(self.window)
        width = 900
        height = 600
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.window.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.window.resizable(0, 0)
        self.window.config(bg="#00B0AA")
        self.style = ttk.Style(self.window)
        self.style.theme_use("default")
        self.style.configure("Treeview", background="#00B0AA",
                             fieldbackground="#F7D0FF", foreground="#000000")
        self.style.configure(
            "Treeview.Heading", background="#F0FFF4", font=("Yu Gothic Light", 10))
        #___________________TITLE LABEL______________________#

        self.titlelable = Label(self.window, text="PhoneBook", font=(
            "Gabriola", 18), bg="#00B0AA", fg="#14213d")
        self.titlelable.pack(pady=5)

        #_____________________BUTTONS________________________#

        self.addbut = Button(self.window, text="Add", relief=FLAT, activebackground="#1BFF1E", font=(
            "Yu Gothic Light", 10), bg="#8AFF1B", fg="#14213d", command=self.addgui)
        self.addbut.place(x=50, y=20)
        self.delbut = Button(self.window, text="Delete", relief=FLAT, activebackground="#FF200E", activeforeground="#FFFFFF", font=(
            "Yu Gothic Light", 10), bg="#FF2525", fg="#FFFFFF", command=self.delete)
        self.delbut.place(x=800, y=20)

        #__________________TREE & SCROLLBAR__________________#
        self.scrollbarx = Scrollbar(self.window, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(self.window, orient=VERTICAL)
        self.tree = ttk.Treeview(
            self.window, height=500, yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set)

        self.scrollbary.config(command=self.tree.yview)
        self.scrollbary.pack(side=RIGHT, fill=Y)
        self.scrollbarx.config(command=self.tree.xview)
        self.scrollbarx.pack(side=BOTTOM, fill=X)
        self.tree["columns"] = ("1", "2", "3", "4", "5", "6", "7")
        self.tree['show'] = 'headings'
        self.tree.column("1", width=170, anchor='se')
        self.tree.column("2", width=170, anchor='se')
        self.tree.column("3", width=150, anchor='se')
        self.tree.column("4", width=150, anchor='se')
        self.tree.column("5", width=200, anchor='se')
        self.tree.column("6", width=150, anchor='se')
        self.tree.column("7", width=250, anchor='se')

        self.tree.heading("1", text="FirstName")
        self.tree.heading("2", text="Lastname")
        self.tree.heading("3", text="Mobile")
        self.tree.heading("4", text="Phone")
        self.tree.heading("5", text="Email")
        self.tree.heading("6", text="Instagram")
        self.tree.heading("7", text="Notes")

        self.tree.pack()
        self.add()
        self.window.mainloop()

    def clear(self, window):
        x = window.winfo_children()
        for i in x:
            i.destroy()

    def add(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.cursor.execute(
                "SELECT * FROM CONTACTS_TABLE ORDER BY First_Name ASC")
            fetch = self.cursor.fetchall()
            for data in fetch:
                self.tree.insert('', 'end', values=(data))
        except TclError:
            pass

    def delete(self):
        if not self.tree.selection():
            result = tkMessageBox.showwarning(
                'Error : No Contact Selected', 'Please Select Something First!', icon="warning")
        else:
            result = tkMessageBox.askquestion(
                'Warning', 'Are you sure you want to delete this record?', icon="warning")
            if result == 'yes':
                curItem = self.tree.focus()
                contents = (self.tree.item(curItem))
                selecteditem = contents['values']
                self.tree.delete(curItem)
                self.cursor.execute(
                    f"DELETE FROM CONTACTS_TABLE WHERE Mobile_Number = {selecteditem[2]}")
                self.con.commit()
                self.add()

    def intcheck(self, num):
        for i in num:
            print(i)
            if ord(i) > 57 or ord(i) < 48:
                return False
        return True

    def callinit(self):
        self.__init__(self.window, self.con)

    def addgui(self):
        def save():
            #__________________VARIABLES____________________#
            FN = self.FIRSTNAME.get()
            LN = self.LASTNAME.get()
            MN = self.MOBILE.get()
            PN = self.PHONE.get()
            EI = self.EMAIL.get()
            IH = self.INSTA.get()
            NS = self.E7.get("1.0", 'end-1c')

            if FN == "" or LN == "" or MN == "" or PN == "" or EI == "" or IH == "" or NS == "":
                result = tkMessageBox.showwarning(
                    'Error : All Fields Not Filled', 'Please Complete The Required Fields', icon="warning")
            print(self.intcheck(MN), self.intcheck(PN))
            if self.intcheck(MN) == False or self.intcheck(PN) == False:

                result = tkMessageBox.showwarning('Error : Invalid Mobile or Phone Number',
                                                  'Please Check The Mobile or Phone Number. No special Characters or Letters allowed.', icon="warning")

            else:
                self.cursor.execute(
                    f'SELECT * FROM CONTACTS_TABLE WHERE Mobile_Number = {int(MN)}')
                res = self.cursor.fetchall()
                if len(res) == 0:

                    print(
                        F"""INSERT INTO CONTACTS_TABLE VALUES({FN},{LN},{MN},{PN},{EI},{IH},{NS})""")

                    self.cursor.execute(F"""INSERT INTO CONTACTS_TABLE VALUES(
                                    '{FN}','{LN}',{MN},{PN},'{EI}','{IH}','{NS}')
                                    """)
                    self.con.commit()

                    self.clear(self.window)
                    self.__init__(self.window, self.con)
                    self.add()
                else:
                    result = tkMessageBox.showwarning(
                        'Error : Contact Exists', 'A Contact Card with this Mobile Number Already Exists. Please Check.', icon="warning")

        self.clear(self.window)
        self.window.config(bg="#00B0AA")
        self.window.title("New Contact")

        #_________________VARIABLES______________________#

        self.FIRSTNAME = StringVar()
        self.LASTNAME = StringVar()
        self.MOBILE = StringVar()
        self.PHONE = StringVar()
        self.EMAIL = StringVar()
        self.INSTA = StringVar()

        #___________LABELS & ENTRIES & BUTTONS____________#

        self.TitleLabel = Label(self.window, text="New Contact", font=(
            "Gabriola", 18), bg="#00B0AA", fg="#14213d")
        self.TitleLabel.pack()
        self.L1 = Label(self.window, text="First Name", font=(
            "Yu Gothic Light", 10), bg="#00B0AA", fg="#14213d")
        self.E1 = Entry(self.window, textvariable=self.FIRSTNAME,
                        width=40, relief=FLAT, font=("Yu Gothic Light", 10))
        self.L2 = Label(self.window, text="Last Name", font=(
            "Yu Gothic Light", 10), bg="#00B0AA", fg="#14213d")
        self.E2 = Entry(self.window, textvariable=self.LASTNAME,
                        width=40, relief=FLAT, font=("Yu Gothic Light", 10))
        self.L3 = Label(self.window, text="Mobile Number", font=(
            "Yu Gothic Light", 10), bg="#00B0AA", fg="#14213d")
        self.E3 = Entry(self.window, textvariable=self.MOBILE,
                        width=40, relief=FLAT, font=("Yu Gothic Light", 10))
        self.L4 = Label(self.window, text="Phone Number", font=(
            "Yu Gothic Light", 10), bg="#00B0AA", fg="#14213d")
        self.E4 = Entry(self.window, textvariable=self.PHONE,
                        width=40, relief=FLAT, font=("Yu Gothic Light", 10))
        self.L5 = Label(self.window, text="Email Id", font=(
            "Yu Gothic Light", 10), bg="#00B0AA", fg="#14213d")
        self.E5 = Entry(self.window, textvariable=self.EMAIL,
                        width=40, relief=FLAT, font=("Yu Gothic Light", 10))
        self.L6 = Label(self.window, text="Instagram Handle", font=(
            "Yu Gothic Light", 10), bg="#00B0AA", fg="#14213d")
        self.E6 = Entry(self.window, textvariable=self.INSTA,
                        width=40, relief=FLAT, font=("Yu Gothic Light", 10))
        self.L7 = Label(self.window, text="Notes", font=(
            "Yu Gothic Light", 10), bg="#00B0AA", fg="#14213d")
        self.E7 = Text(self.window, width=40, height=4,
                       relief=FLAT, font=("Yu Gothic Light", 10))

        self.B1 = Button(self.window, text="Save", relief=FLAT, activebackground="#1BFF1E", font=(
            "Yu Gothic Light", 10), bg="#8AFF1B", fg="#14213d", command=save)
        self.B2 = Button(self.window, text="Cancel", relief=FLAT, activebackground="#FF200E", activeforeground="#FFFFFF", font=(
            "Yu Gothic Light", 10), bg="#FF2525", fg="#FFFFFF", command=self.callinit)
        #_____________________PLACEMENTS___________________________#
        self.L1.place(x=10, y=60)
        self.E1.place(x=170, y=60)
        self.L2.place(x=10, y=100)
        self.E2.place(x=170, y=100)
        self.L3.place(x=10, y=140)
        self.E3.place(x=170, y=140)
        self.L4.place(x=10, y=180)
        self.E4.place(x=170, y=180)
        self.L5.place(x=10, y=220)
        self.E5.place(x=170, y=220)
        self.L6.place(x=10, y=260)
        self.E6.place(x=170, y=260)
        self.L7.place(x=10, y=300)
        self.E7.place(x=170, y=300)
        self.B1.place(x=240, y=450)
        self.B2.place(x=300, y=450)


root = Tk()
con = sqlite3.connect("Contact.db")

cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS CONTACTS_TABLE(
            First_Name varchar(50),
            Last_Name varchar(50),
            Mobile_Number int PRIMARY KEY,
            Phone_Number int,
            Email_ID varchar(100),
            Instagram_Handle varchar(50),
            Notes longtext)           
            """
            )
cur.execute("DELETE FROM CONTACTS_TABLE")
cur.execute("""INSERT INTO CONTACTS_TABLE VALUES
("Test1","Test1",987642212,12345678,"test1@test1.com","@test1","A Test Contact Card."),
("Test2","Test2",987643312,12343378,"test2@test2.com","@test2","A Test Contact Card.")
""")
cur = PhoneBook(root, con)

