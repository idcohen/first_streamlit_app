import streamlit
import pandas
import snowflake.connector
# display api request response 
import requests
from urllib.error import URLError

streamlit.title("This is a test")
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑🍞 Hard-Boiled Free-Range Egg')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# fruit picker
fruits_selected = streamlit.multiselect("select a fruit",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display fruits
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice advice")

def get_fruityvice_data(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
try:
  #streamlit.text(fruityvice_response.json())
  fruit_choice = streamlit.text_input("select a fruit","kiwi")
  if not fruit_choice:
      streamlit.error("please select a fruit")
  else:
#    streamlit.write("user entered",fruit_choice)
    df = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(df)
except URLError as e:
  streamlit.error()

 
#streamlit.stop();
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains")
streamlit.dataframe(my_data_row)
#my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values('from streamlit')");

def insert_row_snfl(new_fruit):
  with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values('from streamlit')");
  return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input("select a fruit")
if streamlit.button("add a new fruit to the list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  rtn = insert_row_snfl(add_my_fruit)
  streamlit.text(rtn)

#streamlit.write("user entered",add_my_fruit)
