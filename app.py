import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# cargar datos
df = pd.read_csv("notas_estudiantes.csv")

# calcular promedio por estudiante
df["Promedio"] = df.drop(columns=["Nombre"]).mean(axis=1)

# promedio por evaluación
promedios_eval = df.drop(columns=["Nombre","Promedio"]).mean()

# app
app = dash.Dash(__name__)
server = app.server

# gráficos
fig_promedio_estudiante = px.bar(
    df,
    x="Nombre",
    y="Promedio",
    title="Promedio por estudiante",
    color="Promedio",
    color_continuous_scale="Blues"
)

fig_distribucion = px.histogram(
    df,
    x="Promedio",
    nbins=10,
    title="Distribución de promedios"
)

fig_promedio_eval = px.bar(
    x=promedios_eval.index,
    y=promedios_eval.values,
    labels={"x": "Evaluación", "y": "Promedio"},
    title="Promedio por evaluación"
)

ranking = df.sort_values("Promedio", ascending=False)

# layout
app.layout = html.Div([
    
    html.H1("Dashboard de Rendimiento Estudiantil", 
            style={"textAlign":"center"}),

    html.Div([
        dcc.Graph(figure=fig_promedio_estudiante)
    ]),

    html.Div([
        dcc.Graph(figure=fig_distribucion)
    ]),

    html.Div([
        dcc.Graph(figure=fig_promedio_eval)
    ]),

    html.H2("Ranking de estudiantes"),

    html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in ranking.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(ranking.iloc[i][col]) for col in ranking.columns
            ]) for i in range(len(ranking))
        ])
    ], style={"margin":"auto", "width":"60%"})

])

if __name__ == "__main__":
    app.run(debug=True)
