# Tarea 2: Análisis de datos del Titanic con Gradio - Saúl García Medina

import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt


def cargar_datos():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    return df


def grafica_supervivencia_por_sexo():
    df = cargar_datos()

    resumen = df.groupby("Sex")["Survived"].mean() * 100

    fig, ax = plt.subplots()
    resumen.plot(kind="bar", ax=ax)

    ax.set_title("Porcentaje de supervivencia por sexo")
    ax.set_xlabel("Sexo")
    ax.set_ylabel("Porcentaje de supervivencia")
    ax.set_ylim(0, 100)

    for i, valor in enumerate(resumen):
        ax.text(i, valor + 2, f"{valor:.1f}%", ha="center")

    plt.tight_layout()
    return fig


def grafica_supervivencia_por_clase():
    df = cargar_datos()

    resumen = df.groupby("Pclass")["Survived"].mean() * 100
    resumen.index = ["Alta", "Media", "Baja"]

    fig, ax = plt.subplots()
    resumen.plot(kind="bar", ax=ax)

    ax.set_title("Porcentaje de supervivencia por clase")
    ax.set_xlabel("Clase del pasajero")
    ax.set_ylabel("Porcentaje de supervivencia")
    ax.set_ylim(0, 100)

    for i, valor in enumerate(resumen):
        ax.text(i, valor + 2, f"{valor:.1f}%", ha="center")

    plt.tight_layout()
    return fig


def mostrar_primeros_registros():
    df = cargar_datos()
    return df.head(10)


with gr.Blocks(title="Análisis Titanic con Gradio") as app:
    gr.Markdown("# Análisis del Titanic con Gradio")
    gr.Markdown(
        "Esta aplicación muestra estadísticas descriptivas del dataset Titanic "
        "utilizando Python, Pandas, Matplotlib y Gradio."
    )

    with gr.Tab("Datos"):
        gr.Markdown("## Primeros registros del dataset")
        boton_datos = gr.Button("Mostrar datos")
        tabla = gr.Dataframe()

        boton_datos.click(
            fn=mostrar_primeros_registros,
            outputs=tabla
        )

    with gr.Tab("Supervivencia por sexo"):
        gr.Markdown("## Porcentaje de supervivencia por sexo")
        boton_sexo = gr.Button("Generar gráfica")
        grafica_sexo = gr.Plot()

        boton_sexo.click(
            fn=grafica_supervivencia_por_sexo,
            outputs=grafica_sexo
        )

    with gr.Tab("Supervivencia por clase"):
        gr.Markdown("## Porcentaje de supervivencia por clase")
        boton_clase = gr.Button("Generar gráfica")
        grafica_clase = gr.Plot()

        boton_clase.click(
            fn=grafica_supervivencia_por_clase,
            outputs=grafica_clase
        )


if __name__ == "__main__":
    app.launch()