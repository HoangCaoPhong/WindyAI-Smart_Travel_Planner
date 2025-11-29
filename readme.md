# Hướng Dẫn Cài Đặt & Chạy Hệ Thống Nhận Diện Ảnh Địa Điểm Việt Nam

> Ví dụ thư mục dự án: `C:\PC\HOC\SmartTravel System\AI image`  
> Các file chính:
> - `train.py` – huấn luyện mô hình
> - `predict_vn.py` (hoặc `backend_model.py`) – nhận diện ảnh từ model đã train

---

## 1. Tạo Môi Trường Ảo & Cài Thư Viện

1. Mở VS Code tại thư mục `AI image`.
2. Mở **Terminal**:
   - Menu: `View → Terminal`.
3. Tạo môi trường ảo:

   ```bash
   python -m venv venv
Kích hoạt môi trường ảo (Windows):

bash
Sao chép mã
venv\Scripts\activate
Khi thành công, đầu dòng lệnh sẽ có (venv).

Cài các thư viện cần thiết:

bash
Sao chép mã
pip install torch torchvision pillow streamlit
2. Chuẩn Bị Dataset
Trong thư mục AI image, tạo cấu trúc:

text
Sao chép mã
AI image/
├─ train.py
├─ predict_vn.py
├─ data/
│  ├─ train/
│  └─ val/
Trong data/train và data/val:

Mỗi địa điểm là một thư mục con.

Tên thư mục chính là tên lớp (label) sẽ dự đoán.

Ví dụ:

text
Sao chép mã
data/
├─ train/
│  ├─ cho_ben_thanh/
│  │   ├─ img1.jpg
│  │   ├─ img2.jpg
│  ├─ nhathoducba/
│  ├─ landmark81/
│  └─ ...
└─ val/
   ├─ cho_ben_thanh/
   ├─ nhathoducba/
   ├─ landmark81/
   └─ ...
Lưu ý:

Ảnh nên ở dạng .jpg, .jpeg hoặc .png.

Tập val dùng để đánh giá model, nên chứa ảnh khác với train.

3. Cấu Hình train.py
Mở train.py và kiểm tra:

python
Sao chép mã
DATA_DIR = "data"   # Thư mục chứa train/ và val/
Nếu bạn đặt tên thư mục khác (ví dụ dataset) thì sửa DATA_DIR cho khớp.

Một số tham số quan trọng:

python
Sao chép mã
BATCH_SIZE = 32
NUM_EPOCHS = 30
LR = 1e-4
PATIENCE = 5
Máy yếu có thể giảm BATCH_SIZE (ví dụ 16) hoặc giảm NUM_EPOCHS.

4. Chạy Huấn Luyện Mô Hình
Trong Terminal (đang ở thư mục AI image, có (venv)):

bash
Sao chép mã
python train.py
Trong quá trình chạy:

In ra: thiết bị (cpu hoặc cuda).

In danh sách lớp, ví dụ:

text
Sao chép mã
Số lớp: 9
Classes: ['cho_ben_thanh', 'nhathoducba', ...]
Mỗi epoch in:

TRAIN Loss / Acc

VAL Loss / Acc

Khi Val Acc tốt hơn, chương trình sẽ lưu:

model_vietnam.pth – trọng số mô hình tốt nhất.

classes.txt – danh sách tên lớp (mỗi dòng 1 lớp).

Sau khi train xong, thư mục có thêm:

text
Sao chép mã
AI image/
├─ model_vietnam.pth
└─ classes.txt
5. Test Backend Nhận Diện Ảnh Trong CMD
Giả sử file backend là predict_vn.py.

Đảm bảo file cùng thư mục với:

model_vietnam.pth

classes.txt

Chạy thử với 1 ảnh:

bash
Sao chép mã
python predict_vn.py q.jpg
Kết quả mong đợi:

text
Sao chép mã
Using device: cpu
Số lớp: 9
Classes: [...]
Kết quả: cho_ben_thanh (độ tin cậy = 95.23%)