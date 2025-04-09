import itertools
import time
import numpy as np
from trade_data import TradeEngine
from load_candles import candles_to_df
from hyperliquid.info import Info
from hyperliquid.utils import constants
from datetime import datetime, timezone
import pandas as pd

# === 1. Load Candles ===
info = Info(constants.MAINNET_API_URL, skip_ws=True)
end_time = int(datetime.now(timezone.utc).timestamp() * 1000)
start_time = end_time - (60 * 60 * 1000 * 1265)

candles = info.candles_snapshot(name="VINE", interval="15m", startTime=start_time, endTime=end_time)
df = candles_to_df(candles)

# === 2. Define Full Parameter Grid ===
short_sizes = list(range(3, 26, 2))
long_sizes = list(range(20, 101, 5))
volume_enter_scalers = [round(x, 2) for x in np.arange(0.5, 1.01, 0.1)]
volume_exit_scalers = [round(x, 2) for x in np.arange(1.0, 3.01, 0.1)]
trailing_stop_losses = [round(x, 2) for x in np.arange(1.0, 1.26, 0.02)]
sma_candles = list(range(3, 11))

param_space = list(itertools.product(
    short_sizes,
    long_sizes,
    volume_enter_scalers,
    volume_exit_scalers,
    trailing_stop_losses,
    sma_candles
))

# === 3. Simulation Loop ===
results = []
start_time = time.time()

print(f"Total configs: {len(param_space)}")
for i, (short_size, long_size, v_enter, v_exit, trailing_sl, sma) in enumerate(param_space):
    hp = {
        "short_size": short_size,
        "long_size": long_size,
        "volume_enter_scaler": v_enter,
        "volume_exit_scaler": v_exit,
        "trailing_stop_loss": trailing_sl,
        "sma_candles": sma,
        "buy_amount": 1000
    }

    engine = TradeEngine(df.copy(), hp)
    engine.simulate()

    results.append({
        "short_size": short_size,
        "long_size": long_size,
        "v_enter": v_enter,
        "v_exit": v_exit,
        "trailing_sl": trailing_sl,
        "sma": sma,
        "PV": engine.PV,
        "trades": len(engine.trades)
    })

    if i % 100 == 0:
        elapsed = time.time() - start_time
        print(f"{i}/{len(param_space)} configs done | Elapsed: {elapsed:.2f}s")

# === 4. Save Results ===
df_results = pd.DataFrame(results)
df_results.to_csv("monte_carlo_results.csv", index=False)

elapsed = time.time() - start_time
print(f"\n✅ Completed {len(param_space)} simulations in {elapsed:.2f} seconds")
