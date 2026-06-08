import streamlit as st
from openai import OpenAI
import random
from datetime import datetime
import json

st.set_page_config(page_title="🏠 Grok Architecture Studio", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .stTabs [data-baseweb="tab-list"] button { color: #FFFFFF !important; font-weight: 600; }
    .stTabs [data-baseweb="tab-list"] button:hover { color: #FFCC00 !important; }
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

# ====================== SAFE API KEY ======================
api_key = None
try:
    api_key = st.secrets["XAI_API_KEY"]
except:
    api_key = st.sidebar.text_input("🔑 xAI API Key (local testing)", type="password")

# Load favorites
if "favorites" not in st.session_state:
    try:
        with open("favorites.json", "r") as f:
            st.session_state.favorites = json.load(f)
    except:
        st.session_state.favorites = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    mode = st.radio("Design Mode", ["Exterior", "Interior"], horizontal=True)
    num_images = st.slider("Number of images", 1, 4, 3)

tab1, tab2, tab3 = st.tabs(["🎨 Create", "❤️ Favorites", "🖼️ All Gallery"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Design Parameters")
        view_type = st.selectbox("View Type", ["exterior outlook", "interior living room", "interior kitchen", "interior bedroom", "drone view"])
        house_type = st.text_input("House Type", "modern minimalist villa")
        roof = st.text_input("Roof / Ceiling", "flat roof with generous overhangs")
        materials = st.text_input("Materials", "white concrete, warm wood accents, large glass panels")
        landscape = st.text_input("Surroundings", "Mediterranean garden, infinity pool, Lisbon hills")
        lighting = st.selectbox("Lighting", ["golden hour sunset", "soft morning light", "dramatic blue hour", "cozy interior lighting"])
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
            if not api_key:
                st.error("Please enter your xAI API key in the sidebar")
            else:
                with st.spinner("Generating..."):
                    try:
                        client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                        base = f"A highly detailed {view_type} of a {house_type} with {roof}, {materials}"
                        if landscape and mode == "Exterior":
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

    # Latest Generation
    if "history" in st.session_state and st.session_state.history:
        item = st.session_state.history[0]
        st.subheader("Latest Generation")
        cols = st.columns(4)
        for i, url in enumerate(item["images"]):
            with cols[i]:
                st.image(url, use_column_width=True)
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("❤️", key=f"heart_latest_{i}"):
                        st.session_state.favorites.append({"url": url, "prompt": item["prompt"], "time": item["time"]})
                        st.toast("❤️ Added!")
                with c2:
                    if st.button("🔄 Variant", key=f"var_latest_{i}"):
                        st.session_state.variant_base = url
                        st.session_state.variant_prompt = item["prompt"]
                        st.rerun()

# Variant Feature
if "variant_base" in st.session_state:
    st.subheader("🔄 Create Variant")
    desc = st.text_input("How should it differ?", placeholder="make it more luxurious, add a pool, night time, warmer colors...")
    if st.button("Generate Variant"):
        if api_key:
            with st.spinner("Creating variant..."):
                new_prompt = st.session_state.variant_prompt + f". {desc}"
                try:
                    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                    response = client.images.generate(model="grok-imagine-image-quality", prompt=new_prompt, n=1, response_format="url")
                    new_url = response.data[0].url
                    st.image(new_url, use_column_width=True)
                    if st.button("❤️ Save this variant"):
                        st.session_state.favorites.append({"url": new_url, "prompt": new_prompt, "time": datetime.now().strftime("%H:%M")})
                        st.toast("❤️ Saved!")
                except Exception as e:
                    st.error(e)
        else:
            st.error("API key required")

with tab2:
    st.subheader("❤️ My Favorites")
    if not st.session_state.favorites:
        st.info("No favorites yet")
    else:
        if st.button("💾 Save to file"):
            with open("favorites.json", "w") as f:
                json.dump(st.session_state.favorites, f)
            st.success("Saved!")
        uploaded = st.file_uploader("Load saved favorites", type="json")
        if uploaded:
            st.session_state.favorites = json.load(uploaded)
            st.success("Loaded!")

        cols = st.columns(3)
        for idx, fav in enumerate(st.session_state.favorites):
            with cols[idx % 3]:
                st.image(fav["url"], use_column_width=True)
                st.caption(fav["time"])
                c1, c2 = st.columns(2)
                with c1:
                    st.download_button("⬇️", fav["url"], f"favorite_{idx}.png", key=f"dl{idx}")
                with c2:
                    if st.button("🗑️", key=f"rem{idx}"):
                        st.session_state.favorites.pop(idx)
                        st.rerun()

with tab3:
    st.subheader("🖼️ All Gallery")
    if "history" not in st.session_state or not st.session_state.history:
        st.info("Generate some images first!")
    else:
        for gen_idx, item in enumerate(st.session_state.history):
            st.markdown(f"**{item['time']}** — {item['mode']} • {item['prompt']}")
            cols = st.columns(4)
            for i, url in enumerate(item["images"]):
                with cols[i]:
                    st.image(url, use_column_width=True)
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("❤️", key=f"allh_{gen_idx}_{i}"):
                            st.session_state.favorites.append({"url": url, "prompt": item["prompt"], "time": item["time"]})
                            st.toast("❤️ Added!")
                    with c2:
                        if st.button("🔄", key=f"allv_{gen_idx}_{i}"):
                            st.session_state.variant_base = url
                            st.session_state.variant_prompt = item["prompt"]
                            st.rerun()

st.caption("Built with ❤️ by Helgi • Powered by xAI Grok Imagine")
