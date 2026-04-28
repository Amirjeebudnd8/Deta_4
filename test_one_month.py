import requests
import zipfile
import io
import pandas as pd

SYMBOL = "BTCUSDT"
INTERVAL = "5m"
YEAR = 2024
MONTH = 1  # ژانویه

url = f"https://data.binance.vision/data/spot/monthly/klines/{SYMBOL}/{INTERVAL}/{SYMBOL}-{INTERVAL}-{YEAR}-{MONTH:02d}.zip"
print(f"در حال دانلود {url}")

try:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f, header=None)
    df.columns = ['open_time','open','high','low','close','volume',
                  'close_time','quote_volume','trades','taker_buy_base',
                  'taker_buy_quote','ignore']
    df['timestamp'] = pd.to_datetime(df['open_time'], unit='ms')
    df = df[['timestamp','open','high','low','close','volume']]
    df.to_csv("BTCUSDT_5m_test.csv", index=False)
    print(f"✅ موفق شد. تعداد رکوردها: {len(df)}")
except Exception as e:
    print(f"❌ خطا: {e}")
    exit(1)
