# Import python packages
import streamlit as st
import os
from snowflake.snowpark.functions import col
import requests  


# Write directly to the app
st.title(f"Customize Your Smoothie!🥤\n")
st.write(
  """Choose the fruits you want in your custom smoothie
  """
)

#name box for customer
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on you smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, width='stretch')


ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:", my_dataframe,
    max_selections=5
)

if ingredients_list:
    
    ingredients_string = ''
    
    for i in ingredients_list:       
        ingredients_string+=i + ' '
        # API for smoothiefroot for chosen fruit
        st.subheader(i+'Nutrition Information')
        smoothiefroot_response = requests.get(
        f"https://my.smoothiefroot.com/api/fruit/{i}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


    my_insert_smt = """ insert into smoothies.public.orders(ingredients, name_on_order) 
    values ('""" + ingredients_string + """', '"""+name_on_order+"""')"""

    # st.write(my_insert_smt)
    # st.stop()

    #insert button
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_smt).collect()

        st.success(f"Your Smoothie is ordered, {name_on_order}", icon="✅")


# API for smoothiefroot
smoothiefroot_response = requests.get(
"https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
