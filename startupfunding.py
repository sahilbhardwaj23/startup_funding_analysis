import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#set page width and title
st.set_page_config(layout="wide",page_title='Startup Aanlysis')
#first we upload the original file and if possible do data cleaning here or upload the cleaned csv file
df=pd.read_csv('startup_cleaned.csv')

df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
def load_overall_analysis():
    st.title('Overall Analysis')
    #total invested amount
    total=round(df['amount'].sum())
    #max amount infused in a startup
    max_funding=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    #average funding
    average_funding=df.groupby('startup')['amount'].sum().mean()
    #total funded startups
    num_startups=df['startup'].nunique()
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric('Total',str(total)+'cr')
    with col2:
        st.metric('Max',str(max_funding)+'cr')
    with col3:
        st.metric('Average',str(average_funding)+'cr')
    with col4:
        st.metric('Funded startup number',str(num_startups))
    st.header("MoM on graph")
    selected_option=st.selectbox('Select Type',['Total','Count'])
    if selected_option=='Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig5,ax5 = plt.subplots()
    ax5.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig5)
def load_investor_details(investor):
    st.title(investor)
    #load the recent 5 investment of the investor
    last5_df=df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1,col2=st.columns(2)
    #biggest investment
    with col1:
        big_series=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False)
        st.subheader('Biggest Investments')
        fig,ax=plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)
    with col2:
        vertical_series=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sector invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct='%0.01f')
        st.pyplot(fig1)
    col3,col4=st.columns(2)
    with col3:
        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Sector invested in round')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct='%0.01f')
        st.pyplot(fig2)
    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('Sector invested in city')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct='%0.01f')
        st.pyplot(fig3)
    df['year']=df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('YoY Investment')
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index,year_series.values)
    st.pyplot(fig4)


    #find similar investors
#data cleaning
# df['Investors Name']=df['Investors Name'].fillna('Undisclosed')

st.sidebar.title('Startup Funding Analysis')

option=st.sidebar.selectbox('Select one',['Overall Analysis','Startup','Investor'])

if option=='Overall Analysis':
    st.sidebar.button('Show Overall Analysis')
    load_overall_analysis()
elif option=='Startup':
    st.title('Startup Analysis')
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Startup Details')
else:
    st.title('Investor Analysis')
    selected_investor=st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investors Details')
    if btn2:
        load_investor_details(selected_investor)
