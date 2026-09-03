"""
Content Calendar Pro - Free Preview + Paywall
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
VERSION = "v2.0"
PRICE_NGN = 15000

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        text-align: center;
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
    .paywall-box {
        background: #16213E;
        border: 2px solid #FFD700;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin: 20px 0;
    }
    .paywall-box h3 {
        color: #FFD700;
        margin-bottom: 10px;
    }
    .locked-content {
        filter: blur(5px);
        pointer-events: none;
        user-select: none;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_components():
    return HashtagEngine(), ContentCalendar(), Visualizer(), LicenseManager()

hashtag_engine, calendar, viz, license_mgr = init_components()

if 'licensed' not in st.session_state:
    st.session_state.licensed = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""

# Sidebar
with st.sidebar:
    st.markdown(f"## {COMPANY}")
    st.markdown("### Already Purchased?")
    
    lic_key = st.text_input("License Key", placeholder="CAL-XXXX-XXXX-XXXX")
    lic_email = st.text_input("Email", placeholder="you@email.com")
    
    if st.button("Activate License", type="primary"):
        valid, msg = license_mgr.validate(lic_key, lic_email)
        if valid:
            st.success(f"✅ {msg} - Full Access!")
            st.session_state.licensed = True
            st.session_state.user_email = lic_email
        else:
            st.error(f"❌ {msg}")
    
    if st.session_state.licensed:
        st.success("🔓 Full Access Unlocked")
    else:
        st.info("🔒 Free Preview Mode")

# Main Content
st.markdown(f'<h1 class="main-header">📅 Content Calendar Pro</h1>', unsafe_allow_html=True)
st.markdown(f"### Free Hashtags | Unlock Calendar + Analytics | {COMPANY}")
st.markdown(f"<p style='text-align:center;'>✅ Free Hashtag Generator | 🔒 Calendar + Analytics - ₦{PRICE_NGN:,} One-Time</p>", unsafe_allow_html=True)

industry = st.selectbox("Industry", ["Technology", "Business", "Health", "Fashion", "Food", "Travel"])

tab1, tab2, tab3 = st.tabs(["📝 Create Post", "📅 Calendar", "📊 Analytics"])

with tab1:
    st.markdown("### Create Post (Free Hashtags)")
    
    c1, c2 = st.columns(2)
    with c1:
        post_date = st.date_input("Date", datetime.now())
        post_time = st.selectbox("Best Time", hashtag_engine.get_best_times(industry))
        platform = st.selectbox("Platform", ["Instagram", "Facebook", "Twitter", "LinkedIn", "TikTok", "YouTube"])
    with c2:
        caption = st.text_area("Caption", height=120)
        if st.button("Generate Content Ideas"):
            for idea in hashtag_engine.get_ideas(industry):
                st.info(idea)
    
    # FREE: Hashtag generation
    hashtag_count = st.slider("Hashtags", 5, 30, 15)
    if st.button("Generate Hashtags", type="primary"):
        st.session_state.tags = hashtag_engine.get_hashtags(industry, hashtag_count)
    
    if 'tags' in st.session_state:
        tags_html = " ".join([f'<span class="hashtag">{h}</span>' for h in st.session_state.tags])
        st.markdown(tags_html, unsafe_allow_html=True)
    
    # ============ LOCKED: Schedule Post ============
    st.markdown("---")
    
    if st.session_state.licensed:
        if st.button("Schedule Post", type="primary"):
            post = calendar.add_post({
                "date": post_date.strftime("%Y-%m-%d"), "time": post_time,
                "platform": platform, "caption": caption,
                "hashtags": st.session_state.get('tags', []), "industry": industry
            })
            st.success(f"Post scheduled for {post['date']}!")
            st.balloons()
    else:
        st.markdown(f"""
        <div class="paywall-box">
            <h3>🔒 Unlock Post Scheduling + Calendar</h3>
            <p style="color:#B0B0B0;margin-bottom:15px;">
                Schedule posts, access your weekly calendar, 
                and view analytics.
            </p>
            <p style="color:#FFD700;font-size:24px;font-weight:700;margin:15px 0;">
                ₦{PRICE_NGN:,} One-Time
            </p>
            <p style="color:#B0B0B0;font-size:14px;margin-bottom:15px;">
                ✅ Post Scheduling<br>
                ✅ Weekly Calendar View<br>
                ✅ Analytics Dashboard<br>
                ✅ Unlimited Hashtags<br>
                ✅ 1-Year License
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📧 Where should we send your license?")
        user_email = st.text_input("Your Email Address", placeholder="you@email.com")
        
        if st.button("🔓 Unlock Full Access - ₦15,000", type="primary", use_container_width=True):
            if user_email and '@' in user_email:
                st.session_state.user_email = user_email
                st.success(f"✅ Check your email at {user_email}!")
                
                st.markdown(f"""
                ### Complete Your Payment:
                
                [🔗 Click here to pay ₦15,000 via Paystack](https://paystack.com/buy/content-calendar-pro---full-access-license-infpne)
                
                After payment, your license key will be sent to: **{user_email}**
                
                *Having trouble? WhatsApp: +234 806 520 9323*
                """)
            else:
                st.error("Please enter a valid email address")

with tab2:
    st.markdown("### 📅 Weekly Calendar")
    
    if st.session_state.licensed:
        week = calendar.get_week(datetime.now())
        st.components.v1.html(viz.calendar_heatmap(week), height=150)
        
        for date, posts in week.items():
            if posts:
                st.markdown(f"**{date}**")
                for p in posts:
                    with st.expander(f"{p['time']} - {p['platform']}"):
                        st.write(p['caption'][:100])
    else:
        st.markdown("""<div class="locked-content">""", unsafe_allow_html=True)
        st.markdown("Monday - 0 posts")
        st.markdown("Tuesday - 0 posts")
        st.markdown("Wednesday - 0 posts")
        st.markdown("""</div>""", unsafe_allow_html=True)
        st.info("🔒 Unlock to access your weekly calendar")

with tab3:
    st.markdown("### 📊 Analytics")
    
    if st.session_state.licensed:
        analytics = calendar.get_analytics()
        if analytics:
            st.components.v1.html(viz.summary_cards(analytics), height=100)
            if analytics['by_platform']:
                st.image(f"data:image/png;base64,{viz.platform_chart(analytics['by_platform'])}", width=500)
        else:
            st.info("Create posts to see analytics!")
    else:
        st.markdown("""<div class="locked-content">""", unsafe_allow_html=True)
        st.markdown("Total Posts: 0")
        st.markdown("Platform Breakdown: Locked")
        st.markdown("Engagement Metrics: Locked")
        st.markdown("""</div>""", unsafe_allow_html=True)
        st.info("🔒 Unlock to access analytics dashboard")

st.markdown("---")
st.markdown(f"<p style='text-align:center;'>© {YEAR} {COMPANY} | Built by {DEVELOPER} | {VERSION}</p>", unsafe_allow_html=True)