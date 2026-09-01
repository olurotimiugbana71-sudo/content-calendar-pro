"""
Content Calendar Pro - Main Application
Copyright 2026 ApexDynamics Solutions | Built by Rotimi Ugbana
"""
import streamlit as st

st.set_page_config(
    page_title="Content Calendar Pro | ApexDynamics Solutions",
    page_icon="📅",
    layout="wide"
)

from hashtag_engine import HashtagEngine
from content_calendar import ContentCalendar
from visualizer import Visualizer
from license_gen import LicenseManager
from datetime import datetime

COMPANY = "ApexDynamics Solutions"
DEVELOPER = "Rotimi Ugbana"
YEAR = "2026"
VERSION = "v1.1"

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .hashtag {
        display: inline-block;
        background: #e8eaf6;
        padding: 4px 10px;
        margin: 3px;
        border-radius: 12px;
        font-size: 12px;
        color: #667EEA;
    }
    .preview-banner {
        background: #fff3cd;
        border: 2px solid #ffc107;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_components():
    return HashtagEngine(), ContentCalendar(), Visualizer(), LicenseManager()

hashtag_engine, calendar, viz, license_mgr = init_components()

if 'licensed' not in st.session_state:
    st.session_state.licensed = False

# Sidebar
with st.sidebar:
    st.markdown(f"## {COMPANY}")
    st.markdown("### 💰 Pricing")
    
    with st.expander("Full Access License - N15,000", expanded=True):
        st.write("✓ Content Calendar")
        st.write("✓ AI Hashtag Engine")
        st.write("✓ Best Posting Times")
        st.write("✓ Analytics Dashboard")
        st.write("✓ 1-Year License")
    
    st.markdown("---")
    st.markdown("### 🔑 License Activation")
    
    lic_key = st.text_input("License Key", placeholder="CAL-XXXX-XXXX-XXXX")
    lic_email = st.text_input("Email", placeholder="you@email.com")
    
    if st.button("Activate License", type="primary"):
        valid, msg = license_mgr.validate(lic_key, lic_email)
        if valid:
            st.success(f"✅ {msg} - Full Access!")
            st.session_state.licensed = True
        else:
            st.error(f"❌ {msg}")
    
    if st.session_state.licensed:
        st.success("🔓 Licensed")
    else:
        st.info("🔒 Preview Mode")

# Main Content
st.markdown(f'<h1 class="main-header">📅 Content Calendar Pro</h1>', unsafe_allow_html=True)
st.markdown(f"### Plan, Create & Schedule Content | {COMPANY}")

if not st.session_state.licensed:
    st.markdown("""
    <div class="preview-banner">
        <h3>🔒 PREVIEW MODE</h3>
        <p>Generate hashtags and preview features. <strong>Activate license</strong> for full access.</p>
        <p style="font-size:14px;">💰 Full Access: N15,000 (1-Year License)</p>
    </div>
    """, unsafe_allow_html=True)

industry = st.selectbox("Industry", ["Technology", "Business", "Health", "Fashion", "Food", "Travel"])

tab1, tab2, tab3 = st.tabs(["📝 Create Post", "📅 Calendar", "📊 Analytics"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        post_date = st.date_input("Date", datetime.now())
        post_time = st.selectbox("Best Time", hashtag_engine.get_best_times(industry))
        platform = st.selectbox("Platform", ["Instagram", "Facebook", "Twitter", "LinkedIn", "TikTok", "YouTube"])
    with c2:
        caption = st.text_area("Caption", height=120)
        if st.button("Generate Ideas"):
            for idea in hashtag_engine.get_ideas(industry):
                st.info(idea)
    
    hashtag_count = st.slider("Hashtags", 5, 30, 15)
    if st.button("Generate Hashtags", type="primary"):
        st.session_state.tags = hashtag_engine.get_hashtags(industry, hashtag_count)
    
    if 'tags' in st.session_state:
        tags_html = " ".join([f'<span class="hashtag">{h}</span>' for h in st.session_state.tags])
        st.markdown(tags_html, unsafe_allow_html=True)
    
    if st.button("Schedule Post", type="primary"):
        post = calendar.add_post({
            "date": post_date.strftime("%Y-%m-%d"), "time": post_time,
            "platform": platform, "caption": caption,
            "hashtags": st.session_state.get('tags', []), "industry": industry
        })
        st.success(f"Post scheduled for {post['date']}!")
        st.balloons()

with tab2:
    st.markdown("### Weekly Calendar")
    week = calendar.get_week(datetime.now())
    st.components.v1.html(viz.calendar_heatmap(week), height=150)
    
    for date, posts in week.items():
        if posts:
            st.markdown(f"**{date}**")
            for p in posts:
                with st.expander(f"{p['time']} - {p['platform']}"):
                    st.write(p['caption'][:100])

with tab3:
    analytics = calendar.get_analytics()
    if analytics:
        st.components.v1.html(viz.summary_cards(analytics), height=100)
        if analytics['by_platform']:
            st.image(f"data:image/png;base64,{viz.platform_chart(analytics['by_platform'])}", width=500)
    else:
        st.info("Create posts to see analytics!")

st.markdown("---")
st.markdown(f"<p style='text-align:center;'>© {YEAR} {COMPANY} | Built by {DEVELOPER} | {VERSION}</p>", unsafe_allow_html=True)