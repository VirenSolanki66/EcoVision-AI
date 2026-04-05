
from ultralytics import YOLO
import os

MODEL_PATH = "best.pt"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("best.pt model file not found")

model = YOLO(MODEL_PATH)

def predict_image(image):
    temp_path = "temp.jpg"
    image.save(temp_path)

    results = model.predict(temp_path, verbose=False)

    probs = results[0].probs.data.tolist()
    names = results[0].names

    os.remove(temp_path)

    top3 = sorted(zip(names.values(), probs), key=lambda x: x[1], reverse=True)[:3]
    return top3
