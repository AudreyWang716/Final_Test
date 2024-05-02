import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Datasets & Overview')

tabs = st.tabs(['Datasets Description','Data Overview'])

 
with tabs[0]:
    st.header('Datasets Description')
    st.write('Here you can put any content related to the first tab.')


with tabs[1]:
    st.header('Data Overview')

    # 加载数据
    data = pd.read_csv('WANG_QING_final_data.csv')

    # 计算独特的州和城市数量
    unique_states = data['State'].nunique()
    unique_cities = data.groupby('State')['City'].nunique().sum()

    # 显示总览信息
    st.write(f'''This project focuses on the United States only. 
             It has gathered data on music events held in the US, 
             as listed on Ticketmaster from the past 6 months to the upcoming year. 
             Then it has been integrated with population and median household incomes for each city 
             and state in the US, extracted from Census.gov, as well as information on US airports 
             from Wikipedia. Using Pandas for data modeling, the final dataset includes information 
             on music events across {unique_states} States and {unique_cities} Cities in the US, 
             which has been extensively collected and analyzed.''')
    

    
    # 计算每个州的独特活动数和机场数
    state_events = data.drop_duplicates(subset=['Event Number', 'State']).groupby('State').size()
    state_airports = data.drop_duplicates(subset=['IATA', 'State']).groupby('State').size()

    # 计算每个城市的独特活动数和机场数
    city_events = data.drop_duplicates(subset=['Event Number', 'City', 'State']).groupby(['City', 'State']).size()
    city_airports = data.drop_duplicates(subset=['IATA', 'City', 'State']).groupby(['City', 'State']).size()

    # 清理收入数据并转换为整数
    data['Median Household Income_city'] = data['Median Household Income_city'].replace('[\$,]', '', regex=True).astype(int)
    data['Median Household Income_state'] = data['Median Household Income_state'].replace('[\$,]', '', regex=True).astype(int)

    # 更新存储经济指标的DataFrame
    state_pop_income = data.drop_duplicates(subset='State').set_index('State')[['Population_state', 'Median Household Income_state']]
    city_pop_income = data.drop_duplicates(subset=['City', 'State']).set_index(['City', 'State'])[['Population_city', 'Median Household Income_city']]



    st.header('Specific Search')
    st.markdown('''
            <style>
            .small-font {
                font-size: 14px;
                font-style: italic;
                color: lightcoral
            }
            </style>
            <div class="small-font">
            Select the States or Cities level, then choose the ones you are interested in, you will get the detailed information about that State/City:
            </div>
            ''', unsafe_allow_html=True)
    # 用户选择级别：州或城市
    level = st.radio("Level:", ['State', 'City'])

    if level == 'State':
        state = st.selectbox('Select a State:', sorted(data['State'].unique()))
        events_count = state_events.get(state, 0)
        airports_count = state_airports.get(state, 0)
        population, median_income = state_pop_income.loc[state]

        # 创建一个DataFrame来存储数据
        df = pd.DataFrame({
            "Metric": ["Total Number of Events", "Population", "Median Household Income", "Number of Airports"],
            "Value": [events_count, population, median_income, airports_count]
        })
        # 显示表格但不显示列名
        st.table(df.set_index('Metric'))

    elif level == 'City':
        state = st.selectbox('Select a State for City:', sorted(data['State'].unique()))
        city = st.selectbox('Select a City:', sorted(data[data['State'] == state]['City'].unique()))
        events_count = city_events.get((city, state), 0)
        airports_count = city_airports.get((city, state), 0)
        population, median_income = city_pop_income.loc[(city, state)]

        # 创建一个DataFrame来存储数据
        df = pd.DataFrame({
            "Metric": ["Total Number of Events", "Population", "Median Household Income", "Number of Airports"],
            "Value": [events_count, population, median_income, airports_count]
        })
        # 显示表格但不显示列名
        st.table(df.set_index('Metric'))
