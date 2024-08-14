

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout = 'wide', page_title = 'Startup Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors = 'coerce')
df['year'] = df['date'].dt.year
df["month"] = df['date'].dt.month

def load_overall_analysis():
    st.title('Overall Analysis')
    #total invested amount
    total = round(df['amount'].sum())
    # maximum amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending = False).head(1).values[0]
    #avg ticket size
    avg_ticket_size = df.groupby('startup')['amount'].sum().mean()
    #total funded startups
    num_startups = df['startup'].nunique()
    
    col1, col2, col3, col4 =st.columns(4)
    
    with col1:
     st.metric('Total',str(total) + ' Cr')
    with col2:
     st.metric('Max',str(max_funding) + ' Cr')
    with col3:
     st.metric('Avg Ticket Size',str(round(avg_ticket_size)) + ' Cr')
    with col4:
     st.metric('Funded Startups', num_startups)

st.header('Month on Month graph')
selected_option = st.selectbox('Select Type', ['Total', "Count"])

if selected_option == "Total":
    temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
else:
    temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

# Create the x-axis as a combination of month and year
temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)        

# Plotting the graph
fig4, ax4 = plt.subplots()
ax4.plot(temp_df['x_axis'], temp_df["amount"])

st.pyplot(fig4)
def load_investors_details(investor):
# load the recent 5 investments of the investors
    st.title(investor)
    last5_df = df[df["investors"].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)
    
    col1, col2, col3, col4  = st.columns(4)
    with col1:
    #biggest investments
     big_series = df[df["investors"].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
     st.subheader('Biggest investments')
     fig, ax = plt.subplots()
     ax.bar(big_series.index,big_series.values)

     st.pyplot(fig)
     
     with col2:
         vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
         st.subheader('Sectors invested in')
         fig1, ax1 = plt.subplots()
         ax1.pie(vertical_series, labels = vertical_series.index, autopct="%0.01F%%")

         st.pyplot(fig1)
    with col3:
         round_series = df[df["investors"].str.contains(investor)].groupby('round')['amount'].sum()
         st.subheader('Stages invested in')
         fig2, ax2 = plt.subplots()
         ax2.pie(round_series, labels = round_series.index, autopct="%0.01F%%")     
         st.pyplot(fig2)
    
    with col4:
         city_series = df[df["investors"].str.contains(investor)].groupby('city')['amount'].sum()
         st.subheader('Cities invested in')
         fig3, ax3 = plt.subplots()
         ax3.pie(city_series, labels = city_series.index, autopct="%0.01F%%")     
         st.pyplot(fig3)
         
         
    df['year'] = df['date'].dt.year
    df["month"] = df['date'].dt.month
    year_series = df[df["investors"].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('YoY investment')
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index, year_series.values)      
    st.pyplot(fig4)
    

st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox('Select One', ["Overall Analysis", "Startup", "Investor"])

if option == 'Overall Analysis':
    btn0 = st.sidebar.button('Show Overall Analysis')
    if btn0:
        load_overall_analysis()
elif option == 'Startup': 
    st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Starup Details')
    st.title('Startup Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select Startup', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investors Details')
    if btn2:            
        load_investors_details(selected_investor)

