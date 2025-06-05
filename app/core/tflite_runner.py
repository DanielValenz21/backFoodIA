# app/core/tflite_runner.py
# ------------------------------------------------------------
#  Carga el modelo TFLite con tensorflow.lite.Interpreter
#  y expone la función predict(image_bytes) para FastAPI
# ------------------------------------------------------------
import os, io
import numpy as np
import tensorflow as tf            # ← ahora usamos TensorFlow completo
from PIL import Image

# Ruta al modelo .tflite y al archivo de etiquetas
BASE_DIR   = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "food_classifier_model.tflite")
LABELS_PATH = os.path.join(BASE_DIR, "..", "models", "labels.txt")

# Cargar etiquetas (101 líneas)
LABELS = [l.strip() for l in open(LABELS_PATH, 'r', encoding='utf-8')]

# Inicializar Intérprete TFLite UNA sola vez
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
inp_idx  = interpreter.get_input_details()[0]['index']
out_idx  = interpreter.get_output_details()[0]['index']

def preprocess(image_bytes: bytes) -> np.ndarray:
    """Convierte bytes de imagen a tensor 1x224x224x3 float32 [0,1]."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((224, 224))
    arr = np.expand_dims(np.array(img) / 255.0, axis=0).astype('float32')
    return arr

def predict(image_bytes: bytes) -> dict:
    """Devuelve platillo y confianza o mensaje 'no comida'."""
    input_tensor = preprocess(image_bytes)

    interpreter.set_tensor(inp_idx, input_tensor)
    interpreter.invoke()
    probs = interpreter.get_tensor(out_idx)[0]

    idx   = int(np.argmax(probs))
    conf  = float(probs[idx])

    if conf < 0.30:
        return {"platillo": None, "mensaje": "Esto no es comida", "confianza": conf}

    return {"platillo": LABELS[idx], "confianza": conf}
