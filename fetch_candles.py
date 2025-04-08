from hyperliquid.info import Info
from hyperliquid.utils import constants
from datetime import datetime, timezone, timedelta
import json

# Initialize the Info class
info = Info(constants.MAINNET_API_URL, skip_ws=True)

# Define parameters
symbol = "ETH"
interval = "1m"

# Set the time range for the candlestick data
# For example, the last 24 hours
end_time = int(datetime.now(timezone.utc).timestamp() * 1000)  # Current time in milliseconds
start_time = end_time - (24 * 60 * 60 * 1000)  # 24 hours ago in milliseconds

# Fetch candlestick data
candles = info.candles_snapshot(name=symbol, interval=interval, startTime=start_time, endTime=end_time)

# Process the data as needed
print(json.dumps(candles, indent=2))
