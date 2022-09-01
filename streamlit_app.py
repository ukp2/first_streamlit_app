import streamlit

streamlit.title('Heheh, działa')
streamlit.text('first line of text')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show) # old: streamlit.dataframe(my_fruit_list)

# Fruity response
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) #pandas used to normalize
streamlit.dataframe( fruityvice_normalized ) #wsadza znormalizowane w tabelke




import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()") # metadata
my_data_row_0 = my_cur.fetchone() #fetchone
streamlit.text("Snowflake metadata:")
streamlit.text(my_data_row_0)

my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()  #fetchall
streamlit.header("The fruit load list contains:")
streamlit.text(my_data_row)
streamlit.dataframe(my_data_row)
