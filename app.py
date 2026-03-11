import dash
from dash import html

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Mi primera app Dash en Render 🚀"),
    html.P("Si ves esto, el deploy funcionó")
])

if __name__ == "__main__":
    app.run(debug=True)
