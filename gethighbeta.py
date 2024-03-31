import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd

# 獲取台指加權指數成分股
def get_component_stocks():
    url = "https://www.taifex.com.tw/cht/9/futuresQADetail"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    stocks = []
    for tr in soup.find_all("tr", bgcolor="#FFFFFF"):
        tds = tr.find_all("td", align="right")
        stock_id = tds[1].get_text().strip()
        stocks.append(stock_id)
    
    return stocks

# 獲取最近90個交易日的股票價格
def get_stock_prices(stock_id):
    stock = yf.Ticker(f"{stock_id}.TW")
    hist = stock.history(period="90d")
    return hist["Close"]

# 計算股票的BETA值
def calculate_beta(stock_returns, market_returns):
    cov = stock_returns.cov(market_returns)
    market_var = market_returns.var()
    beta = cov / market_var
    return beta

# 主函數
def main():
    component_stocks = get_component_stocks()
    market = yf.Ticker("^TWII")
    market_prices = market.history(period="90d")["Close"]

    betas = {}
    for stock_id in component_stocks:
        stock_prices = get_stock_prices(stock_id)
        stock_returns = stock_prices.pct_change().dropna()
        market_returns = market_prices.pct_change().dropna()

        beta = calculate_beta(stock_returns, market_returns)
        betas[stock_id] = beta

    # 找到前30高BETA值的股票
    top_30_betas = sorted(betas.items(), key=lambda x: x[1], reverse=True)[:30]

    print("Top 30 stocks with highest BETA values:")
    for stock_id, beta in top_30_betas:
        print(f"{stock_id}: {beta}")

if __name__ == "__main__":
    main()
