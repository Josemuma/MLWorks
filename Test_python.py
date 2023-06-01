import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from palmerpenguins import load_penguins

penguins = load_penguins()

penguins.head()
penguins.describe()

plot1 = sns.scatterplot(x = "flipper_length_mm", y = "body_mass_g",hue = "species",data = penguins,palette = ["#FF8C00","#159090","#A034F0"])

plot1.set_xlabel("Flipper Length (mm)")
plot1.set_ylabel("Body mass (g)")

plt.show(plot1)
plt.clf()
