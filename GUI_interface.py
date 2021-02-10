# Making GUI interface
from tkinter import *


root = Tk()

# create a title
root.title('Add new customer!')

# Create entry boxes
gender = Entry(root, width = 30)
gender.grid(row = 0, column = 1, padx = 20)

dob = Entry(root, width = 30)
dob.grid(row = 1, column = 1, padx = 20)

language = Entry(root, width = 30)
language.grid(row = 2, column = 1, padx = 20)



# Create entry box labels
gender_label =  Label(root, text = 'Gender:')
gender_label.grid(row = 0, column = 0)

dob_label =  Label(root, text = 'Date of Birth:')
dob_label.grid(row = 1, column = 0)

language_label =  Label(root, text = 'Language:')
language_label.grid(row = 2, column = 0)



# connect to the database
conn = sqlite3.connect('/Users/xuehanyin/coursework/comp5000/restaurant.db')

# create a cursor    
c = conn.cursor()


# create unrepetetive 7 digits customer_id with uppercase letter and numbers
import random
def ran():
    a = random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", 7)
    code = ""
    code = code.join(a)
    return code


# get current time
from datetime import datetime

now = datetime.now()
    
current = now.strftime("%Y-%m-%d %H:%M:%S")


# Create submit funtion for database
def submit():
    # connect to the database
    conn = sqlite3.connect('/Users/xuehanyin/coursework/comp5000/restaurant.db')
    
    c = conn.cursor()
    
    c.execute("INSERT INTO customers VALUES (:akeed_customer_id, :gender, :dob, :language, :created_at)",
             {
                 'akeed_customer_id':ran(),
                 'gender':gender.get(),
                 'dob':dob.get(),
                 'language':language.get(),
                 'created_at':current
                 
             })
    
    
    conn.commit()
    
    # close the database 
    conn.close()
    
    
    # erase the input value in the entry box
    gender.delete(0,END)
    dob.delete(0,END)
    language.delete(0,END)
    
    
# Create button
submit_btn = Button(root, text = "Add", command = submit)
submit_btn.grid(row = 9, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100)


conn.commit()

# close the database
conn.close()

# pop out the window
root.mainloop()
    