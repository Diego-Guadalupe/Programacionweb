import streamlit as st

from api.productos import (
    obtener_productos,
    buscar_productos,
    obtener_categorias,
    obtener_productos_categoria
)


st.set_page_config(
    page_title="SPORT SHOP",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown(
    """
    <style>


    .stApp {
        background-color: #ffffff;
    }

    .block-container {
        padding-top: 0rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1500px;
    }


    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }


    .top-bar {
        background-color: #000000;
        color: white;
        text-align: center;
        padding: 9px;
        font-size: 13px;
        letter-spacing: 0.5px;
        margin-left: -3rem;
        margin-right: -3rem;
    }


    .brand {
        font-size: 32px;
        font-weight: 900;
        letter-spacing: -2px;
        color: #000000;
        margin-top: 18px;
    }


    .menu {
        text-align: center;
        padding-top: 20px;
    }

    .menu span {
        margin: 0 18px;
        font-size: 15px;
        font-weight: 600;
    }


    .icons {
        text-align: right;
        padding-top: 15px;
        font-size: 22px;
    }


    .hero {
        background-color: #eeeeee;
        padding: 55px 30px;
        margin-top: 25px;
        margin-bottom: 40px;
        text-align: center;
    }

    .hero h1 {
        font-size: 48px;
        font-weight: 900;
        margin-bottom: 10px;
        color: #000000;
    }

    .hero p {
        font-size: 18px;
        color: #333333;
        margin-bottom: 25px;
    }

    .hero-button {
        display: inline-block;
        background-color: #000000;
        color: white;
        padding: 14px 30px;
        font-weight: bold;
        text-decoration: none;
    }


    .section-title {
        font-size: 28px;
        font-weight: 800;
        margin-top: 35px;
        margin-bottom: 20px;
        color: #000000;
    }


    .product-card {
        background-color: #f5f5f5;
        padding: 15px;
        margin-bottom: 15px;
        min-height: 440px;
    }

    .product-title {
        font-size: 17px;
        font-weight: 700;
        color: #111111;
        margin-top: 8px;
        min-height: 45px;
    }

    .product-category {
        font-size: 12px;
        color: #777777;
        text-transform: uppercase;
        margin-top: 5px;
    }

    .product-price {
        font-size: 18px;
        font-weight: bold;
        color: #000000;
        margin-top: 8px;
    }

    .product-rating {
        font-size: 13px;
        color: #444444;
    }


    .discount {
        display: inline-block;
        background-color: #ffffff;
        color: #d00000;
        padding: 4px 8px;
        font-size: 11px;
        font-weight: bold;
        margin-bottom: 5px;
    }


    .search-title {
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 10px;
    }


    .category-box {
        background-color: #eeeeee;
        text-align: center;
        padding: 30px 10px;
        font-weight: bold;
        margin-bottom: 15px;
        text-transform: uppercase;
    }


    .cart-box {
        border: 1px solid #dddddd;
        padding: 20px;
        margin-top: 20px;
    }


    .footer {
        background-color: #000000;
        color: white;
        padding: 45px;
        margin-top: 70px;
        margin-left: -3rem;
        margin-right: -3rem;
        text-align: center;
    }

    .footer h3 {
        font-size: 25px;
    }

    .footer p {
        color: #cccccc;
    }

    </style>
    """,
    unsafe_allow_html=True
)


if "carrito" not in st.session_state:

    st.session_state.carrito = []

if "vista" not in st.session_state:

    st.session_state.vista = "Inicio"


@st.cache_data(ttl=300)
def cargar_productos():

    return obtener_productos()


@st.cache_data(ttl=300)
def cargar_categorias():

    return obtener_categorias()


def agregar_carrito(producto):

    for item in st.session_state.carrito:

        if item["id"] == producto["id"]:

            item["cantidad"] += 1

            return

    st.session_state.carrito.append(
        {
            "id": producto["id"],
            "title": producto["title"],
            "price": producto["price"],
            "thumbnail": producto["thumbnail"],
            "cantidad": 1
        }
    )


def quitar_carrito(producto_id):

    st.session_state.carrito = [
        producto
        for producto in st.session_state.carrito
        if producto["id"] != producto_id
    ]


def calcular_total():

    total = 0

    for producto in st.session_state.carrito:

        total += (
            producto["price"] *
            producto["cantidad"]
        )

    return total


def mostrar_producto(producto):

    st.markdown(
        '<div class="product-card">',
        unsafe_allow_html=True
    )

    if producto.get("discountPercentage", 0) > 0:

        st.markdown(
            f"""
            <span class="discount">
                -{producto["discountPercentage"]:.0f}%
            </span>
            """,
            unsafe_allow_html=True
        )

    st.image(
        producto["thumbnail"],
        use_container_width=True
    )

    st.markdown(
        f"""
        <div class="product-title">
            {producto["title"]}
        </div>

        <div class="product-category">
            {producto["category"]}
        </div>

        <div class="product-rating">
            ⭐ {producto["rating"]}
        </div>

        <div class="product-price">
            ${producto["price"]:.2f} USD
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    if st.button(
        "AGREGAR AL CARRITO",
        key=f"producto_{producto['id']}",
        use_container_width=True
    ):

        agregar_carrito(producto)

        st.success(
            "Producto agregado al carrito"
        )


st.markdown(
    """
    <div class="top-bar">
        ENVÍO GRATIS EN PRODUCTOS SELECCIONADOS
        &nbsp;&nbsp; | &nbsp;&nbsp;
        DESCUBRE NUEVAS COLECCIONES
    </div>
    """,
    unsafe_allow_html=True
)


col_logo, col_menu, col_icons = st.columns(
    [2, 7, 2]
)


with col_logo:

    st.markdown(
        """
        <div class="brand">
            SPORT
        </div>
        """,
        unsafe_allow_html=True
    )


with col_menu:

    menu_col1, menu_col2, menu_col3, menu_col4 = st.columns(4)

    with menu_col1:

        if st.button(
            "MUJER",
            use_container_width=True
        ):

            st.session_state.vista = "Productos"

    with menu_col2:

        if st.button(
            "HOMBRE",
            use_container_width=True
        ):

            st.session_state.vista = "Productos"

    with menu_col3:

        if st.button(
            "NIÑOS",
            use_container_width=True
        ):

            st.session_state.vista = "Categorías"

    with menu_col4:

        if st.button(
            "OFERTAS",
            use_container_width=True
        ):

            st.session_state.vista = "Ofertas"


with col_icons:

    st.markdown(
        """
        <div class="icons">
            ♡ &nbsp;&nbsp; 🛍️
        </div>
        """,
        unsafe_allow_html=True
    )


col_buscar, col_carrito = st.columns(
    [8, 2]
)


with col_buscar:

    busqueda = st.text_input(
        "",
        placeholder="Buscar productos...",
        label_visibility="collapsed"
    )


with col_carrito:

    cantidad_carrito = sum(
        item["cantidad"]
        for item in st.session_state.carrito
    )

    if st.button(
        f"🛍️ CARRITO ({cantidad_carrito})",
        use_container_width=True
    ):

        st.session_state.vista = "Carrito"


if busqueda:

    st.markdown(
        '<div class="section-title">RESULTADOS DE BÚSQUEDA</div>',
        unsafe_allow_html=True
    )

    resultados = buscar_productos(busqueda)

    if not resultados:

        st.warning(
            "No encontramos productos."
        )

    else:

        columnas = st.columns(4)

        for indice, producto in enumerate(resultados):

            with columnas[indice % 4]:

                mostrar_producto(producto)


elif st.session_state.vista == "Inicio":


    st.markdown(
        '<div class="section-title">COMPRA POR CATEGORÍA</div>',
        unsafe_allow_html=True
    )

    categorias = cargar_categorias()

    categorias_mostrar = categorias[:6]

    columnas = st.columns(3)

    for indice, categoria in enumerate(
        categorias_mostrar
    ):

        with columnas[indice % 3]:

            st.markdown(
                f"""
                <div class="category-box">
                    {categoria.upper()}
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "VER PRODUCTOS",
                key=f"cat_inicio_{categoria}",
                use_container_width=True
            ):

                st.session_state.categoria_seleccionada = categoria

                st.session_state.vista = "Categoria"

                st.rerun()


    st.markdown(
        '<div class="section-title">PRODUCTOS DESTACADOS</div>',
        unsafe_allow_html=True
    )

    productos = cargar_productos()

    columnas = st.columns(4)

    for indice, producto in enumerate(productos[:12]):

        with columnas[indice % 4]:

            mostrar_producto(producto)


elif st.session_state.vista == "Productos":

    st.markdown(
        '<div class="section-title">TODOS LOS PRODUCTOS</div>',
        unsafe_allow_html=True
    )

    productos = cargar_productos()

    columnas = st.columns(4)

    for indice, producto in enumerate(productos):

        with columnas[indice % 4]:

            mostrar_producto(producto)


elif st.session_state.vista == "Categorías":

    st.markdown(
        '<div class="section-title">CATEGORÍAS</div>',
        unsafe_allow_html=True
    )

    categorias = cargar_categorias()

    columnas = st.columns(4)

    for indice, categoria in enumerate(categorias):

        with columnas[indice % 4]:

            st.markdown(
                f"""
                <div class="category-box">
                    {categoria.upper()}
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "VER",
                key=f"categoria_{categoria}",
                use_container_width=True
            ):

                st.session_state.categoria_seleccionada = categoria

                st.session_state.vista = "Categoria"

                st.rerun()


elif st.session_state.vista == "Categoria":

    categoria = st.session_state.categoria_seleccionada

    st.markdown(
        f"""
        <div class="section-title">
            {categoria.upper()}
        </div>
        """,
        unsafe_allow_html=True
    )

    productos_categoria = (
        obtener_productos_categoria(
            categoria
        )
    )

    if not productos_categoria:

        st.warning(
            "No hay productos en esta categoría."
        )

    else:

        columnas = st.columns(4)

        for indice, producto in enumerate(
            productos_categoria
        ):

            with columnas[indice % 4]:

                mostrar_producto(producto)


elif st.session_state.vista == "Ofertas":

    st.markdown(
        """
        <div class="section-title">
            OFERTAS
        </div>
        """,
        unsafe_allow_html=True
    )

    productos = cargar_productos()

    ofertas = [
        producto
        for producto in productos
        if producto.get(
            "discountPercentage",
            0
        ) >= 10
    ]

    columnas = st.columns(4)

    for indice, producto in enumerate(ofertas):

        with columnas[indice % 4]:

            mostrar_producto(producto)


elif st.session_state.vista == "Carrito":

    st.markdown(
        """
        <div class="section-title">
            MI CARRITO
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.carrito:

        st.info(
            "Tu carrito está vacío."
        )

    else:

        for producto in st.session_state.carrito:

            col1, col2, col3, col4 = st.columns(
                [1, 4, 2, 1]
            )

            with col1:

                st.image(
                    producto["thumbnail"],
                    width=100
                )

            with col2:

                st.write(
                    f"**{producto['title']}**"
                )

                st.write(
                    f"${producto['price']:.2f} USD"
                )

            with col3:

                cantidad = st.number_input(
                    "Cantidad",
                    min_value=1,
                    value=producto["cantidad"],
                    key=f"cantidad_{producto['id']}"
                )

                producto["cantidad"] = cantidad

            with col4:

                if st.button(
                    "❌",
                    key=f"eliminar_{producto['id']}"
                ):

                    quitar_carrito(
                        producto["id"]
                    )

                    st.rerun()

        st.divider()

        total = calcular_total()

        col1, col2 = st.columns(2)

        with col2:

            st.subheader(
                "RESUMEN"
            )

            st.write(
                f"Productos: {cantidad_carrito}"
            )

            st.write(
                f"Total: **${total:.2f} USD**"
            )

            if st.button(
                "FINALIZAR COMPRA",
                use_container_width=True
            ):

                st.success(
                    "Compra simulada correctamente."
                )

