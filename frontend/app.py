import streamlit as st, requests, os, time, json

st.set_page_config(page_title="Tech Spartans - Password AI", layout="wide")
st.title("🔑 Tech Spartans - Password Predictor & Cracker (Demo)")

st.sidebar.header("Controls")
predictor = st.sidebar.selectbox("Predictor", ["baseline","markov"])
top_n = st.sidebar.slider("Top N candidates to try", 50, 5000, 500, step=50)

st.markdown("### 1) Generate candidate passwords from model")
if st.button("Get Predictions"):
    try:
        r = requests.get(f"http://127.0.0.1:8000/predict?type={predictor}&top_n={top_n}", timeout=10)
        if r.status_code == 200:
            cands = r.json().get("candidates", [])
            st.success(f"Received {len(cands)} candidates (showing first 100)")
            st.write(cands[:100])
            # Save locally for quick use
            with open("candidates/latest.txt","w",encoding="utf-8") as f:
                for p in cands:
                    f.write(p+"\n")
        else:
            st.error("Failed to get predictions from backend")
    except Exception as e:
        st.error(str(e))

st.markdown("### 2) Upload hash file (MD5) and run cracking (demo uses Python MD5)")
uploaded_file = st.file_uploader("Upload a hash file (MD5 hashes, one per line or hash:plain)", type=["txt"])
if uploaded_file is not None:
    st.write("Uploaded:", uploaded_file.name)
    if st.button("Run Crack"):
        files = {"hashfile": (uploaded_file.name, uploaded_file.getvalue())}
        data = {"predictor": predictor, "top_n": top_n}
        with st.spinner("Cracking (this is a demo, using Python MD5 comparisons)..."):
            r = requests.post("http://127.0.0.1:8000/crack", files=files, data=data, timeout=120)
            if r.status_code == 200:
                resp = r.json()
                st.success(f"Done — tried {resp['candidates_tried']} candidates in {resp['duration_seconds']:.2f}s")
                st.write("Cracked results:")
                st.write(resp["cracked"])
            else:
                st.error("Crack failed: " + str(r.text))

st.markdown("---")
st.markdown("### Notes for judges")
st.markdown("- This is a hackathon demo: the 'cracker' here uses Python MD5 checks for simplicity (no Hashcat).")
st.markdown("- Use small hash files for fast demo. Example hash file is provided in `hashes/sample_md5.txt`.")
