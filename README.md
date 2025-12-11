# 🧠 **MindMeetingAI – Intelligent Meeting Assistant**

*a AI system for meeting summarization, topic extraction, and RAG-based chatbot interaction.*

---

# 👥 **1. Development Team (Team Information)**

| No.   | Full Name            | Email                                                                 | Role                            |
| ----- | -------------------- | --------------------------------------------------------------------- | ------------------------------- |
| **1** | Hoàng Cao Phong      | [hoangcaophong.works@gmail.com](mailto:hoangcaophong.works@gmail.com) | Project Manager & AI Engineer   |
| **2** | Vũ Đức Dương         | [vdduong2438@clc.fitus.edu.vn](mailto:vdduong2438@clc.fitus.edu.vn)   | Backend Developer & Tester      |
| **3** | Nguyễn Phạm Tuấn Đạt | [nptdat2429@clc.fitus.edu.vn](mailto:nptdat2429@clc.fitus.edu.vn)     | UX & Frontend Developer         |
| **4** | Trương Văn Phong     | [truongvanphong12111@gmail.com](mailto:truongvanphong12111@gmail.com) | AI Engineer & Backend Developer |


# 📘 **2. Project Overview**

MindMeetingAI is an AI-powered system designed to enhance meeting workflows by providing:

* Automated meeting summarization
* Extraction of key discussion points
* Action-item recommendations
* A chatbot interface based on **RAG (Retrieval-Augmented Generation)**
* A scalable backend powered by **FastAPI**
* Embedding-based search for internal knowledge retrieval

The system is engineered with modularity and clarity, suitable for academic projects and real-world applications.

---

# ⚙️ **3. Core Features**

| Category            | Description                                            |
| ------------------- | ------------------------------------------------------ |
| **AI Processing**   | Summarization, topic detection, semantic understanding |
| **RAG Pipeline**    | Retrieve relevant documents using FAISS/Chroma         |
| **Embeddings**      | Sentence-Transformers for vectorization                |
| **Backend**         | FastAPI with clean architecture                        |
| **LLM Integration** | OpenAI, Groq, or custom model support                  |

---

# 🛠️ **4. Installation**

### Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
# or
source .venv/bin/activate  # macOS/Linux
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🚀 **5. Running the Server**

```bash
uvicorn app.main:app --reload
```

API Documentation available at:

```
http://localhost:8000/docs
```

---

# 🔐 **6. Environment Variables**

Create a `.env` file:

```
OPENAI_API_KEY=your_key
GROQ_API_KEY=your_key
EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

---

# 📂 **7. Project Structure**

```
app/
 ├── main.py
 ├── api/
 ├── services/
 │     ├── rag_service.py
 │     ├── embedder.py
 │     ├── vector_store.py
 ├── models/
 ├── core/
docs/
 
```

---

# 📄 **8. License**

Licensed under the **MIT License**.

---

<br>

# 🇻🇳 **MindMeetingAI – Trợ lý họp thông minh**


---

# 👥 **1. Thông tin Nhóm (Development Team)**

*(Đã ẩn các thông tin nhạy cảm: ngày sinh, số điện thoại, chữ ký)*

| STT   | Họ và tên            | Email                                                                 | Vai trò                         |
| ----- | -------------------- | --------------------------------------------------------------------- | ------------------------------- |
| **1** | Hoàng Cao Phong      | [hoangcaophong.works@gmail.com](mailto:hoangcaophong.works@gmail.com) | Project Manager & AI Engineer   |
| **2** | Vũ Đức Dương         | [vdduong2438@clc.fitus.edu.vn](mailto:vdduong2438@clc.fitus.edu.vn)   | Backend Developer & Tester      |
| **3** | Nguyễn Phạm Tuấn Đạt | [nptdat2429@clc.fitus.edu.vn](mailto:nptdat2429@clc.fitus.edu.vn)     | UX & Frontend Developer         |
| **4** | Trương Văn Phong     | [truongvanphong12111@gmail.com](mailto:truongvanphong12111@gmail.com) | AI Engineer & Backend Developer |

---

# 📘 **2. Giới thiệu dự án**

MindMeetingAI hỗ trợ quy trình họp bằng cách:

* Tự động tóm tắt nội dung
* Rút trích chủ đề chính
* Đề xuất hành động cần thực hiện
* Chatbot theo cơ chế RAG để hỏi–đáp nội bộ
* Kiến trúc backend FastAPI dễ mở rộng
* Tìm kiếm thông minh dựa trên embeddings

---

# ⚙️ **3. Tính năng chính**

* Summarization (tóm tắt)
* Topic Extraction (trích xuất chủ đề)
* RAG-based Chatbot
* Semantic Search qua Vector DB
* FastAPI API service

---

# 🛠️ **4. Cài đặt**

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

# 🚀 **5. Chạy server**

```bash
uvicorn app.main:app --reload
```

Truy cập tài liệu API tại:

```
http://localhost:8000/docs
```

---

# 🔐 **6. File .env**

```
OPENAI_API_KEY=your_key
GROQ_API_KEY=your_key
EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

---

# 📂 **7. Cấu trúc dự án**

*(Giống phần tiếng Anh)*

---

# 📝 **8. Giấy phép**

MIT License.

---

