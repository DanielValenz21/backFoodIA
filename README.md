# 🍽️ Food API – FastAPI + TensorFlow Lite

API REST que identifica platillos de comida a partir de imágenes usando un modelo **TensorFlow Lite** entrenado sobre el dataset **Food-101** y ofrece registro / login con JWT, además de documentación Swagger automática.

---

## 1. Requisitos

| SO / arquitectura                  | Python | Paquete TensorFlow recomendado | Notas                             |
| ---------------------------------- | ------ | ------------------------------ | --------------------------------- |
| **macOS Apple Silicon (M1/M2/M3)** | 3.10.x | `tensorflow-macos==2.16.1`     | Rinde gracias a aceleración Metal |
| **macOS Intel**                    | 3.10.x | `tensorflow-cpu==2.16.1`       | Sólo CPU                          |
| **Linux (x86\_64)**                | 3.10.x | `tensorflow-cpu==2.16.1`       |                                   |
| **Windows 10/11 (x86\_64)**        | 3.10.x | `tensorflow-cpu==2.16.1`       | Asegúrate de 64 bits              |

> ⚠️ Python ≥ 3.11 aún no ofrece binarios estables para TensorFlow. Usa 3.10.

Otras dependencias (instaladas vía `pip` / `requirements.txt`):
`fastapi`, `uvicorn[standard]`, `python-multipart`, `bcrypt`, `python-jose[cryptography]`, `Pillow`.

---

## 2. Instalación local

### macOS / Linux

```bash
# Clona repo y entra
 git clone https://github.com/tu-usuario/food-api-python.git
 cd food-api-python

# Crea y activa venv
 python3.10 -m venv venv
 source venv/bin/activate

# Actualiza pip e instala dependencias
 python -m pip install --upgrade pip
 pip install -r requirements.txt tensorflow-macos==2.16.1       # Apple Silicon
# ó
 pip install -r requirements.txt tensorflow-cpu==2.16.1          # Intel / Linux
```

### Windows PowerShell / CMD

```powershell
REM Clonar y entrar
git clone https://github.com/tu-usuario/food-api-python.git
cd food-api-python

REM Crear virtualenv (usa la ruta a tu Python 3.10)
py -3.10 -m venv venv

REM Activar venv
venv\Scripts\activate

REM Actualizar pip e instalar
python -m pip install --upgrade pip
pip install -r requirements.txt tensorflow-cpu==2.16.1
```

---

## 3. Archivos imprescindibles

```
app/models/food_classifier_model.tflite    ← modelo IA
app/models/labels.txt                      ← 101 etiquetas Food-101
```

Si pierdes `labels.txt` puedes regenerarlo:

```python
import tensorflow_datasets as tfds
labels = tfds.builder('food101').info.features['label'].names
open('app/models/labels.txt','w').write('\n'.join(labels))
```

---

## 4. Estructura del proyecto

```
app/
├── core/
│   ├── security.py          # Hash + JWT
│   └── tflite_runner.py     # Carga y predice
├── models/
│   ├── food_classifier_model.tflite
│   ├── labels.txt
│   └── users.json           # "BD" demo
├── auth.py                  # Rutas /auth
├── predict.py               # Ruta /predict
└── main.py                  # Arranque FastAPI
```

---

## 5. Levantar la API

```bash
# Con venv activo
activate   # (macOS/Linux ya está activo; Windows: venv\Scripts\activate)

python -m uvicorn app.main:app --reload --port 8000
```

Consola → `Uvicorn running on http://127.0.0.1:8000`

### Documentación interactiva

* Swagger-UI → [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc      → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 6. Uso paso a paso

### 6.1 Registro

```bash
curl -X POST http://localhost:8000/auth/register \
     -H "Content-Type: application/json" \
     -d '{"username":"dan","password":"123"}'
```

### 6.2 Login

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
        -H "Content-Type: application/json" \
        -d '{"username":"dan","password":"123"}' | python -c "import sys, json; print(json.load(sys.stdin)['token'])")
```

### 6.3 Predicción

```bash
curl -X POST http://localhost:8000/predict/ \
     -H "Authorization: Bearer $TOKEN" \
     -F image=@burger.jpg
```

Respuesta típica:

```json
{
  "platillo": "hamburger",
  "confianza": 0.87
}
```

Si `confianza < 0.30` →

```json
{"platillo": null, "mensaje": "Esto no es comida", "confianza": 0.12}
```

---

## 7. Docker (opcional)

```bash
# Construir
docker build -t food-api .
# Ejecutar
docker run -p 8000:8000 food-api
```

---

## 8. Notas técnicas

* **Modelo**: MobileNetV2 + capas custom, entrenado 10 épocas sobre Food-101.
* **Formato**: `.tflite` ⇒ ligero, portable.
* **Inferencia**: `tf.lite.Interpreter` incluido en TensorFlow.
* **Seguridad**: JWT (expira en 2 h), contraseñas bcrypt.
* **Persistencia demo**: `users.json`. En producción cambia a PostgreSQL, MongoDB, etc.

---

## 9. Créditos

Proyecto académico – Universidad Mazatenango, Ingeniería en Sistemas.
IA entrenada y backend desarrollado por **Daniel Valenzuela**.
