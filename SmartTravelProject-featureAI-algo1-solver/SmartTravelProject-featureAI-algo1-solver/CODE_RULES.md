# ✍️ CODE RULES & DEVELOPMENT GUIDELINES

Đây là bộ quy tắc code chính thức của nhóm, được thiết lập nhằm đảm bảo **tính đồng nhất, chất lượng và khả năng bảo trì** của mã nguồn, đặc biệt là các module Thuật toán cốt lõi.

---

## 1. Quy Tắc Git Workflow (Quản lý Phiên bản)

**Trách nhiệm chính:** Tech Lead (Hoàng Cao Phong) chịu trách nhiệm Code Review và Merge.

### 1.1. Branching Rule
* **main:** Luôn giữ code **ổn định**, đã được kiểm thử (Tested). Không code trực tiếp vào main.
* **Feature Branches:** Mọi tính năng mới phải được phát triển trên nhánh riêng, đặt tên theo format:
    * **Logic/Backend:** `feature/optimization-solver`, `feature/data-processor`
    * **Frontend/UI:** `feature/ui-streamlit`

### 1.2. Quy tắc Commit Message
Sử dụng format tiêu chuẩn **`<LOẠI>: <Mô tả ngắn gọn>`** để lịch sử dễ theo dõi:
* **FEAT** (Feature): Thêm một tính năng/module mới.
* **FIX** (Bug fix): Sửa một lỗi (bug) trong code.
* **DOCS** (Documentation): Sửa/thêm tài liệu (Docstrings, README, CODE_RULES).
* **REFACTOR** (Refactoring): Tối ưu hóa code mà không thay đổi tính năng.

## 2. Quy Tắc Code Style (Python PEP 8 & Học thuật)

### 2.1. Đặt Tên Biến và Hàm
* **Hàm/Biến:** Sử dụng **`snake_case`** (viết thường, dùng gạch dưới).
    * *Ví dụ:* `calculate_cost()`, `max_budget`, `optimized_route`.
* **Class/Lớp:** Sử dụng **`PascalCase`** (viết hoa chữ cái đầu mỗi từ).
    * *Ví dụ:* `CostMatrixSolver`, `RoutePlanner`.
* **Hằng số (CONSTANTS):** Sử dụng **`ALL_CAPS`** (chữ in hoa).
    * *Ví dụ:* `TIME_WINDOW_HOURS = 12`.

### 2.2. Viết Tài liệu (Documentation)
* **Docstrings Bắt buộc:** Tất cả các hàm và Class cốt lõi (đặc biệt là trong module Thuật toán/Solver) **phải có Docstring** giải thích:
    * Mục đích của hàm.
    * Các tham số đầu vào (`Args`).
    * Giá trị trả về (`Returns`).
* **Tránh Magic Numbers:** Tránh sử dụng các con số cố định trực tiếp trong code (ví dụ: `if distance > 1000`). Thay vào đó, định nghĩa chúng là **Hằng số** (CONSTANTS) ở đầu file hoặc comment rõ ràng.