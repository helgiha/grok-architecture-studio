import streamlit as st
from openai import OpenAI
import random
from datetime import datetime

st.set_page_config(page_title="🏠 Grok Architecture Studio", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .heart-button { color: #FF4B4B; font-size: 1.5rem; }
</style>
""", unsafe_allow_html=True)

st.title("🏠 Grok Architecture Studio")
st.markdown("**Professional AI Architectural Visualizer • Powered by xAI Grok Imagine**")

with st.expander("👋 My Story", expanded=False):
    st.markdown("""
    Hi, I always wanted to be an architect. Engineering became my path, but the dream never died.  
    Recently I was accepted into architecture studies and built this tool with Grok while traveling.  
    **Welcome to my personal Architecture Studio!** 🌍✨
    """)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    mode = st.radio("Design Mode", ["Exterior", "Interior"], horizontal=True)
    num_images = st.slider("Number of images", 1, 4, 4)

# Tabs
tab1, tab2, tab3 = st.tabs(["🎨 Create", "❤️ Favorites", "🖼️ All Gallery"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Design Parameters")
        view_type = st.selectbox("View Type", ["exterior outlook", "interior", "drone view", "isometric", "perspective"])
        house_type = st.text_input("House Type", "modern minimalist villa")
        roof = st.text_input("Roof / Ceiling", "flat roof with generous overhangs")
        materials = st.text_input("Materials", "white concrete, warm wood accents, large glass panels")
        landscape = st.text_input("Surroundings", "Mediterranean garden, infinity pool, Lisbon hills")
        lighting = st.selectbox("Lighting", ["golden hour sunset", "soft morning light", "dramatic blue hour"])
        mood = st.text_input("Mood", "warm, serene and luxurious")

    with col2:
        st.subheader("Quick Actions")
        if st.button("🎲 Surprise Me!", type="primary", use_container_width=True):
            presets = [
                ("modern minimalist villa", "flat roof", "white concrete and glass", "Lisbon hills with ocean view", "golden hour sunset", "serene luxury"),
                ("Lisbon traditional townhouse", "terracotta roof", "colorful azulejo tiles", "narrow cobblestone street", "golden hour sunset", "charming and vibrant"),
                ("luxury contemporary villa", "green living roof", "wood and stone", "cliff overlooking the sea", "dramatic blue hour", "exclusive"),
            ]
            choice = random.choice(presets)
            keys = ["house_type", "roof", "materials", "landscape", "lighting", "mood"]
            for k, v in zip(keys, choice):
                st.session_state[k] = v
            st.rerun()

        if st.button("🚀 Generate Images", type="primary", use_container_width=True):
            with st.spinner("Generating beautiful images..."):
                try:
                    client = OpenAI(api_key=st.secrets["XAI_API_KEY"], base_url="https://api.x.ai/v1")
                    base = f"A highly detailed {view_type} of a {house_type} with {roof}, {materials}"
                    if landscape:
                        base += f", set in {landscape}"
                    prompt = f"{base}. {lighting}, {mood} atmosphere. Professional architectural visualization, sharp details, photorealistic."

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
                        "time": datetime.now().strftime("%H:%M"),
                        "mode": mode
                    })
                    st.success("✅ Images generated!")
                except Exception as e:
                    st.error(f"Error: {e}")

    # Display latest generation with actions
    if "history" in st.session_state and st.session_state.history:
        item = st.session_state.history[0]
        st.subheader("Latest Generation")
        cols = st.columns(4)
        for i, url in enumerate(item["images"]):
            with cols[i]:
                st.image(url, use_column_width=True)
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("❤️", key=f"heart_{i}"):
                        if "favorites" not in st.session_state:
                            st.session_state.favorites = []
                        st.session_state.favorites.append({
                            "url": url, 
                            "prompt": item["prompt"], 
                            "time": item["time"]
                        })
                        st.toast("Added to Favorites ❤️", icon="❤️")
                with col_b:
                    if st.button("🔄 Variant", key=f"var_{i}"):
                        st.session_state.variant_base = url
                        st.rerun()

with tab2:
    st.subheader("❤️ My Favorites")
    if "favorites" not in st.session_state or not st.session_state.favorites:
        st.info("Click ❤️ on images you like to save them here")
    else:
        cols = st.columns(3)
        for idx, fav in enumerate(st.session_state.favorites):
            with cols[idx % 3]:
                st.image(fav["url"], use_column_width=True)
                st.caption(fav["time"])
                if st.button("Remove", key=f"rem_{idx}"):
                    st.session_state.favorites.pop(idx)
                    st.rerun()

with tab3:
    st.subheader("🖼️ All Gallery")
    if "history" not in st.session_state or not st.session_state.history:
        st.info("No generations yet")
    else:
        for item in st.session_state.history:
            st.markdown(f"**{item['time']}** — {item['mode']} • {item['prompt']}")
            cols = st.columns(4)
            for url in item["images"]:
                with cols[0]:
                    st.image(url, use_column_width=True)

st.caption("Built with ❤️ by Helgi • Powered by xAI Grok Imagine")
