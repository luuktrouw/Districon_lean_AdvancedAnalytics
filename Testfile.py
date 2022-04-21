import plotly.graph_objects as go
import plotly.io as pio
from PIL import Image

# to render in jupyterlab
#pio.renderers.default = "plotly_mimetype"

# Create figure
fig = go.Figure()

pyLogo = Image.open(r'C:\Users\l.trouw\Documents\Pycharm\Lean_simulation\VSMvisualizationMatrasses.png')

# Add trace
fig.add_trace(
    go.Scatter(x=[0, 0.5, 1, 2, 2.2], y=[1.23, 2.5, 0.42, 3, 1])
)

fig.add_layout_image(
        dict(
            source=pyLogo,
            xref="x",
            yref="y",
            x=0,
            y=3,
            sizex=2,
            sizey=2,
            sizing="stretch",
            opacity=0.5,
            layer="above")
)

fig.show()