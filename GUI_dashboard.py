import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sqlite3

conn = sqlite3.connect('/Users/xuehanyin/coursework/comp5000/restaurant.db')

df = pd.read_sql_query("SELECT item_count, grand_total, delivery_distance FROM orders", conn)

conn.close()


from tkinter import *

root = Tk()
root.geometry("200x100")

root.title('Click the button!')

def graph():
    dd = df['delivery_distance']
    plt.hist(dd)
    plt.show()
    
    ic = df['item_count'].mean()
    print(ic)
    
    gt = df['grand_total'].mean()
    print(gt)
    

button = Button(root, text = 'click it!', command = graph)
button.pack()


root.mainloop()