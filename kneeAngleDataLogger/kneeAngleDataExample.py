import numpy as np
import plotly.graph_objects as go
x = np.linspace(0, 2 * np.pi, 49)
y = np.sin(x)
data = go.Scatter(x = x, y = y)
fig = go.Figure(data)
fig.update_layout(xaxis_title = 'Time in Seconds', yaxis_title = 'Knee Angle in Degrees')
fig.update_layout(title = 'Knee Angle Data Example')
fig.show()
