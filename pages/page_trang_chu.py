"""Trang Trang chủ với Video Background"""
import streamlit as st
import base64
import os
import textwrap

@st.cache_data
def get_base64_media(filename, folder="background"):
    """Đọc file media (video/image) và chuyển sang base64 (có cache)"""
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(current_dir, "assets", folder, filename)
    
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
                # Fix mime type for jpg
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
    # Check file size first
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(current_dir, "assets", folder, filename)
    
    # Clean up indentation in HTML content
    content_html = textwrap.dedent(content_html).strip()
    
    if os.path.exists(file_path):
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb > 10.0:  # Increased limit to 10MB to allow larger video files
            # File too large for base64 inline injection (prevents string overflow/rendering issues)
            st.warning(f"Background '{filename}' is too large ({size_mb:.1f}MB) for inline rendering. Showing placeholder.")
            
            placeholder_html = f"""
            <div class="video-section" style="min-height: {height}; position: relative; overflow: hidden; border-radius: 20px; margin-bottom: 2rem; display: flex; align-items: center; justify-content: center; background-color: #1e293b;">
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(45deg, #1e293b, #0f172a); z-index: 0;"></div>
                <div class="overlay-dark" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,{overlay_opacity}); z-index: 1; pointer-events: none;"></div>
                <div class="content-box" style="position: relative; z-index: 2; width: 100%; padding: 2rem;">
                    {content_html}
                </div>
            </div>
            """
            st.markdown(placeholder_html, unsafe_allow_html=True)
            return

    b64, mime = get_base64_media(filename, folder=folder)
    if not b64 or not mime:
        st.warning(f"Không thể tải resource: {filename}")
        return

    media_html = ""
    # Use explicit tags instead of background-image style to avoid quote parsing issues
    if mime.startswith("video"):
        media_html = f"""<video autoplay muted loop playsinline style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0;"><source src="data:{mime};base64,{b64}" type="{mime}"></video>"""
    else:
        media_html = f"""<img src="data:{mime};base64,{b64}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0;">"""

    # Render the complete section
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

def page_trang_chu():
    """Hiển thị nội dung trang chủ với video/image background."""
    
    # CSS Custom cho trang chủ
    st.markdown("""
    <style>
        /* Ẩn padding mặc định của block-container để video tràn viền đẹp hơn */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 100% !important;
        }
        
        .video-section {
            position: relative;
            width: 100%;
            min-height: 85vh; /* Chiều cao mỗi section */
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            background-color: #1e293b; /* Fallback color */
        }
        
        .video-bg {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: 0;
        }
        
        .overlay-dark {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5); /* Lớp phủ tối để nổi bật chữ */
            z-index: 1;
        }
        
        .content-box {
            position: relative;
            z-index: 2;
            text-align: center;
            color: white;
            padding: 2rem;
            max-width: 900px;
            animation: fadeIn 1.5s ease-in-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .home-title {
            font-size: 3.5rem;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 1.5rem;
            text-shadow: 0 4px 10px rgba(0,0,0,0.5);
            background: linear-gradient(90deg, #60A5FA, #FFFFFF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .home-subtitle {
            font-size: 1.2rem;
            line-height: 1.6;
            margin-bottom: 2rem;
            color: #E2E8F0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }
        
        .feature-box {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 1.5rem;
            border-radius: 16px;
            margin: 10px;
            flex: 1;
            min-width: 200px;
            transition: transform 0.3s ease;
        }
        
        .feature-box:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.2);
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #60A5FA;
            margin-bottom: 0.5rem;
        }
        
        .flex-row {
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            justify-content: center;
            margin-top: 2rem;
        }
        
        .badge-pill {
            display: inline-block;
            padding: 0.5rem 1.5rem;
            background: rgba(37, 99, 235, 0.8);
            color: white;
            border-radius: 99px;
            font-weight: 600;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)

    # --- SECTION 1: HERO (City Night) ---
    render_hero_section("section-1_optimized.jpg", """
        <div class="badge-pill">✨ WindyAI - Smart Travel Planner</div>
        <h1 class="home-title">Lên kế hoạch du lịch<br>thông minh với AI</h1>
        <p class="home-subtitle">
            Chỉ cần nhập điểm đến, ngân sách và thời gian rảnh.<br>
            Hệ thống sẽ giúp bạn tạo lịch trình <b>thông minh – nhanh chóng – tối ưu</b>.
        </p>
    """, overlay_opacity=0.5)

    # --- SECTION 2: HIGHLIGHTS (Global Connection) ---
    render_hero_section("section-2_optimized.jpg", """
        <h2 style="font-size: 2.5rem; margin-bottom: 2rem; font-weight: 700;">Điểm nổi bật</h2>
        <div class="flex-row">
            <div class="feature-box">
                <div style="font-size: 3rem; margin-bottom: 1rem;">⏱️</div>
                <h3>Tối ưu thời gian</h3>
                <p style="font-size: 0.9rem; opacity: 0.9;">Sắp xếp lộ trình khoa học, không lo kẹt xe hay đi đường vòng.</p>
            </div>
            <div class="feature-box">
                <div style="font-size: 3rem; margin-bottom: 1rem;">💸</div>
                <h3>Cân đối chi phí</h3>
                <p style="font-size: 0.9rem; opacity: 0.9;">Gợi ý điểm đến phù hợp với túi tiền của bạn.</p>
            </div>
            <div class="feature-box">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🧭</div>
                <h3>Dễ sử dụng</h3>
                <p style="font-size: 0.9rem; opacity: 0.9;">Giao diện thân thiện, thao tác đơn giản cho mọi lứa tuổi.</p>
            </div>
        </div>
    """, overlay_opacity=0.6)

    # --- SECTION 3: STATS (Coding/Encryption) ---
    render_hero_section("section-3.mp4", """
        <h2 style="font-size: 2.5rem; margin-bottom: 2rem; font-weight: 700;">Hiệu suất vượt trội</h2>
        <div class="flex-row">
            <div class="feature-box">
                <div class="stat-number">~ 2 phút</div>
                <div style="font-weight: 600;">Thời gian chuẩn bị</div>
            </div>
            <div class="feature-box">
                <div class="stat-number">3 – 20</div>
                <div style="font-weight: 600;">Điểm đến / ngày</div>
            </div>
            <div class="feature-box">
                <div class="stat-number">100%</div>
                <div style="font-weight: 600;">Tự động hóa</div>
            </div>
        </div>
    """, overlay_opacity=0.7)

    # --- SECTION 4: FOOTER (Clouds) ---
    render_hero_section("section-4.MP4", """
        <h2 style="font-size: 2.5rem; margin-bottom: 1rem; font-weight: 700;">Trải nghiệm ngay hôm nay</h2>
        <p style="font-size: 1.2rem; margin-bottom: 2rem;">Khám phá thế giới theo cách riêng của bạn.</p>
        <div style="font-size: 0.9rem; opacity: 0.8;">© 2025 WindyAI - Smart Travel Planner</div>
    """, height="60vh", overlay_opacity=0.3)
