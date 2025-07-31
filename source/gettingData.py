import yfinance as yf

def getData( symbol : str ) : 

    try:
        symbolInfo = yf.Ticker(symbol)

        current_price = symbolInfo.info.get("regularMarketPrice", "No data")
        currency = symbolInfo.info.get("currency")
        lastClose = symbolInfo.info.get("previousClose")

        return {
            'currentPrice': current_price,
            'currency' : currency,
            'lastClose' : lastClose
        }
    
    except Exception as e:
        print(f"Error during getting data '{symbol}': {e}")
        return None