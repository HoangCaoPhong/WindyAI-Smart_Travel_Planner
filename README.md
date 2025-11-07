# SmartTravel - Ứng dụng Du lịch Thông minh ✈️

## 📋 Mô tả

SmartTravel là ứng dụng du lịch thông minh sử dụng AI để giúp người dùng:
- 🔍 Tìm kiếm và khám phá địa điểm
- 📸 Nhận diện địa điểm từ ảnh
- 💾 Quản lý bộ sưu tập địa điểm
- 🗺️ Xem bản đồ và chỉ đường

## 🏗️ Cấu trúc Project

```
SmartTravelProject/
├── SmartTravel.py              # File chính để chạy ứng dụng
├── requirements.txt            # Các thư viện cần thiết
├── smarttravel.db             # Database SQLite
├── README.md                  # File này
│
├── src/                       # Source code chính
│   ├── __init__.py
│   │
│   ├── components/            # UI Components
│   │   ├── __init__.py
│   │   └── ui_components.py   # Các component giao diện tái sử dụng
│   │
│   ├── pages/                 # Các trang của ứng dụng
│   │   ├── __init__.py
│   │   ├── page_home.py       # Trang chủ
│   │   ├── page_dashboard.py  # Bảng điều khiển
│   │   ├── page_discover.py   # Trang khám phá
│   │   ├── page_recognize.py  # Trang nhận diện ảnh
│   │   └── page_profile.py    # Trang hồ sơ
│   │
│   └── utils/                 # Tiện ích và helpers
│       ├── __init__.py
│       ├── auth.py            # Xác thực người dùng
│       ├── db_utils.py        # Quản lý database
│       └── constants.py       # Hằng số và cấu hình
│
├── static/                    # File tĩnh
│   ├── css/
│   │   └── style.css         # CSS chính
│   └── images/               # Hình ảnh
│
└── pages/                    # Streamlit multipage (legacy)
    ├── 1_Dashboard.py
    ├── 2_Dang_nhap.py
    ├── 3_Kham_pha.py
    ├── 4_Nhan_dien.py
    └── 5_Ho_so.py
```

## 🚀 Cài đặt

### 1. Clone repository
```bash
git clone https://github.com/HoangCaoPhong/SmartTravelProject.git
cd SmartTravelProject
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Chạy ứng dụng
```bash
streamlit run SmartTravel.py
```

## 📦 Dependencies

- streamlit >= 1.28.0
- pandas >= 2.0.0
- bcrypt >= 4.0.0
- streamlit-option-menu >= 0.3.2
- Pillow >= 10.0.0
- requests >= 2.31.0
- python-dotenv >= 1.0.0

## 🎨 Tính năng UI/UX

### Design System
- **Color Scheme**: Professional blue & teal gradient
- **Typography**: Modern sans-serif font stack
- **Shadows**: Subtle elevation system
- **Borders**: Rounded corners for modern look
- **Animations**: Smooth transitions and hover effects

### Components
- Hero sections with gradient backgrounds
- Feature cards with hover effects
- Stat cards for dashboard
- Location cards with images
- Section headers with icons
- Info boxes with different types
- Empty states
- Loading spinners

### Responsive Design
- Mobile-first approach
- Adaptive layouts
- Touch-friendly buttons

## 🔧 Cấu hình

Các hằng số và cấu hình được tập trung trong `src/utils/constants.py`:

```python
DATABASE_NAME = "smarttravel.db"
USERNAME_MIN_LENGTH = 3
PASSWORD_MIN_LENGTH = 6
PAGE_TITLE = "SmartTravel"
PRIMARY_COLOR = "#1E88E5"
```

## 📊 Database Schema

### Users
- id: INTEGER PRIMARY KEY
- username: TEXT UNIQUE
- password_hash: TEXT

### Search History
- id: INTEGER PRIMARY KEY
- user_id: INTEGER
- query: TEXT
- timestamp: DATETIME

### Collections
- id: INTEGER PRIMARY KEY
- user_id: INTEGER
- name: TEXT

### Saved Places
- id: INTEGER PRIMARY KEY
- collection_id: INTEGER
- place_name: TEXT
- address: TEXT
- image_url: TEXT
- latitude: REAL
- longitude: REAL

## 🔐 Authentication

- Bcrypt password hashing
- Session-based authentication
- Secure login/register system
- Password validation rules

## 🛣️ Roadmap

### Phase 1 (Current)
- ✅ UI/UX redesign
- ✅ Project structure reorganization
- ✅ Authentication system
- ✅ Database setup

### Phase 2 (Coming Soon)
- 🔄 AI image recognition integration
- 🔄 Search API integration
- 🔄 Recommendation system
- 🔄 Map integration

### Phase 3 (Future)
- 📋 Advanced filtering
- 📊 Analytics dashboard
- 🌐 Multi-language support
- 📱 Mobile app version

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

Made with ❤️ by SmartTravel Team
