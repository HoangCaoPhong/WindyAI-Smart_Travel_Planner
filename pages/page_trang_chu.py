import streamlit as st
import base64
import os
import html as _html
import textwrap
try:
    from core.algo6_chatbot.chatbot_engine import ChatbotEngine
except ImportError:
    ChatbotEngine = None


# ==============================================================================
# 1. CẤU HÌNH CSS (CHAT BUTTON + GIAO DIỆN CHUNG)
# ==============================================================================
def inject_custom_css(logo_b64=None, chat_open=False):
    # Xác định style cho nút dựa trên trạng thái (Mở/Đóng) và có logo hay không
    if logo_b64 and not chat_open:
        # Trạng thái ĐÓNG: Hiển thị Logo WindyAI, nền trắng, ẩn text emoji
        btn_background = f"url('data:image/png;base64,{logo_b64}') center/70% no-repeat white"
        btn_color = "transparent" # Ẩn emoji "💬"
        btn_border = "1px solid #e0e0e0" # Viền nhẹ cho nút trắng
        hover_transform = "scale(1.1)"
    else:
        # Trạng thái MỞ (hoặc không có logo): Hiển thị nút Xanh/Đỏ mặc định
        btn_background = "#0084ff"
        btn_color = "white"
        btn_border = "none"
        hover_transform = "scale(1.1) rotate(90deg)" if chat_open else "scale(1.1)"

    st.markdown(f"""
    <style>
        /* ---------------------------------------------------------------------- */
        /* 1. ĐỊNH VỊ NÚT CHAT TRÒN (FIXED POSITION) */
        /* ---------------------------------------------------------------------- */
        div.element-container:has(#chat-btn-marker) + div.element-container button {{
            position: fixed !important;
            bottom: 70px !important;
            right: 20px !important;
            width: 60px !important;
            height: 60px !important;
            border-radius: 50% !important;
            background: {btn_background} !important;
            color: {btn_color} !important;
            border: {btn_border} !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
            font-size: 24px !important;
            z-index: 999999 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        }}
        div.element-container:has(#chat-btn-marker) + div.element-container button:hover {{
            transform: {hover_transform} !important;
            box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
        }}

        /* ---------------------------------------------------------------------- */
        /* 2. KHUNG CHAT WINDOW */
        /* ---------------------------------------------------------------------- */
        div.floating-chat-window {{
            position: fixed;
            bottom: 140px;
            right: 20px;
            width: 350px;
            height: min(440px, calc(100vh - 270px));
            background: #ffffff;
            border-radius: 20px;
            box-shadow: 0 5px 30px rgba(0,0,0,0.2);
            z-index: 999998;
            display: flex; flex-direction: column;
            overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        @keyframes slideIn {{ from {{ opacity: 0; transform: translateY(20px) scale(0.95); }} to {{ opacity: 1; transform: translateY(0) scale(1); }} }}

        .chat-header {{
            padding: 15px; background: #fff; border-bottom: 1px solid #f0f0f0;
            display: flex; align-items: center; justify-content: space-between;
        }}
        .chat-header .title {{ font-weight: bold; color: #0084ff; font-size: 1.1rem; }}
        .chat-header .status {{ font-size: 0.8rem; color: #31a24c; }}

        .chat-body-scroll {{
            flex: 1; overflow-y: auto; padding: 15px; background: #fff;
            display: flex; flex-direction: column;
            margin-bottom: 70px;
        }}
        .chat-body-scroll::-webkit-scrollbar {{ width: 5px; }}
        .chat-body-scroll::-webkit-scrollbar-thumb {{ background: #ccc; border-radius: 10px; }}

        .msg-row {{ display: flex; margin-bottom: 10px; width: 100%; }}
        .msg-row.user {{ justify-content: flex-end; }}
        .msg-row.assistant {{ justify-content: flex-start; }}
        
        .msg-bubble {{
            max-width: 80%; padding: 10px 14px; border-radius: 18px;
            font-size: 14px; line-height: 1.4; position: relative;
        }}
        .msg-bubble.user {{ background: #0084ff; color: white; border-bottom-right-radius: 4px; }}
        .msg-bubble.assistant {{ background: #f0f0f0; color: #333; border-bottom-left-radius: 4px; }}

        .chat-footer-bg {{
            position: absolute; bottom: 0; left: 0; width: 100%; height: 75px;
            background: #fff; border-top: 1px solid #f0f0f0; z-index: 1;
        }}

        /* ---------------------------------------------------------------------- */
        /* 3. INPUT HACK */
        /* ---------------------------------------------------------------------- */
        div.element-container:has(#chat-input-marker) + div.element-container div[data-testid="stTextInput"] {{
            position: fixed !important;
            bottom: 155px !important;
            right: 35px !important;
            width: 320px !important;
            z-index: 999999 !important;
        }}
        div[data-testid="stTextInput"] input {{
            border-radius: 25px !important;
            background: #f0f2f5 !important;
            border: none !important;
            padding: 10px 20px !important;
        }}
        div[data-testid="stTextInput"] input:focus {{
            background: #fff !important;
            box-shadow: 0 0 0 2px #0084ff !important;
        }}
        div[data-testid="stTextInput"] label {{ display: none !important; }}

        /* Ẩn header footer mặc định của Streamlit */
        header {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. HÀM XỬ LÝ MEDIA (UPDATED)
# ==============================================================================
@st.cache_data
def get_base64_media(filename, folder="background"):
    """Đọc file media (video/image) và chuyển sang base64 (có cache)"""
    # Tìm đường dẫn file linh hoạt (chạy ở root hoặc trong pages)
    try: current_dir = os.path.dirname(os.path.abspath(__file__))
    except: current_dir = os.getcwd()
    
    # Thử tìm trực tiếp trong folder assets
    file_path = os.path.join(current_dir, "assets", folder, filename)
    
    # Nếu không thấy, thử lùi ra 1 cấp (trường hợp chạy trong thư mục con)
    if not os.path.exists(file_path):
        file_path = os.path.join(os.path.dirname(current_dir), "assets", folder, filename)

    if not os.path.exists(file_path):
        return None, None
        
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            # Ensure no newlines or carriage returns in base64 string
            b64 = base64.b64encode(data).decode("utf-8").replace("\n", "").replace("\r", "")
            
            ext = filename.split('.')[-1].lower()
            if ext in ['mp4', 'mov']:
                return b64, 'video/mp4'
            elif ext in ['png', 'jpg', 'jpeg']:
                mime_type = 'image/jpeg' if ext in ['jpg', 'jpeg'] else f'image/{ext}'
                return b64, mime_type
            elif ext == 'gif':
                return b64, 'image/gif'
            else:
                return None, None
    except Exception as e:
        st.error(f"Lỗi khi đọc file {filename}: {e}")
        return None, None

def render_hero_section(filename, content_html, height="85vh", overlay_opacity=0.5, folder="background"):
    content_html = textwrap.dedent(content_html).strip()
    b64, mime = get_base64_media(filename, folder=folder)
    
    media_html = ""
    if not b64:
        media_html = '<div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(45deg, #1e293b, #0f172a); z-index: 0;"></div>'
    else:
        if mime.startswith("video"):
            media_html = f"""<video autoplay muted loop playsinline style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0;"><source src="data:{mime};base64,{b64}" type="{mime}"></video>"""
        else:
            media_html = f"""<img src="data:{mime};base64,{b64}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0;">"""

    full_html = f"""
    <div class="video-section" style="min-height: {height}; position: relative; overflow: hidden; border-radius: 20px; margin-bottom: 2rem; display: flex; align-items: center; justify-content: center; background-color: #1e293b;">
        {media_html}
        <div class="overlay-dark" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,{overlay_opacity}); z-index: 1; pointer-events: none;"></div>
        <div class="content-box" style="position: relative; z-index: 2; width: 100%; padding: 2rem;">
            {content_html}
        </div>
    </div>
    """
    st.markdown(full_html, unsafe_allow_html=True)

# ==============================================================================
# 3. LOGIC CHATBOT (GIỮ NGUYÊN)
# ==============================================================================
def render_floating_chat():
    # 1. Init State (Đã được xử lý ở đầu trang_chu nhưng giữ lại để an toàn)
    if 'show_chat' not in st.session_state: st.session_state.show_chat = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Chào bạn! WindyAI đây. 👋\nMình có thể giúp gì cho chuyến đi của bạn?"}
        ]

    # Init Chatbot Engine
    if 'chatbot_engine' not in st.session_state and ChatbotEngine:
        st.session_state.chatbot_engine = ChatbotEngine()
        
    if 'waiting_for_bot' not in st.session_state:
        st.session_state.waiting_for_bot = False

    # 2. MARKER CHO NÚT CHAT
    st.markdown('<span id="chat-btn-marker"></span>', unsafe_allow_html=True)
    
    # Render Nút - Text sẽ được ẩn bởi CSS nếu ở trạng thái đóng và có logo
    if st.button("💬" if not st.session_state.show_chat else "✕", key="btn_chat"):
        st.session_state.show_chat = not st.session_state.show_chat
        st.rerun()

    # 3. Render Khung Chat
    if st.session_state.show_chat:
        messages_html = ""
        for msg in st.session_state.chat_history:
            role = "assistant" if msg["role"] == "assistant" else "user"
            content = _html.escape(msg["content"]).replace("\n", "<br>")
            messages_html += f'<div class="msg-row {role}"><div class="msg-bubble {role}">{content}</div></div>'
            
        # Nếu đang chờ bot trả lời, thêm bubble "đang soạn tin..."
        if st.session_state.waiting_for_bot:
            messages_html += """<div class="msg-row assistant"><div class="msg-bubble assistant"><div class="typing-indicator"><span></span><span></span><span></span></div></div></div>"""

        full_chat_html = textwrap.dedent(f"""
            <div class="floating-chat-window">
                <div class="chat-header">
                    <span class="title">WindyAI Assistant</span>
                    <span class="status">● Online</span>
                </div>
                <div class="chat-body-scroll">
                    {messages_html}
                </div>
                <div class="chat-footer-bg"></div>
            </div>
            <style>
            .typing-indicator {{
                display: flex;
                align-items: center;
                justify-content: center;
                height: 20px;
            }}
            .typing-indicator span {{
                display: block;
                width: 6px;
                height: 6px;
                background-color: #555;
                border-radius: 50%;
                margin: 0 2px;
                animation: typing 1.4s infinite ease-in-out both;
            }}
            .typing-indicator span:nth-child(1) {{ animation-delay: -0.32s; }}
            .typing-indicator span:nth-child(2) {{ animation-delay: -0.16s; }}
            @keyframes typing {{
                0%, 80%, 100% {{ transform: scale(0); }}
                40% {{ transform: scale(1); }}
            }}
            </style>
        """)
        st.markdown(full_chat_html, unsafe_allow_html=True)

        st.markdown('<span id="chat-input-marker"></span>', unsafe_allow_html=True)
        
        def submit_chat():
            user_input = st.session_state.temp_input
            if user_input:
                # Thêm tin nhắn user vào history ngay lập tức
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                st.session_state.temp_input = "" # Clear input ngay
                st.session_state.waiting_for_bot = True # Đánh dấu đang chờ bot

        st.text_input("input_placeholder", key="temp_input", on_change=submit_chat, placeholder="Hỏi về lịch trình...", label_visibility="collapsed")
        
        # Xử lý logic bot trả lời SAU khi đã render UI (để user thấy tin nhắn của mình trước)
        if st.session_state.waiting_for_bot:
            # Lấy tin nhắn cuối cùng của user
            last_user_msg = st.session_state.chat_history[-1]["content"]
            
            reply = ""
            if 'chatbot_engine' in st.session_state and st.session_state.chatbot_engine:
                reply = st.session_state.chatbot_engine.process_message(last_user_msg)
            else:
                # Fallback logic cũ
                txt_lower = last_user_msg.lower()
                if "lịch trình" in txt_lower or "kế hoạch" in txt_lower:
                    reply = "Để tạo lịch trình, bạn vui lòng truy cập tab 'Chức năng' ở trên, sau đó chọn mục '📅 Tạo lịch trình gợi ý' để bắt đầu nhé!"
                elif "đường" in txt_lower or "chỉ đường" in txt_lower:
                    reply = "Bạn muốn tìm đường đi? Hãy vào tab 'Chức năng' và nhấn vào nút '🚗 Tìm đường đi' nha."
                elif "thời tiết" in txt_lower:
                    reply = "Để xem thời tiết, bạn có thể vào tab 'Chức năng' và chọn '🌤️ Báo thời tiết vị trí', hoặc hỏi mình trực tiếp như 'Thời tiết ở Quận 1' nhé!"
                elif "gợi ý địa điểm" in txt_lower or "địa điểm" in txt_lower:
                    reply = "Mình có thể giúp bạn gợi ý địa điểm dựa trên sở thích của bạn. Hãy vào tab 'Chức năng' và chọn '📍 Gợi ý địa điểm' để trải nghiệm nhé!"
                elif "ảnh" in txt_lower or "hình" in txt_lower:
                    reply = "Bạn muốn tìm vị trí ảnh? Vui lòng vào tab 'Chức năng' và chọn '📸 Tìm vị trí ảnh' để sử dụng tính năng này."
                elif "các chức năng" in txt_lower or "tính năng" in txt_lower or "help" in txt_lower:
                    reply = "WindyAI có các tính năng chính: Lịch trình, Tìm đường, Thời tiết, Gợi ý địa điểm, Tìm vị trí ảnh. Vào tab 'Chức năng' để trải nghiệm nhé!"
                elif "xin chào" in txt_lower or "chào" in txt_lower:
                    reply = "Chào bạn! Mình là WindyAI, trợ lý du lịch thông minh của bạn. Mình có thể giúp gì cho chuyến đi của bạn?"
                else:
                    reply = "Chào bạn! WindyAI có các tính năng: Lịch trình, Tìm đường, Thời tiết... Bạn hãy vào tab 'Chức năng' để trải nghiệm đầy đủ nhé."

            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.session_state.waiting_for_bot = False
            st.rerun()

# ==============================================================================
# 4. MAIN APP (CẬP NHẬT GIAO DIỆN MỚI)
# ==============================================================================
def _open_feature(feature):
    st.session_state["selected_function"] = feature
    st.session_state["current_page"] = "Chức năng"
    st.rerun()


def page_trang_chu():
    # Landing page with real Streamlit actions for every existing feature.
    if "show_chat" not in st.session_state:
        st.session_state.show_chat = False
    logo_b64, _ = get_base64_media("logo.png", folder="logo")
    inject_custom_css(logo_b64, st.session_state.show_chat)

    image_b64, mime = get_base64_media("section-1_optimized.jpg")
    image_style = f"background-image: linear-gradient(90deg, rgba(3,30,68,.91) 0%, rgba(3,42,82,.73) 52%, rgba(8,51,91,.10) 100%), url('data:{mime};base64,{image_b64}');" if image_b64 else ""
    st.markdown(f'''<section class="landing-hero" style="{image_style}">
      <div class="hero-inner">
        <span class="eyebrow">KHÁM PHÁ VIỆT NAM THEO CÁCH CỦA BẠN</span>
        <h1>Mỗi chuyến đi,<br><em>một trải nghiệm đáng nhớ.</em></h1>
        <p>WindyAI giúp bạn lên lịch trình, khám phá địa điểm và tìm đường đi phù hợp với thời gian, sở thích và ngân sách của mình.</p>
        <div class="hero-proof"><span>Lịch trình cá nhân hóa</span><span>Khám phá thông minh</span><span>Dễ dàng bắt đầu</span></div>
      </div>
    </section>''', unsafe_allow_html=True)
    cta, more, spacer = st.columns([1.45, 1.3, 4.2], gap="small")
    with cta:
        if st.button("Tạo lịch trình ngay", type="primary", use_container_width=True, key="home_plan"):
            _open_feature("Tạo lịch trình gợi ý")
    with more:
        if st.button("Khám phá tính năng  →", use_container_width=True, key="home_features"):
            st.session_state["current_page"] = "Chức năng"
            st.rerun()

    st.markdown('''<div class="section-heading"><div><span class="overline">CÔNG CỤ CHO CHUYẾN ĐI</span><h2>Bạn muốn <span class="title-accent">khám phá</span> điều gì?</h2><p>Chọn một công cụ và bắt đầu lên kế hoạch theo cách của bạn.</p></div></div>''', unsafe_allow_html=True)
    features = [
        ("Tạo lịch trình", "Lên kế hoạch theo thời gian, sở thích và ngân sách.", "Tạo lịch trình gợi ý", "Lên kế hoạch"),
        ("Tìm đường đi", "Xem lộ trình giữa các điểm đến của bạn.", "Tìm đường đi", "Xem đường đi"),
        ("Tìm vị trí ảnh", "Nhận diện địa điểm từ hình ảnh của bạn.", "Tìm vị trí ảnh", "Thử nhận diện"),
        ("Xem thời tiết", "Kiểm tra thời tiết trước khi khởi hành.", "Báo thời tiết vị trí", "Xem dự báo"),
        ("Gợi ý địa điểm", "Tìm những điểm dừng chân hợp sở thích.", "Gợi ý địa điểm", "Khám phá ngay"),
    ]
    cols = st.columns(5, gap="medium")
    for i, (title, desc, feature, action) in enumerate(features):
        with cols[i]:
            st.markdown(f'<div class="tool-card"><div class="tool-index">{i + 1:02d} / 05</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
            if st.button(f"{action}  →", key=f"home_tool_{i}", use_container_width=True):
                _open_feature(feature)

    st.markdown('''<div class="how-intro"><span class="overline">BẮT ĐẦU THẬT ĐƠN GIẢN</span><h2>Ba bước cho <span class="title-accent">hành trình</span> của bạn</h2></div>
    <div class="steps-grid">
      <div><span>01</span><h3>Chọn điều bạn cần</h3><p>Lịch trình, đường đi, thời tiết hay một địa điểm mới.</p></div>
      <div><span>02</span><h3>Thêm thông tin</h3><p>Cho WindyAI biết thời gian, ngân sách và sở thích của bạn.</p></div>
      <div><span>03</span><h3>Sẵn sàng khám phá</h3><p>Xem gợi ý và lưu lịch trình trong tài khoản.</p></div>
    </div>
    <div class="landing-footer"><strong>WindyAI</strong><span>Lên kế hoạch dễ hơn. Tận hưởng hành trình nhiều hơn.</span></div>''', unsafe_allow_html=True)
    render_floating_chat()


if __name__ == "__main__":
    page_trang_chu()
