import streamlit as st
from yahooquery import Screener
import yfinance as yf

# Streamlit 앱 제목
st.title("커뮤니티 인기 종목과 트렌드 주식 급등주 분석")

# 야후 파이낸스 트렌드 주식
st.subheader("야후 파이낸스 트렌드 주식 상위 5개")

# Yahoo Finance 스크리너를 통해 트렌드 주식 가져오기
screener = Screener()
data = screener.get_screeners('day_gainers', count=5)

# 트렌드 종목 추출
if 'day_gainers' in data and 'quotes' in data['day_gainers']:
    trending_stocks = data['day_gainers']['quotes']
    trending_symbols = [stock['symbol'] for stock in trending_stocks]

    # 종목 리스트 출력
    for symbol in trending_symbols:
        st.write(symbol)

    # 급등주 분석 함수
    def analyze_stocks(symbols):
        hot_stocks = []
        for symbol in symbols:
            stock_data = yf.download(symbol, period="1y")
            if not stock_data.empty:
                # 52주 신고가, 거래량 급등 분석 로직을 여기에 추가
                hot_stocks.append(symbol)
        return hot_stocks

    # 급등주 분석 결과
    st.subheader("커뮤니티 인기 종목 중 급등주 추천")
    hot_stocks = analyze_stocks(trending_symbols)

    if hot_stocks:
        st.write("급등주 추천 목록:")
        for stock in hot_stocks:
            st.write(stock)
    else:
        st.write("급등주가 없습니다.")
else:
    st.write("데이터를 가져오지 못했습니다. 나중에 다시 시도하세요.")
