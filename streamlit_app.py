# Import python packages
import streamlit as st
import os
from snowflake.snowpark.functions import col
import requests  
import pandas

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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, width='stretch')
# st.stop()

# Convert snowpark dataframe to pandas dataframe so we can use the loc function
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:", my_dataframe,
    max_selections=5
)

if ingredients_list:
    
    ingredients_string = ''
    
    for i in ingredients_list:       
        ingredients_string+=i + ' '
      
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == i, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', i,' is ', search_on, '.')
      
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
