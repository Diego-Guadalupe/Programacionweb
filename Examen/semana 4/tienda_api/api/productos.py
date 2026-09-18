import requests


# URL principal de la API
URL_API = "https://dummyjson.com/products"


def obtener_productos():

    try:

        respuesta = requests.get(
            URL_API,
            params={
                "limit": 0
            },
            timeout=10
        )

        respuesta.raise_for_status()

        datos = respuesta.json()

        return datos.get("products", [])

    except requests.exceptions.RequestException as error:

        print("Error al obtener productos:", error)

        return []


def buscar_productos(texto):

    try:

        respuesta = requests.get(
            f"{URL_API}/search",
            params={
                "q": texto
            },
            timeout=10
        )

        respuesta.raise_for_status()

        datos = respuesta.json()

        return datos.get("products", [])

    except requests.exceptions.RequestException as error:

        print("Error al buscar productos:", error)

        return []


def obtener_categorias():

    try:

        respuesta = requests.get(
            f"{URL_API}/category-list",
            timeout=10
        )

        respuesta.raise_for_status()

        return respuesta.json()

    except requests.exceptions.RequestException as error:

        print("Error al obtener categorías:", error)

        return []


def obtener_productos_categoria(categoria):

    try:

        respuesta = requests.get(
            f"{URL_API}/category/{categoria}",
            timeout=10
        )

        respuesta.raise_for_status()

        datos = respuesta.json()

        return datos.get("products", [])

    except requests.exceptions.RequestException as error:

        print("Error al obtener la categoría:", error)

        return []