import numpy as np
import pandas as pd
from datetime import datetime

names_and_works = []

name_and_works_df = pd.DataFrame(names_and_works, columns=["name", "works"])
print(name_and_works_df)