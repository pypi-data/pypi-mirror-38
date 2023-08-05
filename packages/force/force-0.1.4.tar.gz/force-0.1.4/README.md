# Force: A package to visualize the receptive fields
Force is a Python package that allows you to visualize the receptive fields of a neural network.

## 1. How to Run

To run this algorithm in Python:
```
from force.receptive_field import visualize_neuron
from gdbn.dbn import buildDBN
import matplotlib.pyplot as plt

# Make a deep belief network
dbn = buildDBN([1, 100, 1])

# Get the 3rd neuron on the 1st layer. (With Linear averaging)
neuron = visualize_neuron(dbn, 0, 2)

# Plot!
plt.imshow(neuron)
plt.show()

```

All configurable options are in the SBB/config.py file, in the variable CONFIG.
