"""Trang Trang chủ"""
import streamlit as st


def page_trang_chu():
    """Hiển thị nội dung trang chủ."""
    col_text, col_image = st.columns([1.05, 1], gap="large")
    with col_text:
        st.markdown(
            "<div class='badge-pill'>✨ WindyAI - Smart Travel Website</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <h1 class='home-title'
                style='font-size: 3.4rem; font-weight: 750; line-height: 1.15; margin-bottom: 1.2rem; margin-top: 1.2rem;'>
                Lên kế hoạch du lịch<br>thông minh với AI
            </h1>
            """,
            unsafe_allow_html=True,
        )
        st.write(
            "Chỉ cần nhập điểm đến, ngân sách và thời gian rảnh, hệ thống sẽ giúp bạn tạo lịch trình "
            "du lịch **thông minh – nhanh chóng – tối ưu** cho một ngày."
        )

        st.markdown("#### Điểm nổi bật")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.caption("⏱️ Tối ưu thời gian")
        with c2:
            st.caption("💸 Cân đối chi phí")
        with c3:
            st.caption("🧭 Dễ dùng cho mọi người")

        st.markdown("")
        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown(
                """
                <div class='home-stat-card'>
                    <div class='home-stat-label'>Thời gian chuẩn bị</div>
                    <div class='home-stat-value'>~ 2 phút</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with s2:
            st.markdown(
                """
                <div class='home-stat-card'>
                    <div class='home-stat-label'>Số điểm đến trong ngày</div>
                    <div class='home-stat-value'>3 – 6 điểm</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with s3:
            st.markdown(
                """
                <div class='home-stat-card'>
                    <div class='home-stat-label'>Trải nghiệm</div>
                    <div class='home-stat-value'>Thoải mái</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_image:
        st.image(
            "https://images.unsplash.com/photo-1500835556837-99ac94a94552?w=900&auto=format&fit=crop&q=60",
            use_container_width=True,
            output_format="PNG",
        )
