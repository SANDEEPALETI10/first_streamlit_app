import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 and Blueberry Oatmeal')
streamlit.text('🥗 Kale , Spinach and rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-range Egg')

streamlit.text('🥑🍞 Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')   


fruits_selected = streamlit.multiselect("Pick Some Fruits:" , list(my_fruit_list.index),['Avocado' , 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show) 

#new section to display fruity vice response
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  




streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
   


except URLError as e:
  streamlit.error()


    
    
    
   
  
streamlit.write('The user entered ', fruit_choice)



#import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)




# write your own comment -what does the next line do? 
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
#streamlit.dataframe(fruityvice_normalized) 

#dont run anything past here while we troubleshoot


#import snowflake.connector

streamlit.header("View Our Fruit List - Add Your Favourites!")
#snoflake-related functions


def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

  

    
#add a button to load the fruit

if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)
  
#allow the en user to add a fruit to the list

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('"+new_fruit+"')")
    return "Thanks for adding " + new_fruit
    

                         
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  my_cnx.close()
  streamlit.text(back_from_function)
  
  
#    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#    back_from_function = insert_row_snowflake(add_my_fruit)
#   my_cnx.close()
# streamlit.text(back_from_function)
  
  

# streamlit.write('Thanks for adding', add_my_fruit)
# my_cur.execute("insert into fruit_load_list values ('from streamlit')")


# fruit_names = ["jackfruit", "papaya", "guava", "kiwi"]

# for fruit in fruit_names:
#     result = insert_row_snowflake(fruit)
#     print(result)
  
# streamlit.write('Thanks for adding', add_my_fruit)

# my_cur.execute("insert into fruit_load_list values ('from streamlit')")
