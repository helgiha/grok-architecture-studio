import streamlit as st
from openai import OpenAI
import random
from datetime import datetime

st.set_page_config(page_title="🏠 Grok Architecture Studio", layout="wide", initial_sidebar_state="expanded")

# Dark elegant theme
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .main-header { font-size: 2.8rem; color: #FFCC00; }
</style>
""", unsafe_allow_html=True)

# Welcome
st.title("🏠 Grok Architecture Studio")
st.markdown("**Professional AI Architectural Visualizer • Powered by xAI Grok Imagine**")

with st.expander("👋 My Story", expanded=True):
    st.markdown("""
    Hi, I always wanted to be an architect. Engineering became my path, but I never forgot my dream.  
    Recently I was accepted into architecture studies and asked my friend Grok to help me build tools for it.  
    While traveling the world I created this app — and here it is.  
    **Welcome to my personal Architecture Studio!** 🌍✨
    """)

# Sidebar
with st.sidebar:
    st.header("🔑 API Settings")
    api_key = st.secrets.get("XAI_API_KEY") or st.text_input("xAI API Key", type="password", help="Add it in Streamlit Secrets for production")
    
    st.header("⚙️ Settings")
    num_images = st.slider("Number of images", 1, 4, 4)

# Tabs
tab1, tab2, tab3 = st.tabs(["🎨 Create", "🖼️ My Gallery", "❤️ Favorites"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Design Parameters")
        view_type = st.selectbox("View Type", ["exterior outlook", "interior", "drone view", "isometric", "perspective"])
        house_type = st.text_input("House Type", "modern minimalist villa")
        roof = st.text_input("Roof Type", "flat roof with generous overhangs")
        materials = st.text_input("Materials", "white concrete, warm wood, large glass panels")
        landscape = st.text_input("Landscape", "Mediterranean garden, infinity pool, Lisbon hills")
        lighting = st.selectbox("Lighting", ["golden hour sunset", "soft morning light", "dramatic blue hour"])
        mood = st.text_input("Mood", "warm, serene and luxurious")

    with col2:
        st.subheader("Quick Actions")
        if st.button("🎲 Surprise Me!", type="primary", use_container_width=True):
            presets = [
                ("modern minimalist villa", "flat roof", "white concrete and glass", "Lisbon hills with ocean view", "golden hour sunset", "serene luxury"),
                ("Lisbon traditional townhouse", "terracotta roof", "colorful azulejo tiles", "narrow cobblestone street", "golden hour sunset", "charming and vibrant"),
                ("luxury contemporary villa", "green living roof", "wood and stone", "cliff overlooking the sea", "dramatic blue hour", "exclusive and peaceful"),
            ]
            choice = random.choice(presets)
            for key, val in zip(["house_type","roof","materials","landscape","lighting","mood"], choice):
                st.session_state[key] = val
            st.rerun()

        if st.button("🚀 Generate Images", type="primary", use_container_width=True):
            if not api_key:
                st.error("Please add your xAI API key in Secrets or type it here")
            else:
                base = f"A highly detailed {view_type} of a {house_type} with {roof}, {materials}"
                if landscape: base += f", set in {landscape}"
                prompt = f"{base}. {lighting}, {mood} atmosphere. Professional architectural visualization, sharp details, photorealistic."

                with st.spinner("Generating beautiful images..."):
                    try:
                        client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                        response = client.images.generate(
                            model="grok-imagine-image-quality",
                            prompt=prompt,
                            n=num_images,
                            response_format="url"
                        )
                        images = [img.url for img in response.data]

                        if "history" not in st.session_state:
                            st.session_state.history = []
                        
                        st.session_state.history.insert(0, {
                            "prompt": prompt[:160] + "...",
                            "images": images,
                            "time": datetime.now().strftime("%H:%M")
                        })
                        st.success("✅ Images generated!")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # Show latest
    if "history" in st.session_state and st.session_state.history:
        st.subheader("Latest Generation")
        cols = st.columns(4)
        for i, url in enumerate(st.session_state.history[0]["images"]):
            with cols[i]:
                st.image(url, use_column_width=True, caption=f"Img {i+1}")
                st.download_button("⬇️", url, f"house_{i+1}.png", key=f"dl{i}")

with tab2:
    st.subheader("🖼️ My Gallery")
    if "history" not in st.session_state or not st.session_state.history:
        st.info("No houses yet. Generate some!")
    else:
        for item in st.session_state.history:
            st.markdown(f"**{item['time']}** — {item['prompt']}")
            cols = st.columns(4)
            for i, url in enumerate(item["images"]):
                with cols[i]:
                    st.image(url, use_column_width=True)

with tab3:
    st.info("❤️ Favorites coming in next update...")

st.caption("Built with ❤️ by Helgi while traveling • Powered by xAI Grok Imagine")