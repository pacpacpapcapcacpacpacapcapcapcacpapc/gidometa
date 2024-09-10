import streamlit as st
import yfinance as yf
from yahoo_fin import stock_info as si
import requests
import pandas as pd

st.title("커뮤니티 인기 종목과 트렌드 주식 급등주 분석")

# 야후 파이낸스 트렌드 주식
trending_stocks = si.get_day_most_active()
trending_symbols = trending_stocks['Symbol'].head(5).tolist()
st.subheader("야후 파이낸스 트렌드 주식 상위 5개")
st.dataframe(trending_stocks[['Symbol', 'Name', 'Price (Intraday)', 'Volume']].head(5))

# StockTwits 인기 종목
url = "https://api.stocktwits.com/api/2/trending/symbols.json"
response = requests.get(url)
data = response.json()
stocktwits_symbols = [symbol['symbol'] for symbol in data['symbols'][:5]]
st.subheader("StockTwits에서 인기 있는 종목 상위 5개")
for symbol in stocktwits_symbols:
    st.write(symbol)

# Reddit 인기 종목 (수동으로 입력, API 사용하지 않음)
reddit_symbols = ['GME', 'AMC', 'TSLA', 'AAPL', 'MSFT']  # 예시로 수동 입력한 인기 종목
st.subheader("Reddit에서 인기 있는 종목 (수동)")
for symbol in reddit_symbols:
    st.write(symbol)

# 종목 합치기
all_symbols = list(set(trending_symbols + stocktwits_symbols + reddit_symbols))

# 급등주 분석 함수
def analyze_stocks(symbols):
    hot_stocks = []
    for symbol in symbols:
        stock_data = yf.download(symbol, period="1y")
        if not stock_data.empty:
            # 급등 조건 분석 로직 추가 (52주 신고가, 볼린저 밴드, 거래량 등)
            hot_stocks.append(symbol)
    return hot_stocks

# 급등주 분석 결과
st.subheader("커뮤니티 인기 종목 중 급등주 추천")
hot_stocks = analyze_stocks(all_symbols)

if hot_stocks:
    st.write("급등주 추천 목록:")
    for stock in hot_stocks:
        st.write(stock)
else:
    st.write("급등주가 없습니다.")
