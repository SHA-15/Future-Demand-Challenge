# importing pandas as pd
import pandas as pd

# Creating the DataFrame
df = pd.DataFrame({"A": [12, 4, 5, None, 1],
                   "B": [7, 2, 54, 3, None],
                   "C": [20, 16, 11, 3, 8],
                   "D": [14, 3, None, 2, 6]})

# Create the index
index_ = ['Row_1', 'Row_2', 'Row_3', 'Row_4', 'Row_5']

# Set the index
df.index = index_

# Print the DataFrame
print(df)

# return the column labels
result = df.columns

# Print the result
print(list(result))