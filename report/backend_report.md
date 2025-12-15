# Báo cáo Backend: WindyAI - Smart Travel Planner

## 1. Tổng quan
WindyAI là một ứng dụng lập kế hoạch du lịch thông minh được xây dựng chủ yếu bằng **Python** và framework **Streamlit**. Ứng dụng tích hợp nhiều thuật toán xử lý dữ liệu (tối ưu lộ trình, gợi ý địa điểm, dự báo thời tiết) và lưu trữ dữ liệu người dùng trên nền tảng đám mây.

## 2. Công nghệ sử dụng (Tech Stack)

### 2.1. Ngôn ngữ & Framework chính
*   **Ngôn ngữ:** Python 3.x
*   **Web App Framework:** Streamlit (v1.34.0+) - Đóng vai trò vừa là Frontend vừa là Backend runner.
*   **API Framework (Dự phòng/Tương lai):** FastAPI - Hiện tại có module `app/api/chatbot_api.py` nhưng chưa phải là entry point chính.

### 2.2. Thư viện xử lý dữ liệu & AI
*   **Data Manipulation:** Pandas, Numpy.
*   **Machine Learning:** PyTorch (`torch`, `torchvision`) - Sử dụng trong module `core/algo3` (dự đoán/phân loại).
*   **Optimization:** Custom implementation trong `core/algo1`:
    *   **Greedy Strategy:** Lựa chọn điểm đến tốt nhất tiếp theo dựa trên điểm số (score).
    *   **Constraints Handling:** Xử lý ràng buộc về thời gian, ngân sách, và **giãn cách các địa điểm ăn uống**.
    *   **Post-optimization:** Sử dụng thuật toán **2-opt** để cải thiện lộ trình sau khi tạo.
*   **Chatbot:** Custom logic (`core/algo6_chatbot`).

### 2.3. Bản đồ & Geospatial
*   **Visualization:** Folium (hiển thị bản đồ tương tác).
*   **Geospatial Data:** OSMnx.
*   **Geocoding & Routing:** Tương tác với API của OpenStreetMap (Nominatim, OSRM).

### 2.4. Cơ sở dữ liệu & Xác thực
*   **Database:** Supabase (PostgreSQL).
    *   Sử dụng thư viện `supabase-py` để kết nối.
    *   Hỗ trợ `sqlite` cho môi trường local hoặc legacy data.
*   **Authentication:**
    *   Xử lý password hashing bằng `bcrypt`.
    *   Quản lý session bằng `extra-streamlit-components` (Cookie Manager).

### 2.5. Các công nghệ khác
*   **Image Processing:** Pillow (`PIL`).
*   **Environment Management:** `python-dotenv`.

## 3. Kiến trúc Hệ thống

### 3.1. Mô hình kiến trúc
Dự án tuân theo mô hình **Modular Monolith**:
*   Toàn bộ ứng dụng (UI, Logic, Data Access) nằm trong một codebase duy nhất và chạy trên cùng một process (Streamlit).
*   Tuy nhiên, code được tổ chức tách biệt rõ ràng giữa các tầng:
    *   **Presentation Layer (`pages/`, `app/`):** Xử lý giao diện người dùng.
    *   **Business Logic Layer (`core/`):** Chứa các thuật toán nghiệp vụ (Routing, AI, Weather).
    *   **Data Access Layer (`services/`):** Xử lý kết nối CSDL và gọi API bên ngoài.

### 3.2. Cấu trúc thư mục (Backend view)
*   `app/`: Điểm khởi chạy ứng dụng (`main.py`), cấu hình (`config.py`).
*   `core/`: Trái tim của backend, chia thành các module thuật toán:
    *   `algo1`: Tối ưu hóa lộ trình (Optimizer).
    *   `algo2`: Mapping & Routing logic.
    *   `algo3`: Mô hình AI (Vietnam prediction model).
    *   `algo4`: Xử lý dữ liệu thời tiết.
    *   `algo5`: Hệ thống gợi ý (Recommender).
    *   `algo6_chatbot`: Chatbot engine.
*   `services/`: Các dịch vụ dùng chung.
    *   `db.py`: Wrapper cho các thao tác với Supabase.
    *   `utils.py`: Các hàm tiện ích.
*   `data/`: Chứa dữ liệu tĩnh (CSV) và dữ liệu huấn luyện.

## 4. Dịch vụ bên ngoài (External Services)

Dự án tích hợp các API của bên thứ ba để cung cấp tính năng:
1.  **Nominatim (OpenStreetMap):** Chuyển đổi tên địa điểm thành tọa độ (Geocoding).
2.  **OSRM (Open Source Routing Machine):** Tính toán đường đi và khoảng cách giữa các điểm.
3.  **OpenWeatherMap:** Lấy dữ liệu dự báo thời tiết thời gian thực.
4.  **Supabase:** Dịch vụ Backend-as-a-Service (BaaS) cung cấp PostgreSQL Database và Auth API.

## 5. Quy trình Build & Run

### 5.1. Môi trường
*   Yêu cầu: Python 3.8+
*   Hệ điều hành: Windows/Linux/macOS (Project hiện đang dev trên Windows).

### 5.2. Các bước triển khai
1.  **Cài đặt dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Cấu hình môi trường:**
    *   Tạo file `.env` chứa các key: `SUPABASE_URL`, `SUPABASE_KEY`, `OPENWEATHER_API_KEY`.
3.  **Khởi chạy ứng dụng:**
    ```bash
    streamlit run app/main.py
    ```
    *   Có thể sử dụng script `start.ps1` trên Windows.

## 6. Tài liệu đính kèm
*   Xem file `report/backend_flowcharts.md` cho các sơ đồ quy trình và kiến trúc chi tiết (Mermaid diagrams).
