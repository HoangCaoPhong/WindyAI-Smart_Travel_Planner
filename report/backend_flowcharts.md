# Sơ đồ Kiến trúc Backend và Quy trình

Dưới đây là các sơ đồ minh họa kiến trúc và luồng dữ liệu của hệ thống WindyAI, sử dụng cú pháp Mermaid.

## 1. Sơ đồ Kiến trúc Tổng quan (System Architecture)

```mermaid
graph TD
    User[Người dùng cuối] -->|Tương tác qua Browser| UI[Streamlit Frontend]
    
    subgraph "Application Server (Local/Cloud)"
        UI -->|Gọi hàm| Controller["App Controller (pages/)"]
        
        subgraph "Core Business Logic"
            Controller --> Algo1[Algo1: Optimizer]
            Controller --> Algo2[Algo2: Routing]
            Controller --> Algo3[Algo3: AI Model]
            Controller --> Algo4[Algo4: Weather]
            Controller --> Algo5[Algo5: Recommender]
            Controller --> Algo6[Algo6: Chatbot]
        end
        
        subgraph "Data Access Layer"
            Controller --> DBSvc["Services/DB"]
            Algo2 --> ExtAPI[External API Handler]
            Algo4 --> ExtAPI
        end
    end
    
    subgraph "External Services"
        DBSvc -->|Supabase Client| Supabase[("Supabase PostgreSQL")]
        ExtAPI -->|HTTP Requests| Nominatim[Nominatim Geocoding]
        ExtAPI -->|HTTP Requests| OSRM[OSRM Routing]
        ExtAPI -->|HTTP Requests| OWM[OpenWeatherMap]
    end
```

## 2. Luồng xử lý tạo lịch trình (Schedule Creation Flow)

```mermaid
sequenceDiagram
    participant User
    participant App as "Streamlit UI"
    participant Core as "Core Logic"
    participant Ext as "External APIs"
    participant DB as Supabase
    
    User->>App: Nhập điểm đến, thời gian, sở thích
    App->>Core: Gửi dữ liệu đầu vào
    
    opt Xử lý Logic
        Core->>Ext: Lấy thông tin thời tiết (Algo4)
        Ext-->>Core: Dữ liệu thời tiết
        Core->>Core: Lọc địa điểm phù hợp (Algo5)
        Core->>Ext: Lấy tọa độ và khoảng cách (Algo2)
        Ext-->>Core: Geo Data
        Core->>Core: Tối ưu hóa lộ trình (Algo1)
    end
    
    Core-->>App: Trả về Lịch trình đề xuất
    App->>User: Hiển thị lịch trình
    
    User->>App: Xác nhận lưu
    App->>DB: Lưu lịch trình (Services/DB)
    DB-->>App: Xác nhận thành công
    App-->>User: Thông báo thành công
```

## 3. Luồng xác thực người dùng (Authentication Flow)

```mermaid
sequenceDiagram
    participant User
    participant App as Streamlit UI
    participant DB as Supabase
    participant Cookie as Cookie Manager
    
    User->>App: Nhập Email/Password
    App->>DB: Gửi truy vấn xác thực
    DB->>DB: Kiểm tra hash password (bcrypt)
    
    alt Thông tin đúng
        DB-->>App: Trả về User Info & ID
        App->>Cookie: Set Cookie (Session)
        App->>App: Rerun/Redirect to Home
        App-->>User: Đăng nhập thành công
    else Thông tin sai
        DB-->>App: Trả về lỗi
        App-->>User: Hiển thị lỗi đăng nhập
    end
```

## 4. Chi tiết thuật toán tối ưu lộ trình (Algo1 Logic)

```mermaid
flowchart TD
    Start([Bắt đầu]) --> LoadPOIs[Load & Filter POIs]
    LoadPOIs --> Init[Khởi tạo: Start Loc, Time, Budget]
    Init --> Loop{Còn Candidate?}
    
    Loop -- Yes --> Score[Tính điểm Candidate]
    Score --> Filter[Lọc theo Ràng buộc]
    
    subgraph Constraints
        Filter --> CheckTime{Đủ thời gian?}
        Filter --> CheckBudget{Đủ ngân sách?}
        Filter --> CheckFood{Giãn cách ăn uống?}
    end
    
    CheckTime -- No --> NextCand[Bỏ qua]
    CheckBudget -- No --> NextCand
    CheckFood -- No --> NextCand
    
    CheckTime -- Yes --> Select[Chọn Best Candidate]
    CheckBudget -- Yes --> Select
    CheckFood -- Yes --> Select
    
    Select --> Update[Cập nhật: Time, Budget, Loc]
    Update --> Loop
    
    Loop -- No --> Optimize[Chạy 2-Opt Optimization]
    Optimize --> End([Trả về Lộ trình])
    
    NextCand --> Loop
```

## 5. Quy trình Chatbot (Algo6 Design)

Mặc dù hiện tại là phiên bản đơn giản, kiến trúc thiết kế cho Chatbot tuân theo mô hình RAG (Retrieval-Augmented Generation):

```mermaid
flowchart LR
    User[User Message] --> Intent[Intent Classifier]
    Intent --> Check{Intent Type?}
    
    Check -- "Greeting/Chitchat" --> Response[Response Generator]
    Check -- "Travel Query" --> KB[Knowledge Base Search]
    
    KB --> Context[Retrieve Context]
    Context --> Response
    
    Response --> Output[Final Answer]
```

## 6. Quy trình Nhận diện ảnh (Algo3 Pipeline)

```mermaid
flowchart TD
    Input[Upload Image] --> Preprocess[Preprocess: Resize/Normalize]
    Preprocess --> Model[ResNet18 Model Inference]
    Model --> Softmax[Softmax Probability]
    Softmax --> TopK[Get Top-1 Class]
    TopK --> Output[Return Location Name]
```
```
