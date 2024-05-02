import pandas as pd
import plotly.express as px
import streamlit as st
import statsmodels.api as sm

st.title('City-level Analysis')

tabs = st.tabs(['Specific Search','Data Overview'])

# 加载数据
data = pd.read_csv('WANG_QING_final_data.csv')

# 去除重复的活动，确保每个活动在其对应的城市和州只被计数一次
unique_events_per_city = data.drop_duplicates(subset=['Event Number', 'City', 'State']).groupby(['City', 'State']).size().reset_index(name='Number of Events')

# 对结果进行降序排序
unique_events_per_city_sorted = unique_events_per_city.sort_values(by='Number of Events', ascending=False)

# 创建一个新列用于图表的 Y 轴标签，包括城市和州名
unique_events_per_city_sorted['City_State'] = unique_events_per_city_sorted['City'] + ', ' + unique_events_per_city_sorted['State']

# 创建一个交互式的水平柱状图
fig = px.bar(unique_events_per_city_sorted, x='Number of Events', y='City_State', orientation='h',
             labels={'Number of Events': 'Number of Events', 'City_State': 'City, State'},
             title='Number of Music Events per City',
             color_discrete_sequence=['lightcoral'])

# 更新布局以改善视觉效果
fig.update_layout(
    xaxis_title='Number of Events',
    yaxis_title='City, State',
    height=1200,  # 可能需要根据城市数量增加图表的高度
    width=800,
    margin=dict(l=0, r=0, t=50, b=0),
    yaxis={'categoryorder': 'total ascending', 'tickangle': 0},
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)







# 去除重复的活动，确保每个活动在其对应的城市只被计数一次
unique_events_per_city = data.drop_duplicates(subset=['Event Number', 'City']).groupby('City').size().reset_index(name='Number of Events')
# 获取每个城市的人口数据（确保没有重复的城市数据）
city_population = data.drop_duplicates(subset='City')[['City', 'Population_city']]

# 合并活动数据和人口数据
merged_data = pd.merge(unique_events_per_city, city_population, on='City')

# 创建散点图和回归线
fig = px.scatter(merged_data, x='Population_city', y='Number of Events',
                 trendline="ols",
                 labels={"Population_city": "City Population", "Number of Events": "Number of Music Events"},
                 title="Relationship between City Population and Number of Music Events")

fig.update_traces(marker=dict(color='lightcoral'), selector=dict(mode='markers'))
fig.update_traces(line=dict(color='lightcoral'), selector=dict(type='scatter', mode='lines'))

# 显示图表
st.plotly_chart(fig, use_container_width=True)

# 使用statsmodels进行回归分析，获取详细的统计数据
X = sm.add_constant(merged_data['Population_city'])  # 添加常数项
model = sm.OLS(merged_data['Number of Events'], X)
results = model.fit()

# 提取关键统计数据
r_squared = results.rsquared
params = results.params
p_values = results.pvalues
slope = params['Population_city']
intercept = params['const']
p_value_slope = p_values['Population_city']

# 显示关键统计数据，避免使用科学计数法
st.write(f"R² value: {r_squared:.3f}")
st.write(f"Slope (coefficient for City Population): {slope:.3f}")
st.write(f"Intercept: {intercept:.3f}")
st.write(f"P-value for Slope: {p_value_slope:.10f}")








# 清洁数据：去除货币符号和逗号，并转换为数值型
data['Median Household Income_city'] = pd.to_numeric(data['Median Household Income_city'].replace('[\$,]', '', regex=True))

# 获取每个城市的中位家庭收入数据（确保没有重复的城市数据）
city_income = data.drop_duplicates(subset='City')[['City', 'Median Household Income_city']]

# 合并活动数据和收入数据
merged_data = pd.merge(unique_events_per_city, city_income, on='City')

# 创建散点图和回归线
fig = px.scatter(merged_data, x='Median Household Income_city', y='Number of Events',
                 trendline="ols",
                 labels={"Median Household Income_city": "Median Household Income", "Number of Events": "Number of Music Events"},
                 title="Relationship between City Median Household Income and Number of Music Events")

fig.update_traces(marker=dict(color='lightcoral'), selector=dict(mode='markers'))
fig.update_traces(line=dict(color='lightcoral'), selector=dict(type='scatter', mode='lines'))

# 显示图表
st.plotly_chart(fig, use_container_width=True)

# 使用statsmodels进行回归分析，获取详细的统计数据
X = sm.add_constant(merged_data['Median Household Income_city'])  # 添加常数项
model = sm.OLS(merged_data['Number of Events'], X)
results = model.fit()

# 提取关键统计数据
r_squared = results.rsquared
params = results.params
p_values = results.pvalues
slope = params['Median Household Income_city']
intercept = params['const']
p_value_slope = p_values['Median Household Income_city']

# 显示关键统计数据，避免使用科学计数法
st.write(f"R² value: {r_squared:.3f}")
st.write(f"Slope (coefficient for Median Household Income): {slope:.3f}")
st.write(f"Intercept: {intercept:.3f}")
st.write(f"P-value for Slope: {p_value_slope:.10f}")








# 去除重复的机场数据，确保每个机场只被计数一次
data_unique_airports = data.drop_duplicates(subset=['IATA', 'City'])

# 统计每个城市的机场数量
airports_per_city = data_unique_airports.groupby('City').size().reset_index(name='Number of Airports')

# 合并活动数据和机场数据
merged_data = pd.merge(unique_events_per_city, airports_per_city, on='City')

# 创建散点图和回归线
fig = px.scatter(merged_data, x='Number of Airports', y='Number of Events', 
                 trendline="ols", 
                 labels={"Number of Airports": "Number of Airports", "Number of Events": "Number of Music Events"},
                 title="Relationship between Number of Airports and Number of Music Events per City")

fig.update_traces(marker=dict(color='lightcoral'), selector=dict(mode='markers'))
fig.update_traces(line=dict(color='lightcoral'), selector=dict(type='scatter', mode='lines'))

# 显示图表
st.plotly_chart(fig, use_container_width=True)

# 使用statsmodels进行回归分析，获取详细的统计数据
X = sm.add_constant(merged_data['Number of Airports'])  # 添加常数项
model = sm.OLS(merged_data['Number of Events'], X)
results = model.fit()

# 显示回归分析结果的关键统计数据
r_squared = results.rsquared
params = results.params
p_values = results.pvalues
slope = params['Number of Airports']
intercept = params['const']
p_value_slope = p_values['Number of Airports']

# 显示关键统计数据
st.write(f"R² value: {r_squared:.3f}")
st.write(f"Slope (coefficient for Number of Airports): {slope:.3f}")
st.write(f"Intercept: {intercept:.3f}")
st.write(f"P-value for Slope: {p_value_slope:.10f}")  # 避免科学计数法