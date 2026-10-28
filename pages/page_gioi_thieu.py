"""Trang Giới thiệu - Smart Travel Planner"""
import streamlit as st
import base64
import os
import time
from services.feedback import init_feedback_db, add_feedback, get_all_feedback

# ==========================================
# 1. CẤU HÌNH
# ==========================================

PROJECT_INFO = {
    "name": "WindyAI",
    "slogan": "Smart Travel Planner - Du lịch thông minh trong tầm tay",
    "desc": "Hệ thống lập kế hoạch du lịch tự động sử dụng AI.",
    "tech_stack": ["Python", "Streamlit", "FastAPI", "Google Maps API", "Deep Learning", "RecSys"],
    "contact": {
        "address": "227 Nguyễn Văn Cừ, Quận 5, TP.HCM (HCMUS)",
        "email": "hoangcaophong.works@gmail.com",
        "phone": "0123 456 789",
    }
}

MEMBERS = [
    {
        "mssv": "24127486", "name": "Hoàng Cao Phong", "role": "Leader",
        "tech_role": "PM & AI Engineer", "email": "hoangcaophong.works@gmail.com",
        "hobby": "Ngủ, Đọc sách, Đá bóng",
    },
    {
        "mssv": "24127294", "name": "Võ Mỹ Ngọc", "role": "Secretary",
        "tech_role": "Tester & Frontend Dev", "email": "vmngoc2433@clc.fitus.edu.vn",
        "hobby": "Ngủ",
    },
    {
        "mssv": "24127570", "name": "Võ Thúc Trí", "role": "Member",
        "tech_role": "AI & Backend Dev", "email": "vttri2418@clc.fitus.edu.vn",
    },
    {
        "mssv": "24127068", "name": "Nguyễn Trung Kiên", "role": "Member",
        "tech_role": "Data & Fullstack Dev", "email": "ntkien2468@clc.fitus.edu.vn",
    },
    {
        "mssv": "24127569", "name": "Nguyễn Minh Trí", "role": "Member",
        "tech_role": "UX/UI & Frontend Dev", "email": "mntri2437@clc.fitus.edu.vn",
    },
]

# ==========================================
# 2. GIAO DIỆN & CSS
# ==========================================

def get_logo_img():
    # Use the new assets path
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logo_path = os.path.join(current_dir, "assets", "logo", "logo.png")
    # Fallback if png not found, try the other one
    if not os.path.exists(logo_path):
         logo_path = os.path.join(current_dir, "assets", "logo", "Final_WindyAI_Logo_WindyAI_Logo_(RemoveBackgroud).png.png")
    return logo_path

def inject_custom_css():
    st.markdown("""
    <style>
        .main-header {
            color: #11263e; font-family: 'Plus Jakarta Sans','Be Vietnam Pro',sans-serif;
            font-weight: 800; font-size: clamp(2.1rem, 4vw, 3.25rem);
            line-height: 1.2; letter-spacing: -.04em; margin: .3rem 0 .5rem;
        }
        .sub-header { color: #344d68; font-size: 1.05rem; line-height: 1.65; margin-bottom: 1rem; }

        .feature-card {
            background: white; border-radius: 16px; padding: 28px;
            box-shadow: 0 10px 26px rgba(12,42,76,.06); border: 1px solid #ccdaea;
            min-height: 240px; height: 100%; transition: all 0.2s ease;
        }
        .feature-card:hover {
            transform: translateY(-3px); box-shadow: 0 18px 34px rgba(12,42,76,.12); border-color: #80ade7;
        }
        .feature-index { display:inline-flex; padding:.3rem .5rem; border-radius:6px; background:#eaf4ff; color:#0754b1; font-size:.76rem; font-weight:800; letter-spacing:.08em; margin-bottom:1.3rem; }
        .feature-card h4 { color:#11263e; margin:0 0 .8rem; font-family:'Plus Jakarta Sans','Be Vietnam Pro',sans-serif; font-size:1.28rem; font-weight:700; line-height:1.35; }
        .feature-card p { color:#52677f; margin:0; font-size:.95rem; line-height:1.7; }
        .tech-badge { text-align:center; border:1px solid #ccdaea; background:#fff; padding:12px 8px; border-radius:10px; color:#173756; font-size:.9rem; font-weight:700; }
        .tech-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:12px; }
        @media(max-width:600px) { .tech-grid { grid-template-columns:repeat(2,minmax(0,1fr)); } }

        .member-card-container {
            background-color: white; border: 1px solid #E2E8F0; border-radius: 20px 20px 0 0;
            overflow: hidden; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        }
        .card-cover { height: 90px; background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%); width: 100%; }
        .avatar-container {
            width: 110px; height: 110px; margin: -55px auto 10px auto;
            border-radius: 50%; border: 5px solid white; overflow: hidden; background: white;
            position: relative; z-index: 10; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .member-name { font-weight: 700; color: #1E293B; font-size: 1.15rem; margin-top: 5px; }
        .member-mssv { color: #465d74; font-size: 0.9rem; margin-bottom: 8px; }

        /* Badge chức vụ – làm nổi bật hơn */
        .role-badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 12px;
            border: 1px solid rgba(148, 163, 184, 0.6);
        }

        /* ==== CHUYÊN MÔN NỔI BẬT ==== */
        .tech-line {
            border-top: 1px dashed #E2E8F0;
            padding: 14px 0;
            margin-top: 5px;
            background: linear-gradient(90deg, #EFF6FF 0%, #DBEAFE 100%);
            color: #1E3A8A;
            font-size: 0.95rem;
            font-weight: 600;
        }
        .tech-label {
            display: block;
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #64748B;
            margin-bottom: 2px;
        }

        .contact-info-box { padding: 15px; background: #fff; border-radius: 12px; border: 1px solid #ccdaea; margin-bottom: 10px; }
        .contact-label { font-weight: 600; color: #1E293B; font-size: 0.9rem; }
        .contact-value { color: #465d74; font-size: 0.95rem; }

        .skill-tag {
            background: #EFF6FF; color: #1D4ED8; padding: 5px 10px; border-radius: 8px;
            margin-right: 5px; margin-bottom: 5px; display: inline-block; border: 1px solid #BFDBFE; font-size: 0.85rem;
        }

        /* ==== SIDE PEEK: 1/2 MÀN HÌNH, KHÔNG BÓNG MỜ ==== */

        [data-testid="stDialog"] {
            background: transparent !important;
            backdrop-filter: none !important;
            align-items: stretch;
            justify-content: flex-end;
        }

        [data-testid="stDialog"] > div {
            background: transparent !important;
            box-shadow: none !important;
        }

        [data-testid="stDialog"] > div:last-child,
        [data-testid="stDialog"] > div:last-child > div {
            width: 50vw !important;
            max-width: 50vw !important;
            margin-left: auto !important;
            margin-right: 0 !important;
            height: 100vh;
            border-radius: 24px 0 0 24px;
            overflow-y: auto;
        }
    </style>
    """, unsafe_allow_html=True)


# ========= HÀM XỬ LÝ ẢNH THÀNH VIÊN (LOCAL + FALLBACK) =========

def get_image_base64(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_member_img_src(member) -> str:
    """
    Ưu tiên dùng ảnh local: assets/images/members/<mssv>.png|.jpg|.jpeg
    Nếu không có thì dùng 1 avatar placeholder.
    """
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_dir = os.path.join(current_dir, "assets", "images", "members")

    mssv = member.get("mssv", "")
    
    # Check if explicit image is provided
    if "image" in member:
        candidates = [member["image"]]
    else:
        candidates = [
            f"{mssv}.png",
            f"{mssv}.jpg",
            f"{mssv}.jpeg",
        ]

    for filename in candidates:
        img_path = os.path.join(img_dir, filename)
        if os.path.exists(img_path):
            ext = os.path.splitext(filename)[1].lower()
            mime = "image/png" if ext == ".png" else "image/jpeg"
            b64 = get_image_base64(img_path)
            return f"data:{mime};base64,{b64}"

    # fallback: dùng avatar mặc định nếu không có ảnh local
    return "https://cdn-icons-png.flaticon.com/512/4140/4140037.png"


def create_member_card_html(member):
    img_src = get_member_img_src(member)
    role = member["role"]

    # Làm Leader nổi bật hơn
    if "Leader" in role:
        badge_css = (
            "background: linear-gradient(90deg,#2563EB,#4F46E5);"
            "color: #FFFFFF;"
            "box-shadow: 0 10px 20px -5px rgba(37,99,235,0.55);"
            "border: 1px solid rgba(191,219,254,0.9);"
        )
        role_label = f"{role.upper()}"
    elif "Secretary" in role:
        badge_css = "background: #FCE7F3; color: #BE185D;"
        role_label = role.upper()
    else:
        badge_css = "background: #F1F5F9; color: #475569;"
        role_label = role.upper()

    return f"""
    <div class="member-card-container">
        <div class="card-cover"></div>
        <div class="avatar-container">
            <img src="{img_src}" style="width: 100%; height: 100%; object-fit: cover;">
        </div>
        <div class="member-name">{member['name']}</div>
        <div class="member-mssv">{member['mssv']}</div>
        <span class="role-badge" style="{badge_css}">{role_label}</span>
        <div class="tech-line">
            <span class="tech-label">Chuyên môn chính</span>
            {member['tech_role']}
        </div>
    </div>
    """

# ==========================================
# 3. DIALOG HỒ SƠ KIỂU SIDE-PEEK
# ==========================================

@st.dialog("Hồ sơ thành viên")
def show_member_modal():
    idx = st.session_state.get("current_member_idx", 0)
    member = MEMBERS[idx]
    img_src = get_member_img_src(member)

    c1, c2 = st.columns([1, 2], gap="large")
    with c1:
        st.markdown(f"""
            <div style="text-align: center;">
                <img src="{img_src}" style="width: 170px; height: 170px; border-radius: 50%; object-fit: cover; border: 4px solid #3B82F6; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.15);">
                <h3 style="color: #F97316; margin-top: 15px; margin-bottom: 5px;">{member['name']}</h3>
                <p style="color: #64748B; font-family: monospace; background: #F1F5F9; display: inline-block; padding: 4px 12px; border-radius: 6px;">{member['mssv']}</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(
            f"### 🎯 Vai trò: <span style='color:#2563EB'>{member['role']}</span>",
            unsafe_allow_html=True
        )
        st.success(f"Chuyên môn: {member['tech_role']}")
        st.markdown("---")
        st.markdown(f"**Email:** `{member['email']}`")
        st.markdown(f"**Sở thích:** {member.get('hobby', 'Đang cập nhật')}")
    st.markdown("---")
    col_prev, col_close, col_next = st.columns([1, 1, 1])

    with col_prev:
        if st.button("⬅ Trước", key="btn_prev_member"):
            st.session_state.current_member_idx = (idx - 1) % len(MEMBERS)
            st.rerun()

    with col_close:
        if st.button("Đóng", key="btn_close_member"):
            st.session_state.show_member_modal = False
            st.rerun()

    with col_next:
        if st.button("Tiếp ➡", key="btn_next_member"):
            st.session_state.current_member_idx = (idx + 1) % len(MEMBERS)
            st.rerun()

# ==========================================
# 4. CONTACT & ADMIN
# ==========================================


def render_contact_section():
    st.markdown("### Liên hệ & Góp ý")
    col_info, col_form = st.columns([1, 1.5], gap="large")

    with col_info:
        info = PROJECT_INFO['contact']
        st.markdown(f"""
        <div class="contact-info-box">
            <div class="contact-label">Địa chỉ</div>
            <div class="contact-value">{info['address']}</div>
        </div>
        <div class="contact-info-box">
            <div class="contact-label">Email</div>
            <div class="contact-value">{info['email']}</div>
        </div>
        <div class="contact-info-box">
            <div class="contact-label">Hotline</div>
            <div class="contact-value">{info['phone']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        with st.container(border=True):
            st.markdown("##### Gửi tin nhắn cho chúng tôi")
            with st.form("contact_form", clear_on_submit=True):
                c_name, c_email = st.columns(2)
                with c_name:
                    name = st.text_input("Họ tên", placeholder="Tên của bạn")
                with c_email:
                    email = st.text_input("Email", placeholder="example@email.com")
                type_msg = st.selectbox("Chủ đề", ["Góp ý tính năng", "Báo lỗi", "Hợp tác", "Khác"])
                message = st.text_area("Nội dung", placeholder="Nhập tin nhắn...", height=100)

                if st.form_submit_button("Gửi tin nhắn"):
                    if not name or not message:
                        st.error("Vui lòng nhập Tên và Nội dung!")
                    else:
                        with st.spinner("Đang lưu dữ liệu..."):
                            saved = add_feedback(name, email, type_msg, message)

                        if saved:
                            if "show_member_modal" in st.session_state:
                                st.session_state.show_member_modal = False
                            st.success(f"Cảm ơn {name}! Góp ý đã được lưu.")
                            st.balloons()
                        else:
                            st.error("Chưa thể lưu góp ý. Vui lòng thử lại sau.")




# ==========================================
# 5. MAIN PAGE FUNCTION
# ==========================================

def page_gioi_thieu():
    init_feedback_db()
    inject_custom_css()

    # Reset modal state if we just entered this page from another page
    if st.session_state.get("last_page_visited") != "Giới thiệu":
        st.session_state.show_member_modal = False
        st.session_state.last_page_visited = "Giới thiệu"

    if "show_member_modal" not in st.session_state:
        st.session_state.show_member_modal = False
    if "current_member_idx" not in st.session_state:
        st.session_state.current_member_idx = 0

    # The primary navigation already carries the logo; this page starts with a clear title.
    st.markdown(
        f'<div class="about-header"><span class="overline">VỀ DỰ ÁN</span><h1 class="main-header">{PROJECT_INFO["name"]}</h1>'
        f'<div class="sub-header">{PROJECT_INFO["slogan"]}</div></div>',
        unsafe_allow_html=True,
    )

    # FEATURES
    st.markdown('<div class="section-heading"><div><span class="overline">GIẢI PHÁP</span><h2>Tính năng <span class="title-accent">nổi bật</span></h2><p>Những công cụ hỗ trợ bạn chuẩn bị và tận hưởng chuyến đi.</p></div></div>', unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3, gap="medium")
    features = [
        ("Tối ưu lịch trình", "Bạn chỉ cần chọn điểm đến, AI sẽ tự sắp xếp lộ trình đi lại hợp lý và tiết kiệm nhất."),
        ("Gợi ý phù hợp", "Không biết đi đâu? Hệ thống sẽ chỉ cho bạn những chỗ ăn, chỗ chơi đúng sở thích."),
        ("Bản đồ trực quan", "Nhìn thấy toàn bộ đường đi trên bản đồ để dễ dàng hình dung chuyến đi sắp tới.")
    ]
    for i, (col, (title, desc)) in enumerate(zip([f1, f2, f3], features), start=1):
        with col:
            st.markdown(
                f"""<div class="feature-card">
                        <div class="feature-index">{i:02d} / 03</div>
                        <h4>{title}</h4>
                        <p>{desc}</p>
                    </div>""",
                unsafe_allow_html=True
            )

    st.markdown('<div class="section-heading"><div><span class="overline">NỀN TẢNG</span><h2>Công nghệ</h2></div></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tech-grid">' + ''.join(f'<div class="tech-badge">{tech}</div>' for tech in PROJECT_INFO["tech_stack"]) + '</div>',
        unsafe_allow_html=True,
    )

    # DEMO VIDEO
    st.markdown('<div class="section-heading"><div><span class="overline">TRẢI NGHIỆM</span><h2>Demo Website</h2></div></div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="max-width: 960px; width:100%; margin: 0 auto 2rem auto;">
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; width: 100%; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); border: 1px solid #E2E8F0;">
                <iframe src="https://www.youtube.com/embed/LPOv2afp0iU" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # TEAM LIST
    st.markdown('<div class="section-heading"><div><span class="overline">CON NGƯỜI</span><h2>Đội ngũ phát triển</h2></div></div>', unsafe_allow_html=True)
    row1 = st.columns(3, gap="medium")
    for i in range(3):
        with row1[i]:
            st.markdown(
                create_member_card_html(MEMBERS[i]),
                unsafe_allow_html=True
            )
            if st.button("Xem hồ sơ", key=f"btn_{i}"):
                st.session_state.current_member_idx = i
                st.session_state.show_member_modal = True

    st.write("")
    row2 = st.columns([1, 2, 2, 1], gap="medium")
    for i, idx in enumerate([3, 4]):
        with row2[i + 1]:
            st.markdown(
                create_member_card_html(MEMBERS[idx]),
                unsafe_allow_html=True
            )
            if st.button("Xem hồ sơ", key=f"btn_{idx}"):
                st.session_state.current_member_idx = idx
                st.session_state.show_member_modal = True

    st.divider()

    render_contact_section()
    st.write("")

    if st.session_state.get("show_member_modal", False):
        show_member_modal()

    st.markdown(
        f"<div style='text-align:center; padding:30px; color:#94A3B8; border-top:1px solid #E2E8F0; margin-top:50px'>© 2025 {PROJECT_INFO['name']}. Built by WindyAI.Software.</div>",
        unsafe_allow_html=True
    )
