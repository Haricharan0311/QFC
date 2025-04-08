from hyperliquid.info import Info
from hyperliquid.utils import constants
from datetime import datetime, timezone, timedelta
from load_candles import candles_to_df
import numpy as np


# Initialize the Info class
info = Info(constants.MAINNET_API_URL, skip_ws=True)

# Define parameters
# symbols = {"ETH", "BTC", "VINE"}
symbols = {"VINE"}
interval = "15m"
candles = {}

# Set the time range for the candlestick data
# For example, the last 24 hours
end_time = int(datetime.now(timezone.utc).timestamp() * 1000)  # Current time in milliseconds
for symbol in symbols:
    start_time = end_time - (60 * 60 * 1000 * 1265)  # 24 hours ago in milliseconds

    # Fetch candlestick data
    candles[symbol] = info.candles_snapshot(name=symbol, interval=interval, startTime=start_time, endTime=end_time)


df = candles_to_df(candles["VINE"])
print(df.head())