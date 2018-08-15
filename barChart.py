import numpy as np
import matplotlib.pyplot as plt

# Make a fake dataset:
height = [3, 5, 10, 30, 45]
bars = (50, 100, 150, 200, 250)
y_pos = np.arange(len(bars))

# Create bars
plt.bar(y_pos, height)

# Create names on the x-axis
#plt.xticks(y_pos, bars)

# Show graphic
plt.show()
