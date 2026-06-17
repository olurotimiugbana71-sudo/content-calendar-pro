import streamlit as st
st.set_page_config(page_title="Content Calendar Pro | ApexDynamics", page_icon="📅", layout="wide")

from hashtag_engine import HashtagEngine
from content_calendar import ContentCalendar
from visualizer import Visualizer
from license_gen import LicenseManager
from datetime import datetime

COMPANY = "ApexDynamics Solutions"
DEVELOPER = "Rotimi Ugbana"

@st.cache_resource
def init():
    return HashtagEngine(), ContentCalendar(), Visualizer(), LicenseManager()

hashtag_engine, calendar, viz, license_mgr = init()

if 'licensed' not in st.session_state:
    st.session_state.licensed = False

# Sidebar
st.sidebar.markdown(f"## {COMPANY}")
st.sidebar.markdown("### Plans")
st.sidebar.write("Basic: $19/mo | Standard: $29/mo | Premium: $39/mo")
st.sidebar.markdown("---")
lic_key = st.sidebar.text_input("License Key", placeholder="CAL-XXXX-XXXX-XXXX")
lic_email = st.sidebar.text_input("Email")
if st.sidebar.button("Activate"):
    valid, msg = license_mgr.validate(lic_key, lic_email)
    if valid:
        st.sidebar.success(msg)
        st.session_state.licensed = True
    else:
        st.sidebar.error(msg)

# Main
st.markdown(f"<h1 style='background:linear-gradient(135deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:2.5rem;'>📅 Content Calendar Pro</h1>", unsafe_allow_html=True)
st.markdown(f"### Plan, Create & Schedule Content | {COMPANY}")

industry = st.selectbox("Industry", ["Technology","Business","Health","Fashion","Food","Travel"])

tab1, tab2, tab3 = st.tabs(["📝 Create Post", "📅 Calendar", "📊 Analytics"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        post_date = st.date_input("Date", datetime.now())
        post_time = st.selectbox("Best Time", hashtag_engine.get_best_times(industry))
        platform = st.selectbox("Platform", ["Instagram","Facebook","Twitter","LinkedIn","TikTok","YouTube"])
    with c2:
        caption = st.text_area("Caption", height=120)
        if st.button("💡 Generate Ideas"):
            for idea in hashtag_engine.get_ideas(industry):
                st.info(idea)
    
    hashtag_count = st.slider("Hashtags", 5, 30, 15)
    if st.button("🎯 Generate Hashtags", type="primary"):
        st.session_state.tags = hashtag_engine.get_hashtags(industry, hashtag_count)
    
    if 'tags' in st.session_state:
        tags_html = " ".join([f'<span style="background:#e8eaf6;padding:4px 10px;margin:3px;border-radius:12px;display:inline-block;font-size:12px;">{h}</span>' for h in st.session_state.tags])
        st.markdown(tags_html, unsafe_allow_html=True)
    
    if st.button("📅 Schedule Post", type="primary"):
        post = calendar.add_post({
            "date": post_date.strftime("%Y-%m-%d"), "time": post_time,
            "platform": platform, "caption": caption,
            "hashtags": st.session_state.get('tags', []), "industry": industry
        })
        st.success(f"✅ Post scheduled for {post['date']}!")
        st.balloons()

with tab2:
    st.markdown("### Weekly Calendar")
    week = calendar.get_week(datetime.now())
    st.components.v1.html(viz.calendar_heatmap(week), height=150)
    
    for date, posts in week.items():
        if posts:
            st.markdown(f"**{date}**")
            for p in posts:
                with st.expander(f"{p['time']} - {p['platform']} ({p['content_type']})"):
                    st.write(p['caption'][:100])

with tab3:
    analytics = calendar.get_analytics()
    if analytics:
        st.components.v1.html(viz.summary_cards(analytics), height=100)
        if analytics['by_platform']:
            st.image(f"data:image/png;base64,{viz.platform_chart(analytics['by_platform'])}")
        upcoming = calendar.get_upcoming(5)
        if upcoming:
            st.markdown("### Upcoming Posts")
            for p in upcoming:
                st.markdown(f"📅 {p['date']} | {p['time']} | {p['platform']}")
    else:
        st.info("Create posts to see analytics!")

st.markdown("---")
st.caption(f"© 2026 {COMPANY} | Built by {DEVELOPER}")