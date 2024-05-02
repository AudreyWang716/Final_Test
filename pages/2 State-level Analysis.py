import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels.api as sm

st.title('State-level Analysis')

data = pd.read_csv('WANG_QING_final_data.csv')



# 去除重复的活动，确保每个活动只被计数一次
unique_events_per_state = data.drop_duplicates(subset=['Event Number', 'State']).groupby('State').size()

# 对结果进行降序排序
unique_events_per_state_sorted = unique_events_per_state.sort_values(ascending=False)

# 创建一个交互式的水平柱状图
fig = px.bar(unique_events_per_state_sorted, orientation='h',
        labels={'value': 'Number of Events', 'index': 'State'},
        title='Number of Music Events per State',
        color_discrete_sequence=['lightcoral'])

# 更新布局以改善视觉效果
fig.update_layout(
    xaxis_title='Number of Events',
    yaxis_title='State',
    height=800,  # 可以根据需要增加高度
    width=800,   # 可以根据需要调整宽度
    margin=dict(l=0, r=0, t=50, b=0),  # 调整图表的边距
    yaxis={'categoryorder': 'total ascending', 'tickangle': 0},
    showlegend = False
)

st.plotly_chart(fig, use_container_width=True)







# 去除重复的活动，确保每个活动只被计数一次
data_unique_events = data.drop_duplicates(subset=['Event Number', 'State'])

# 统计每个州的活动数量
events_per_state = data_unique_events.groupby('State').size().reset_index(name='Number of Events')

# 确保人口数据是整数形式
if data['Population_state'].dtype == 'O':  # Object type, typically used for strings
    data['Population_state'] = data['Population_state'].str.replace(',', '').astype(int)
elif data['Population_state'].dtype != 'int':
    data['Population_state'] = data['Population_state'].astype(int)

# 获取每个州的人口数据（确保没有重复的州数据）
state_population = data.drop_duplicates(subset='State')[['State', 'Population_state']]

# 合并活动数据和人口数据
merged_data = pd.merge(events_per_state, state_population, on='State')

# 创建散点图和回归线
fig = px.scatter(merged_data, x='Population_state', y='Number of Events', 
                 trendline="ols", 
                 labels={"Population_state": "State Population", "Number of Events": "Number of Events"},
                 title="Relationship between State Population and Number of Events")

fig.update_traces(marker=dict(color='lightcoral'), selector=dict(mode='markers'))
fig.update_traces(line=dict(color='lightcoral'), selector=dict(type='scatter', mode='lines'))

# 显示图表
st.plotly_chart(fig, use_container_width=True)

# 使用statsmodels进行回归分析，获取详细的统计数据
X = sm.add_constant(merged_data['Population_state'])  # 添加常数项
model = sm.OLS(merged_data['Number of Events'], X)
results = model.fit()

# 提取关键统计数据
r_squared = results.rsquared
params = results.params
p_values = results.pvalues
slope = params['Population_state']
intercept = params['const']
p_value_slope = p_values['Population_state']

# 显示关键统计数据
st.write(f"R² value: {r_squared:.3f}")
st.write(f"Slope (coefficient for State Population): {slope:.10f}")
st.write(f"Intercept: {intercept:.3f}")
st.write(f"P-value for Slope: {p_value_slope:.10f}")









# 确保中位家庭收入是整数形式，并处理可能的数据格式问题
if data['Median Household Income_state'].dtype == 'O':  # Object type, typically used for strings
    data['Median Household Income_state'] = data['Median Household Income_state'].str.replace(',', '').str.replace('$', '').astype(int)
elif data['Median Household Income_state'].dtype != 'int':
    data['Median Household Income_state'] = data['Median Household Income_state'].astype(int)

# 获取每个州的中位家庭收入数据（确保没有重复的州数据）
state_income = data.drop_duplicates(subset='State')[['State', 'Median Household Income_state']]

# 合并活动数据和收入数据
merged_data = pd.merge(events_per_state, state_income, on='State')

# 创建散点图和回归线
fig = px.scatter(merged_data, x='Median Household Income_state', y='Number of Events', 
                 trendline="ols", 
                 labels={"Median Household Income_state": "Median Household Income", "Number of Events": "Number of Music Events"},
                 title="Relationship between Median Household Income and Number of Music Events per State")

fig.update_traces(marker=dict(color='lightcoral'), selector=dict(mode='markers'))
fig.update_traces(line=dict(color='lightcoral'), selector=dict(type='scatter', mode='lines'))

# 显示图表
st.plotly_chart(fig, use_container_width=True)

# 使用statsmodels进行回归分析，获取详细的统计数据
X = sm.add_constant(merged_data['Median Household Income_state'])  # 添加常数项
model = sm.OLS(merged_data['Number of Events'], X)
results = model.fit()

# 显示回归分析结果的关键统计数据
r_squared = results.rsquared
params = results.params
p_values = results.pvalues
slope = params['Median Household Income_state']
intercept = params['const']
p_value_slope = p_values['Median Household Income_state']

# 显示关键统计数据
st.write(f"R² value: {r_squared:.3f}")
st.write(f"Slope (coefficient for Median Household Income): {slope:.3f}")
st.write(f"Intercept: {intercept:.3f}")
st.write(f"P-value for Slope: {p_value_slope:.10f}")  # 避免科学计数法







# 去除重复的机场数据，确保每个机场只被计数一次
data_unique_airports = data.drop_duplicates(subset=['IATA', 'State'])

# 统计每个州的机场数量
airports_per_state = data_unique_airports.groupby('State').size().reset_index(name='Number of Airports')

# 合并活动数据和机场数据
merged_data = pd.merge(events_per_state, airports_per_state, on='State')

# 创建散点图和回归线
fig = px.scatter(merged_data, x='Number of Airports', y='Number of Events', 
                 trendline="ols", 
                 labels={"Number of Airports": "Number of Airports", "Number of Events": "Number of Music Events"},
                 title="Relationship between Number of Airports and Number of Music Events per State")

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
