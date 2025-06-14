
# 🍽️ Food API – FastAPI + TensorFlow Lite

> Identifica platillos de comida a partir de imágenes usando un modelo **TFLite** entrenado sobre **Food‑101**. Incluye autenticación JWT y documentación Swagger. Este README te guía para levantar el proyecto tanto en **Windows 10/11 x64** como en **macOS Apple Silicon (M1 → M4)**.

---

## Tabla de contenido

1. [Requisitos rápidos (TL;DR)](#tldr)
2. [Instalación paso a paso](#instalacion)
3. [Ejecutar el servidor](#ejecucion)
4. [Flujo de autenticación](#auth-flow)
5. [Endpoint de predicción](#predict-flow)
6. [Estructura del proyecto](#estructura)
7. [Pruebas locales](#pruebas)
8. [Preguntas frecuentes](#faq)

---

## <a name="tldr">1 · Requisitos rápidos (TL;DR)</a>

```bash
# Windows (PowerShell)
python -m venv .venv && .venv\Scripts\Activate.ps1
pip install -r requirements.txt tensorflow-cpu==2.16.1
uvicorn app.main:app --reload

# macOS (zsh) – Apple Silicon
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt tensorflow-macos tensorflow-metal
uvicorn app.main:app --reload
```

Listo: abre `http://localhost:8000/docs` 🚀.

---

## <a name="instalacion">2 · Instalación paso a paso</a>

### 2.1 · Prerrequisitos comunes

| Software           | Versión recomendada  |
| ------------------ | -------------------- |
| **Python**         | **3.10.x (64 bits)** |
| Git                | Último estable       |
| Pip ≥ 22 o Poetry  | Opcional             |
| Visual Studio Code | Para debugging       |

> ⚠️ TensorFlow 2.16 (la última con wheel público) **no** soporta Python 3.12 todavía.

### 2.2 · Windows 10/11 x64

1. **Instala Python 3.10 x64** desde [https://www.python.org/](https://www.python.org/) (asegúrate de habilitar *Add to PATH*).
2. Clona el repo:

   ```bash
   git clone https://github.com/<tu‑usuario>/food-api.git && cd food-api
   ```
3. Crea y activa entorno virtual:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
4. Instala dependencias:

   ```powershell
   pip install -r requirements.txt tensorflow-cpu==2.16.1
   ```

   *¿GPU NVIDIA?* Instala `tensorflow==2.16.1` con CUDA 12; consulta docs oficiales.

### 2.3 · macOS Apple Silicon (M1 – M4)

1. Instala Python 3.10 con **Homebrew** o **pyenv**:

   ```zsh
   brew install pyenv
   pyenv install 3.10.14
   pyenv local 3.10.14
   ```
2. Clona y entra al repo:

   ```zsh
   git clone https://github.com/<tu‑usuario>/food-api.git && cd food-api
   ```
3. Crea/activa entorno virtual:

   ```zsh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
4. Instala dependencias con aceleración Metal:

   ```zsh
   pip install -r requirements.txt tensorflow-macos tensorflow-metal
   ```
5. (Opcional) Verifica que Metal está activo:

   ```python
   >>> import tensorflow as tf; tf.config.list_physical_devices('GPU')
   ```

---

## <a name="ejecucion">3 · Ejecutar el servidor</a>

| Acción                  | Comando                                                  |
| ----------------------- | -------------------------------------------------------- |
| Servidor dev recargable | `uvicorn app.main:app --reload`                          |
| Producción (Gunicorn)   | `gunicorn -k uvicorn.workers.UvicornWorker app.main:app` |
| Swagger UI              | `http://localhost:8000/docs`                             |

<details>
<summary>Variables de entorno opcionales</summary>

| Variable     | Default        | Descripción                  |
| ------------ | -------------- | ---------------------------- |
| `SECRET_KEY` | "supersecreto" | Clave JWT (cámbiala en prod) |
| `PORT`       | 8000           | Puerto de salida             |

</details>

---

## <a name="auth-flow">4 · Flujo de autenticación</a>

1. **Registro**

   ```bash
   curl -X POST http://localhost:8000/auth/register \
        -H "Content-Type: application/json" \
        -d '{"username":"alice","password":"123"}'
   ```
2. **Login** → token JWT

   ```bash
   TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
        -H "Content-Type: application/json" \
        -d '{"username":"alice","password":"123"}' | jq -r .token)
   echo $TOKEN
   ```

> 😊 El token expira en 2 horas; renueva con otro login.

---

## <a name="predict-flow">5 · Endpoint de predicción</a>

```bash
curl -X POST http://localhost:8000/predict/ \
     -H "Authorization: Bearer $TOKEN" \
     -F image=@/ruta/a/foto.jpg
```

Respuesta JSON:

```json
{
  "platillo": "pizza",
  "confianza": 0.87
}
```

Si la confianza < 0.30 → `{"platillo":null,"mensaje":"Esto no es comida"}`.

---

## <a name="estructura">6 · Estructura del proyecto</a>

```
.
├── app
│   ├── __init__.py
│   ├── main.py          ← Entrypoint FastAPI
│   ├── auth.py          ← Registro / login
│   ├── predict.py       ← Endpoint /predict
│   └── core
│       ├── security.py  ← JWT + bcrypt
│       └── tflite_runner.py
│   └── models
│       ├── food_classifier_model.tflite
│       ├── labels.txt
│       └── users.json
├── requirements.txt
└── README.md (este archivo)
```

---

## <a name="pruebas">7 · Pruebas locales</a>

* **PyTest:** `pip install pytest` y coloca tests en `tests/`.
* **Carga rápida:** usa la imagen `tests/assets/pizza.jpg` incluida y verifica que prediga “pizza”.

---

## <a name="faq">8 · Preguntas frecuentes</a>

| Pregunta                                           | Respuesta breve                                                             |
| -------------------------------------------------- | --------------------------------------------------------------------------- |
| *¿Por qué TensorFlow no instala en Apple Silicon?* | Necesitas `tensorflow‑macos` + `tensorflow‑metal`, no el wheel oficial.     |
| *¿Puedo usar GPU NVIDIA en Windows?*               | Sí, instala CUDA 12 y `tensorflow==2.16.1`; ajusta `requirements.txt`.      |
| *¿Es posible recargar modelo al vuelo?*            | Reinicia el proceso o implementa recarga en caliente en `tflite_runner.py`. |
| *¿Qué tamaño tiene el modelo?*                     | \~9 MB; entra sin problemas en RAM y docker.                                |

---

### ¡Eso es todo!

Levanta el servidor, sube tu foto y deja que la IA decida si es pizza o ensalada. 🍕🥗
