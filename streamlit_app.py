import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import datetime

# 爬取数据
def fetch_data():
    url = "https://tw.tradingview.com/markets/world-stocks/worlds-largest-companies/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    companies = []
    table = soup.find('table')
    rows = table.find_all('tr')[1:]  # 跳过表头行

    for row in rows:
        cols = row.find_all('td')


        if len(cols) >= 3:
            rank = cols[0].text.strip()
            name = cols[1].text.strip()
            market_cap = cols[3].text.strip()
            price = cols[4].text.strip()
            companies.append({ 'Name': rank, 'Market Cap': market_cap, 'Price': price})
    
    return pd.DataFrame(companies)

# 加载数据
data = fetch_data()

# Streamlit 页面设置
st.markdown("<h1 style='text-align: center;'>全球市值最大公司排名</h1>", unsafe_allow_html=True)

st.write("")

# 调整索引从1开始并只显示前100家公司
data.reset_index(drop=True, inplace=True)
data = data.head(100)
data.index = data.index + 1

# 选择需要显示的列
data = data[[ 'Name', 'Market Cap', 'Price']]

# 显示数据表格
st.table(data)

# 获取当前日期
current_date = datetime.date.today().strftime("%Y-%m-%d")

st.markdown(f'<span style="font-size: 14px">**来源:** TradingView | **数据日期:** {current_date}</span>', unsafe_allow_html=True)
