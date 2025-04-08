from hyperliquid.info import Info
from hyperliquid.utils import constants
from datetime import datetime, timezone, timedelta
import json

# Initialize the Info class
info = Info(constants.MAINNET_API_URL, skip_ws=True)

# Define parameters
symbols = {"ETH", "BTC"}
interval = "15m"

# Set the time range for the candlestick data
# For example, the last 24 hours
end_time = int(datetime.now(timezone.utc).timestamp() * 1000)  # Current time in milliseconds
candles = []
for symbol in symbols:
    start_time = end_time - (60 * 60 * 1000 * 1265)  # 24 hours ago in milliseconds

    # Fetch candlestick data
    candles = info.candles_snapshot(name=symbol, interval=interval, startTime=start_time, endTime=end_time)
    print(len(candles))
    # end_time = start_time

# Process the data as needed
print(len(candles))
# print(json.dumps(candles, indent=2))