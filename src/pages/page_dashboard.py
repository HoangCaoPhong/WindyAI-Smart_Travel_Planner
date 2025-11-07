import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from components.ui_components import render_section_header, render_stat_card

def render_dashboard(username):
    """Render dashboard page."""
    # Welcome Header
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1E88E5 0%, #26A69A 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        ">
            <h1 style="color: white; margin: 0;">👋 Chào mừng trở lại, {username}!</h1>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Sẵn sàng khám phá những điểm đến mới hôm nay?</p>
        </div>
    """, unsafe_allow_html=True)

    # Stats Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_stat_card("Địa điểm đã lưu", "24", "📍")
    with col2:
        render_stat_card("Lượt tìm kiếm", "156", "🔍", "+12")
    with col3:
        render_stat_card("Bộ sưu tập", "5", "💾")
    with col4:
        render_stat_card("Ảnh nhận diện", "38", "📸", "+5")

    st.markdown("<br>", unsafe_allow_html=True)

    # Bố cục st.columns([2, 1]) (cột trái 60%, cột phải 40%).
    col_left, col_right = st.columns([2, 1])

    with col_left:
        render_section_header("Lịch sử tìm kiếm", "Các tìm kiếm gần đây của bạn", "🕐")
        
        st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                <div style="margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #E0E0E0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="color: #212121;">Nhà hàng Sài Gòn</strong>
                            <p style="color: #757575; font-size: 0.875rem; margin: 0.25rem 0 0 0;">Hôm qua, 14:30</p>
                        </div>
                        <span style="background: #E3F2FD; color: #1565C0; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.875rem;">Nhà hàng</span>
                    </div>
                </div>
                <div style="margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #E0E0E0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="color: #212121;">Khách sạn 5 sao Đà Nẵng</strong>
                            <p style="color: #757575; font-size: 0.875rem; margin: 0.25rem 0 0 0;">2 ngày trước, 09:15</p>
                        </div>
                        <span style="background: #FFF3E0; color: #EF6C00; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.875rem;">Khách sạn</span>
                    </div>
                </div>
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="color: #212121;">Bảo tàng Hà Nội</strong>
                            <p style="color: #757575; font-size: 0.875rem; margin: 0.25rem 0 0 0;">3 ngày trước, 16:45</p>
                        </div>
                        <span style="background: #E8F5E9; color: #2E7D32; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.875rem;">Tham quan</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        render_section_header("Bộ sưu tập của bạn", "Quản lý các bộ sưu tập địa điểm", "📚")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border-left: 4px solid #1E88E5;">
                    <h4 style="color: #1E88E5; margin: 0 0 0.5rem 0;">🏖️ Kỳ nghỉ hè 2025</h4>
                    <p style="color: #757575; font-size: 0.875rem; margin: 0;">12 địa điểm</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border-left: 4px solid #26A69A;">
                    <h4 style="color: #26A69A; margin: 0 0 0.5rem 0;">🍜 Ẩm thực Việt</h4>
                    <p style="color: #757575; font-size: 0.875rem; margin: 0;">8 địa điểm</p>
                </div>
            """, unsafe_allow_html=True)

    with col_right:
        render_section_header("Gợi ý cho bạn", "Dựa trên sở thích", "✨")

        # 📍 Vị trí chờ API (Đề xuất):
        def get_ai_recommendations(user_id):
            # ---- TODO: Kết nối API thuật toán đề xuất ----
            # response = requests.get(f"api/recommend?user={user_id}")
            # return response.json()['recommendations']

            # ---- Dữ liệu giả lập (Mock data) cho UI ----
            return [
                {'name': 'Quán Phở Demo', 'img': 'url1', 'desc': 'Gợi ý vì bạn thích phở', 'rating': '4.5⭐'},
                {'name': 'Cafe Yên Tĩnh', 'img': 'url2', 'desc': 'Gợi ý vì bạn tìm "yên tĩnh"', 'rating': '4.8⭐'},
                {'name': 'Bảo tàng Nghệ thuật', 'img': 'url3', 'desc': 'Phù hợp với sở thích văn hóa', 'rating': '4.7⭐'}
            ]

        user_id = st.session_state.get('user_id')
        recommendations = get_ai_recommendations(user_id)
        
        for item in recommendations:
            st.markdown(f"""
                <div style="
                    background: white;
                    padding: 1.5rem;
                    border-radius: 12px;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                    margin-bottom: 1rem;
                    transition: all 0.3s ease;
                    border: 1px solid #E0E0E0;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                        <h4 style="color: #212121; margin: 0;">{item['name']}</h4>
                        <span style="color: #FF9800; font-size: 0.875rem;">{item['rating']}</span>
                    </div>
                    <p style="color: #757575; font-size: 0.875rem; margin: 0;">{item['desc']}</p>
                </div>
            """, unsafe_allow_html=True)

