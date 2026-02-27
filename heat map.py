import pandas as pd
from sqlalchemy import create_engine

import matplotlib.pyplot as plt
import seaborn as sns

# Create connection
engine = create_engine(f"postgresql+psycopg2://postgres:Poojitha%40123@localhost:5432/Video_Games_project")

# Load table or view
query = "SELECT * FROM Combine_dataSG"
df = pd.read_sql(query, engine)

print(df.head())

heatmap_data = df.groupby("genre")[[
    "na_sales",
    "eu_sales",
    "jp_sales",
    "other_sales"
]].mean()

# Create heatmap
plt.figure()
sns.heatmap(heatmap_data, annot=True)

plt.title("Average Regional Sales by Genre")
plt.show()