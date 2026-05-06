# Tarea 1: Web Scraping de noticias de IA en Hacker News - Saúl García Medina

import requests
from bs4 import BeautifulSoup
import pandas as pd


def obtener_noticias_hackernews():
    url = "https://news.ycombinator.com/"

    respuesta = requests.get(url, timeout=10)
    respuesta.raise_for_status()

    soup = BeautifulSoup(respuesta.text, "html.parser")

    noticias = []

    filas_titulo = soup.select(".titleline")

    for item in filas_titulo:
        enlace = item.find("a")

        if enlace:
            titulo = enlace.text.strip()
            link = enlace.get("href")

            noticias.append({
                "titulo": titulo,
                "link": link
            })

    return noticias


def filtrar_noticias_ia(noticias):
    palabras_clave = [
        "AI", "Artificial Intelligence", "Machine Learning",
        "OpenAI", "LLM", "ChatGPT", "model", "neural"
    ]

    noticias_filtradas = []

    for noticia in noticias:
        titulo = noticia["titulo"]

        for palabra in palabras_clave:
            if palabra.lower() in titulo.lower():
                noticias_filtradas.append(noticia)
                break

    return noticias_filtradas


def guardar_resultados(noticias, nombre_archivo="tarea_1_webscrapping/resultados.csv"):
    df = pd.DataFrame(noticias)
    df.to_csv(nombre_archivo, index=False, encoding="utf-8-sig")
    return df


def main():
    print("Ejecutando webscraping...")

    noticias = obtener_noticias_hackernews()
    noticias_ia = filtrar_noticias_ia(noticias)

    if len(noticias_ia) == 0:
        print("No se encontraron noticias de IA. Se guardarán las primeras 10 noticias generales.")
        noticias_ia = noticias[:10]

    df = guardar_resultados(noticias_ia)

    print("\nResultados obtenidos:")
    print(df)

    print("\nArchivo resultados.csv generado correctamente.")


if __name__ == "__main__":
    main()