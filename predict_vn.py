# backend_model.py
import sys
import io
import torch
from torchvision import models, transforms
from PIL import Image

MODEL_PATH = "model_vietnam.pth"   
CLASSES_PATH = "classes.txt"      

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# ========================
# 1. LOAD CLASS NAMES
# ========================
with open(CLASSES_PATH, "r", encoding="utf-8") as f:
    CLASS_NAMES = [line.strip() for line in f.readlines()]

num_classes = len(CLASS_NAMES)
print("Số lớp:", num_classes)
print("Classes:", CLASS_NAMES)

# ========================
# 2. LOAD MODEL
# ========================
model = models.resnet18(weights=None)   
in_features = model.fc.in_features
model.fc = torch.nn.Linear(in_features, num_classes)

state_dict = torch.load(MODEL_PATH, map_location=device)
model.load_state_dict(state_dict)
model.eval()
model.to(device)

# ========================
# 3. TIỀN XỬ LÝ ẢNH

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])

# ========================
# 4. CORE PREDICT
# ========================
def _predict_tensor(img_tensor: torch.Tensor):
    """
    img_tensor: [1, 3, 224, 224] đã preprocess & đưa lên device
    """
    with torch.no_grad():
        outputs = model(img_tensor)
        probs = torch.softmax(outputs, dim=1)
        conf, pred_idx = torch.max(probs, 1)
        pred_idx = pred_idx.item()
        conf = conf.item()

    label = CLASS_NAMES[pred_idx]
    return label, conf

# ========================
# 5. HÀM PUBLIC – DÙNG LẠI
# ========================
def predict_image_path(image_path: str):
    """Dự đoán từ đường dẫn file ảnh (dùng CMD / Tkinter / script)."""
    img = Image.open(image_path).convert("RGB")
    tensor = preprocess(img).unsqueeze(0).to(device)
    return _predict_tensor(tensor)

def predict_pil_image(img: Image.Image):
    """Dự đoán từ PIL Image (dùng cho Streamlit, Tkinter)."""
    img = img.convert("RGB")
    tensor = preprocess(img).unsqueeze(0).to(device)
    return _predict_tensor(tensor)

def predict_image_bytes(image_bytes: bytes):
    """Dự đoán từ bytes ảnh (upload web, socket, v.v.)."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = preprocess(img).unsqueeze(0).to(device)
    return _predict_tensor(tensor)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cách dùng: python backend_model.py path/to/image.jpg")
        sys.exit(1)

    image_path = sys.argv[1]
    label, confidence = predict_image_path(image_path)
    print(f"Kết quả: {label} (độ tin cậy = {confidence*100:.2f}%)")
