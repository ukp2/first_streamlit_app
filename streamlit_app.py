import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('Heheh, działa')
streamlit.text('first line of text')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show) # old: streamlit.dataframe(my_fruit_list)

# Fruity response - 3 wersje : 
      ## Odl section - replaced with try-except : 
# streamlit.header("Fruityvice Fruit Advice!")
# fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
# streamlit.write('The user entered ', fruit_choice)
# import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) #pandas used to normalize
# streamlit.dataframe( fruityvice_normalized ) #wsadza znormalizowane w tabelke
      ## New Try-except section - replaced with function: 
# streamlit.header("Fruityvice Fruit Advice!")
# try:
#   fruit_choice = streamlit.text_input('What fruit would you like information about?')
#   if not fruit_choice:
#     streamlit.error("Please select a fruit")
#   else: 
#     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#     fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#     streamlit.dataframe( fruityvice_normalized )
# except URLError as e:
#   streamlit.error()
      ## New section - Function
#create the repetable code block (called function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
            streamlit.error("Please select a fruit")
  else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

#import snowflake.connector - 2 wersje
      ##before
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * from fruit_load_list")
# my_data_row = my_cur.fetchall()  #fetchall
# streamlit.header("The fruit load list contains:")
# streamlit.dataframe(my_data_row)

      ##with function and button that calls function and load data:
#function
streamlit.header("The fruit load list contains:")    
def get_fruit_load_list():
      with my_cnx.cursor() as my_cur:
            my_cur.execute("SELECT * from fruit_load_list")
            return my_cur.fetchall()
 #add a button
if streamlit.button('Get Fruit Load List'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      my_data_row = get_fruit_load_list()
      streamlit.dataframe(my_data_row) 
      
      
# #don't run anything past here while we troubleshoot
# streamlit.stop()

#Allow end user to add an fruit to the list
      ##old
# add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
# streamlit.write('Thanks for adding ', add_my_fruit)
# my_cur.execute("insert into pc_rivery_db.public.FRUIT_LOAD_LIST VALUES ('test_streamlit')" )
      ##new - funkcja i guzik :
def insert_row_snowflake(new_fruit):
      with my_cnx.cursor() as my_cur: 
            my_cur.execute("insert into pc_rivery_db.public.FRUIT_LOAD_LIST VALUES('"+new_fruit+"')")
            return "Thanks for adding "+ new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      back_from_function = insert_row_snowflake(add_my_fruit)
      streamlit.text(back_from_function)

      
## metadata info
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()") # metadata
# my_data_row_0 = my_cur.fetchone() #fetchone
# streamlit.text("Snowflake metadata:")
# streamlit.text(my_data_row_0)
