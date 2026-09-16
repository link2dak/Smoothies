# Import python packages
import streamlit as st
import os
from snowflake.snowpark.functions import col, when_matched


# Write directly to the app
st.title(f"Customize Your Smoothie!🥤\n")
st.write(
  """Choose the fruits you want in your custom smoothie
  """
)

session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED") == 0).collect()


if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    #submit button
    submitted = st.button('Submit')
    
    if submitted:    
        # orders dataset
        og_dataset = session.table("smoothies.public.orders")
        # new edited filled orders
        edited_dataset = session.create_dataframe(editable_df)
        try:
            og_dataset.merge(edited_dataset, (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID']),[when_matched().update({'ORDER_FILLED':          edited_dataset['ORDER_FILLED']})])

            st.success("Order(s) Updated!")

        except:
            st.write("something went wrong")
else:
    st.success("There are no pending orders right now")
