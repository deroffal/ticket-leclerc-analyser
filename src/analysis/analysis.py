import glob
import os

import pandas as pd

from definitions import PROCESSED_DIR

all_files = glob.glob(os.path.join(PROCESSED_DIR, "*.csv"))
df = pd.concat([pd.read_csv(f, sep=";") for f in all_files])

print(df.groupby("category").agg({'total_price': ['sum'], 'quantity': ['sum']}))
