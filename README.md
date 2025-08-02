# 🏆 Proyecto: Gestor de Contenido Personal

Este proyecto consiste en el desarrollo de una aplicación de consola en Python orientada a la gestión de una colección personal de contenido (libros, películas y música), utilizando un archivo JSON local como mecanismo de persistencia. El sistema está diseñado de forma modular y funcional para permitir una gestión ordenada de los elementos, incluyendo funcionalidades de creación, búsqueda, edición y eliminación.

# 📋 Contenido
- [🏆 Proyecto: Gestor de Contenido Personal (Python + JSON)](#-proyecto-gestor-de-contenido-personal-python--json)
- [📋 Contenido](#-contenido)
- [💾 Instalación](#-instalación)
- [🖥️ Uso](#️-uso)
- [✨ Funcionalidades Implementadas](#-funcionalidades-implementadas)
  - [1. ✍️ Gestión de Elementos (CRUD)](#1-️-gestión-de-elementos-crud)
  - [2. 🔍 Búsqueda y Visualización](#2--búsqueda-y-visualización)
  - [3. 💾 Persistencia y Guardado](#3--persistencia-y-guardado)
- [📂 Arquitectura del Proyecto](#-arquitectura-del-proyecto)
- [✔️ Validaciones y Manejo de Errores](#️-validaciones-y-manejo-de-errores)
- [✉️ Autor y Contacto](#️-autor-y-contacto)


# 💾 Instalación

Para ejecutar este proyecto, únicamente es necesario tener **Python 3** instalado. No requiere librerías externas.

1.  **Clona o descarga el repositorio** en tu máquina local.
2.  **Abre una terminal** en la carpeta raíz del proyecto (`Gestor_Contenido/`).
3.  **Ejecuta la aplicación**. Inicia el programa con el siguiente comando:
    ```bash
    python app/main.py
    ```

# 🖥️ Uso

La aplicación se controla completamente desde el teclado, ofreciendo una experiencia de usuario interactiva y fluida a través de la consola.

-   Usa las flechas **▲/▼** para navegar por las opciones de los menús.
-   Presiona **Enter** (una sola vez) para seleccionar una opción o confirmar una entrada.
-   Presiona **Escape (Esc)** para cancelar una acción o volver al menú anterior.
-   Al registrar datos, escribe **`!cancelar`** y presiona **Enter** para anular una entrada específica.


# ✨ Funcionalidades Implementadas

El sistema cuenta con tres áreas funcionales principales:

### 1. ✍️ Gestión de Elementos (CRUD)

-   **Añadir Elementos**: Permite registrar nuevos ítems seleccionando primero su categoría (Libro, Película, Música). El sistema solicita y valida los datos correspondientes como título, responsable, género y una valoración opcional.
-   **Editar Elementos**: Ofrece un flujo guiado para seleccionar cualquier elemento existente y modificar sus campos uno por uno. Muestra el valor actual de cada campo y permite guardar o cancelar los cambios de forma segura.
-   **Eliminar Elementos**: Permite seleccionar un elemento de la colección y eliminarlo de forma permanente, previa confirmación para evitar borrados accidentales.

### 2. 🔍 Búsqueda y Visualización

-   **Ver Colección Completa**: Muestra una tabla clara y formateada con todos los elementos de la colección, incluyendo ID, categoría, título, responsable, género y valoración.
-   **Búsqueda por Criterio**: Permite buscar elementos filtrando por título, responsable o género. La búsqueda no distingue mayúsculas de minúsculas y encuentra coincidencias parciales.
-   **Filtrar por Categoría**: Muestra un menú con las categorías existentes (Libro, Película, Música) para visualizar únicamente los elementos que pertenecen a la categoría seleccionada.

### 3. 💾 Persistencia y Guardado

-   **Guardado en JSON**: Todos los datos de la colección se guardan en el archivo `data/coleccion.json` de forma organizada.
-   **Gestión de Cambios sin Guardar**: La aplicación detecta si se han realizado cambios (añadir, editar, eliminar) y lo indica visualmente en el título del menú con un `[*]`.
-   **Guardado Manual y Automático al Salir**: El usuario puede guardar los cambios explícitamente desde el menú principal. Si intenta salir con cambios pendientes, el programa le preguntará si desea guardar, salir sin guardar o cancelar la salida.

# 📂 Arquitectura del Proyecto

El código está organizado de forma modular para facilitar su mantenimiento y escalabilidad, siguiendo una separación clara de responsabilidades.
```
Gestor_Contenido/
│
├── app/
│   └── main.py              # Punto de entrada, bucle principal y menú.
│
├── controllers/             # Lógica de negocio por módulo
│   ├── element_manager.py   # Lógica para añadir, editar y eliminar (CRUD).
│   └── search_operations.py # Lógica para búsquedas y filtrado de elementos.
│
├── utils/                     # Módulos de utilidades y herramientas reusables
│   ├── corefiles.py         # Funciones centrales para leer y escribir el JSON.
│   ├── screencontroller.py  # Módulos para la interfaz: menús, inputs, etc.
│   ├── styles.py            # Constantes para colores y estilos de la terminal.
│   └── validateData.py      # Funciones para la validación de datos.
│
├── data/                      # Archivos de datos persistentes
│   └── coleccion.json       # Almacena toda la colección en formato JSON.
│
└── README.md                  # Documentación del proyecto.
```
# ✔️ Validaciones y Manejo de Errores

El sistema implementa varias capas de validación para garantizar la integridad de los datos y una experiencia de usuario sin errores.

-   **Unicidad de Títulos**: No permite registrar un elemento si su título ya existe en la colección (ignorando mayúsculas/minúsculas).
-   **Validación de Formato de Texto**:
    -   **Sin Símbolos**: La mayoría de los campos de texto (título, responsable) solo permiten caracteres alfanuméricos y espacios.
    -   **Solo Letras**: El campo "Género" solo admite letras y espacios.
    -   **Rechazo de Entradas Vacías**: El sistema no permite registrar campos que contengan únicamente espacios en blanco.
-   **Validación de Formato Numérico**: Verifica que la valoración sea un número válido y que esté en el rango correcto (1-5).
-   **Flujo de Corrección de Errores Mejorado**: Si el usuario introduce un dato incorrecto, el sistema muestra un mensaje de error claro y le permite corregir la entrada en el mismo lugar, sin desordenar la pantalla ni requerir acciones adicionales.
-   **Guía al Usuario y Cancelación**: El programa guía al usuario con menús interactivos y permite cancelar cualquier operación de forma segura usando `!cancelar` o la tecla `Esc`.

# ✉️ Autor y Contacto

Desarrollado por:

-   **Nombre**: Santiago Andres Gallo Salamanca
-   **Grupo**: J3
-   **Correo Electrónico**: santiagogal7i@gmail.com
