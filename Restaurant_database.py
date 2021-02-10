import pandas as pd


# Read in customer csv file
customers = pd.read_csv('/Users/xuehanyin/coursework/comp5000/restaurant_files/train_customers.csv')
customers


# Cleaning data
# Choose akeed_customer_id as primary key
# Test if the column akeed_customer_id is unique
customers.akeed_customer_id.value_counts()
# This column is not unique e.g. OFOCFVI returns 17 times

# Delete rows that has the same value in column akeed_customer_id 
customers_1 = customers.drop_duplicates(subset = 'akeed_customer_id').reset_index(drop = True)


import sqlite3


# Create a database and connect to it
conn = sqlite3.connect('/Users/xuehanyin/coursework/comp5000/restaurant.db')

# Create a cursor
cursor = conn.cursor()

# Design the table and set akeed_customer_id as primary key
cursor.execute("""CREATE TABLE customers (
    akeed_customer_id text PRIMARY KEY,
    gender text,
    dob integer,
    language text,
    created_at numeric
    
    ) """)


conn.commit()


# Insert rows into database
for index,row in customers_1.iterrows():
    param = """INSERT INTO customers 
    (akeed_customer_id, gender, dob, language,
    created_at)
    VALUES (?,?,?,?,?);"""
    
    data_tuple = (row['akeed_customer_id'], row['gender'], row['dob'], 
    row['language'],row['created_at'])
    
    cursor.execute(param, data_tuple)
    
    
conn.commit()



#-----------------------------------------------------
# Read in lication csv file
locations = pd.read_csv('/Users/xuehanyin/coursework/comp5000/restaurant_files/train_locations.csv')
locations


# Choose customer_id and location_number as composite key
# Test if they are unique
col_lo = locations[locations.duplicated(subset = ['customer_id', 'location_number'], keep = False)]
# No value is returned


# Create the address table
cursor.execute("""CREATE TABLE address (
  customer_id text,
  location_number integer,
  location_type text,
  latitude real,
  longitude real,
  PRIMARY KEY(customer_id, location_number),
  FOREIGN KEY (customer_id) REFERENCES customers (akeed_customer_id))""")

conn.commit()

# Insert rows into table
for index, row in locations.iterrows():
    param = """INSERT INTO address
    (customer_id, location_number,location_type,latitude,longitude)
    VALUES (?,?,?,?,?);"""
    
    data_tuple = (row['customer_id'], row['location_number'],
                  row['location_type'], row['latitude'],row['longitude'])
    
    cursor.execute(param,data_tuple)

conn.commit()




#-----------------------------------------------------
# Read in vender csv file
vendors = pd.read_csv('/Users/xuehanyin/coursework/comp5000/restaurant_files/vendors.csv')


# check duplicated values
col_vendor = vendors[vendors.duplicated(subset = 'id', keep = False)]
col_vendor
# nothing is printed

cursor.execute("""CREATE TABLE vendors (
  id int PRIMARY KEY,
  authentication_id int,
  latitude real,
  longitude real, 
  vendor_category_en text,
  vendor_category_id int,
  delivery_charge real,
  serving_distance int,
  is_open numeric,
  OpeningTime numeric,
  OpeningTime2 numeric,
  prepration_time int,
  discount_percentage int,
  vendor_rating real
  
)""")

conn.commit()


for index,row in vendors.iterrows():
    param = """INSERT INTO vendors (
    id,authentication_id,
    latitude,longitude,vendor_category_en,vendor_category_id,
    delivery_charge,serving_distance,is_open,OpeningTime,OpeningTime2,
    prepration_time, discount_percentage,vendor_rating) 
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
    
    data_tuple = (row['id'],row['authentication_id'],row['latitude'],
                  row['longitude'],row['vendor_category_en'],
                  row['vendor_category_id'],row['delivery_charge'],
                  row['serving_distance'],
                  row['is_open'],row['OpeningTime'],row['OpeningTime2'],
                  row['prepration_time'],row['discount_percentage'],
                  row['vendor_rating'])
    
    cursor.execute(param, data_tuple)
    
conn.commit()




#-----------------------------------------------------
# Read in order csv file
orders = pd.read_csv('/Users/xuehanyin/coursework/comp5000/restaurant_files/orders.csv')


# Check duplicated values
orders.akeed_order_id.value_counts()
# akeed_order_id is not unique it has NAs in the column


# Add an index to order as order ID
orders['order_index'] = range(1,len(orders)+1)

# avoid space in column name
orders['CID_and_LOC_NUM_and_VENDOR'] = orders['CID X LOC_NUM X VENDOR']


cursor.execute("""CREATE TABLE orders (
   order_index int PRIMARY KEY,
   akeed_order_id int,
   customer_id text,
   vendor_id int,
   item_count int,
   grand_total real,
   payment_mode int,
   promo_code text,
   vendor_discount_amount real,
   promo_code_discount_percentage int,
   delivery_distance real,
   delivery_time numeric,
   order_accepted_time numeric,
   driver_accepted_time numeric,
   ready_for_pickup_time numeric,
   picked_up_time numeric,
   delivered_time numeric,
   delivery_date numeric,
   created_at numeric,
   LOCATION_NUMBER int,
   CID_and_LOC_NUM_and_VENDOR text,
   FOREIGN KEY (customer_id) REFERENCES customers (akeed_customer_id),
   FOREIGN KEY (vendor_id) REFERENCES vendors (id))""")

conn.commit()


for index, row in orders.iterrows():
    param = """ INSERT INTO orders (
    order_index,
    akeed_order_id,
    customer_id,
    vendor_id,
    item_count,
    grand_total,
    payment_mode,
    promo_code,
    vendor_discount_amount,
    promo_code_discount_percentage,
    delivery_distance,
    delivery_time,
    order_accepted_time,
    driver_accepted_time,
    ready_for_pickup_time,
    picked_up_time,
    delivered_time,
    delivery_date,
    created_at,
    LOCATION_NUMBER,
    CID_and_LOC_NUM_and_VENDOR)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
    
    data_tuple = (row['order_index'], row['akeed_order_id'],row['customer_id'],
                 row['vendor_id'],row['item_count'],row['grand_total'],
                 row['payment_mode'],row['promo_code'],row['vendor_discount_amount'],
                 row['promo_code_discount_percentage'],row['deliverydistance'],row['delivery_time'],
                 row['order_accepted_time'],row['driver_accepted_time'],row['ready_for_pickup_time'],
                 row['picked_up_time'],row['picked_up_time'],row['delivered_time'],
                 row['created_at'],row['LOCATION_NUMBER'],row['CID_and_LOC_NUM_and_VENDOR'])
    
    cursor.execute(param, data_tuple)


conn.commit()

conn.close()




    







