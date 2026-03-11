import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# =========================
# Cargar datos
# =========================
# https://dash-test-jocu.onrender.com/

df = pd.read_csv("notas_estudiantes.csv")

# Calcular promedio por estudiante
df["Promedio"] = df.drop(columns=["Nombre"]).mean(axis=1)

# Promedio por evaluación
promedios_eval = df.drop(columns=["Nombre", "Promedio"]).mean().reset_index()
promedios_eval.columns = ["Evaluacion", "Promedio"]

# Ranking
ranking = df.sort_values("Promedio", ascending=False)

# =========================
# Crear gráficos
# =========================

fig_promedio_estudiante = px.bar(
    df,
    x="Nombre",
    y="Promedio",
    title="Promedio por Estudiante",
    color="Promedio",
    color_continuous_scale="Blues"
)

fig_distribucion = px.histogram(
    df,
    x="Promedio",
    nbins=10,
    title="Distribución de Promedios"
)

fig_promedio_eval = px.bar(
    promedios_eval,
    x="Evaluacion",
    y="Promedio",
    title="Promedio por Evaluación",
    color="Promedio",
    color_continuous_scale="Greens"
)

# =========================
# Crear aplicación Dash
# =========================

app = dash.Dash(__name__)
server = app.server

# =========================
# Layout
# =========================

app.layout = html.Div([

    html.H1(
        "Dashboard de Rendimiento Estudiantil",
        style={"textAlign": "center"}
    ),

    html.Div([
        dcc.Graph(figure=fig_promedio_estudiante)
    ]),

    html.Div([
        dcc.Graph(figure=fig_distribucion)
    ]),

    html.Div([
        dcc.Graph(figure=fig_promedio_eval)
    ]),

    html.H2("Ranking de Estudiantes", style={"textAlign": "center"}),

    html.Table(

        # Encabezado
        [html.Thead(
            html.Tr([html.Th(col) for col in ranking.columns])
        )] +

        # Filas
        [html.Tbody([
            html.Tr([
                html.Td(ranking.iloc[i][col]) for col in ranking.columns
            ]) for i in range(len(ranking))
        ])],

        style={
            "margin": "auto",
            "width": "70%",
            "border": "1px solid black",
            "textAlign": "center"
        }

    )

])

# =========================
# Ejecutar servidor
# =========================

if __name__ == "__main__":
    app.run(debug=True)
