import streamlit as st
from collections import Counter

st.set_page_config(
    page_title="ConsensusLab",
    page_icon="🌐",
    layout="wide"
)

# ---------- Custom Styling ----------
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        max-width: 1100px;
    }

    .hero {
        padding: 24px;
        border-radius: 16px;
        background: linear-gradient(120deg, #172554, #1e3a8a);
        color: white;
        margin-bottom: 24px;
    }

    .hero p {
        color: #dbeafe;
        margin-bottom: 0;
    }

    .node-card {
        padding: 18px;
        border: 1px solid #dbe3ee;
        border-radius: 12px;
        margin-bottom: 10px;
        background: var(--secondary-background-color);
    }

    .node-title {
        font-size: 18px;
        font-weight: 600;
    }

    .node-subtitle {
        color: var(--text-color);
        opacity: 0.75;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="hero">
    <h1>🌐 ConsensusLab</h1>
    <p>Distributed Consensus Simulator</p>
    <p>Explore how distributed nodes agree using majority voting.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Initialize State ----------
for i in range(1, 6):
    if f"node_{i}" not in st.session_state:
        st.session_state[f"node_{i}"] = "A"

if "result" not in st.session_state:
    st.session_state.result = None

# ---------- Reset ----------
def reset_votes():
    for i in range(1, 6):
        st.session_state[f"node_{i}"] = "A"
    st.session_state.result = None

# ---------- Metrics ----------
votes = [
    st.session_state[f"node_{i}"]
    for i in range(1, 6)
]

vote_counts = Counter(votes)
majority = len(votes) // 2 + 1

m1, m2, m3 = st.columns(3)

m1.metric("🖥️ Total Nodes", len(votes))
m2.metric("🗳️ Majority Required", majority)
m3.metric("📊 Values Available", 3)

st.divider()

# ---------- Node Configuration ----------
st.subheader("🖥️ Node Configuration")
st.caption("Choose a proposed value for each node.")

cols = st.columns(2)
votes = []

for i in range(1, 6):
    with cols[(i - 1) % 2]:
        st.markdown(
            f"""
            <div class="node-card">
                <div class="node-title">🖥️ Node {i}</div>
                <div class="node-subtitle">
                    Select the value this node supports
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        vote = st.selectbox(
            f"Vote for Node {i}",
            ["A", "B", "C"],
            key=f"node_{i}",
            label_visibility="collapsed"
        )
        votes.append(vote)

st.divider()

# ---------- Actions ----------
left, right = st.columns(2)

with left:
    run = st.button(
        "▶ Run Consensus",
        type="primary",
        use_container_width=True
    )

with right:
    st.button(
        "↻ Reset Votes",
        on_click=reset_votes,
        use_container_width=True
    )

# ---------- Consensus Logic ----------
if run:
    vote_counts = Counter(votes)
    winner = None

    for value, count in vote_counts.items():
        if count >= majority:
            winner = value
            break

    if winner:
        st.session_state.result = (
            True, winner, vote_counts[winner],
            dict(vote_counts)
        )
    else:
        st.session_state.result = (
            False, None, 0, dict(vote_counts)
        )

# ---------- Results ----------
if st.session_state.result is not None:
    success, winner, count, counts = st.session_state.result

    st.divider()
    st.subheader("📋 Consensus Results")

    if success:
        st.success(
            f"Consensus Reached! Value {winner} received "
            f"{count} out of {len(votes)} votes."
        )
    else:
        st.error("No Consensus! No value received a majority.")

    result_cols = st.columns(3)

    for i, value in enumerate(["A", "B", "C"]):
        result_cols[i].metric(
            f"Value {value}",
            f"{counts.get(value, 0)} votes"
        )

    st.subheader("Vote Distribution")

    for value in ["A", "B", "C"]:
        count_for_value = counts.get(value, 0)

        st.write(
            f"**Value {value}** — {count_for_value} vote(s)"
        )

        st.progress(count_for_value / len(votes))

st.divider()
st.caption(
    "ConsensusLab"
)