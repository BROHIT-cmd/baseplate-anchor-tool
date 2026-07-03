import streamlit as st

from anchor_data import *
from calculations import *
from report_generator import *

st.set_page_config(
    page_title="Baseplate Anchor Design Tool",
    layout="wide"
)

st.title("🔩 Baseplate Anchor & Foundation Design Tool")

st.markdown("""
Preliminary Design Tool for:

- Anchor Selection Review
- Hole Size Recommendation
- Slot Size Recommendation
- Embedment Depth Recommendation
- FEA Submission Support
""")

# ============================
# INPUTS
# ============================

st.header("Input Parameters")

col1, col2 = st.columns(2)

with col1:

    pump_weight = st.number_input(
        "Pump Weight (kg)",
        value=1500.0
    )

    duty_flow = st.number_input(
        "Duty Flow (m³/hr)",
        value=300.0
    )

    head = st.number_input(
        "Head (m)",
        value=40.0
    )

    pipe_size = st.number_input(
        "Pipe Size DN",
        value=200
    )

with col2:

    pipe_length = st.number_input(
        "Pipe Length (m)",
        value=10.0
    )

    support = st.selectbox(
        "Pipe Support Arrangement",
        [
            "Vertical Pipe - Horizontal Support",
            "Horizontal Pipe - Vertical Support"
        ]
    )

    anchors = st.selectbox(
        "Number of Anchors",
        [4, 6, 8, 12]
    )

    anchor = st.selectbox(
        "Selected Anchor",
        list(ANCHOR_CAPACITY.keys())
    )

concrete = st.selectbox(
    "Concrete Grade",
    list(CONCRETE_FACTOR.keys())
)

# ============================
# RUN
# ============================

if st.button("▶ Run Review"):

    pump_load = calculate_pump_load(
        pump_weight
    )

    additional_load = estimate_additional_load(
        pump_load,
        duty_flow,
        head,
        pipe_size,
        pipe_length
    )

    total = total_load(
        pump_load,
        additional_load
    )

    anchor_load = load_per_anchor(
        total,
        anchors
    )

    utilization = calculate_utilization(
        anchor_load,
        anchor
    )

    embedment = embedment_depth(
        anchor,
        concrete
    )

    hole = HOLE_SIZE[anchor]

    slot_width, slot_length = slot_size(
        anchor
    )

    st.header("Results")

    colA, colB = st.columns(2)

    with colA:

        st.metric(
            "Pump Load (kN)",
            f"{pump_load:.2f}"
        )

        st.metric(
            "Additional Load (kN)",
            f"{additional_load:.2f}"
        )

        st.metric(
            "Total Load (kN)",
            f"{total:.2f}"
        )

        st.metric(
            "Load per Anchor (kN)",
            f"{anchor_load:.2f}"
        )

    with colB:

        st.metric(
            "Anchor",
            anchor
        )

        st.metric(
            "Hole Size",
            f"Ø {hole} mm"
        )

        st.metric(
            "Slot Size",
            f"{slot_width} x {slot_length}"
        )

        st.metric(
            "Embedment",
            f"{embedment:.0f} mm"
        )

    st.subheader("Anchor Utilization")

    st.write(
        f"{utilization:.1f}%"
    )

    if utilization < 70:
        st.success(
            "✅ Safe"
        )

    elif utilization < 90:
        st.warning(
            "🟡 Review Recommended"
        )

    elif utilization <= 100:
        st.warning(
            "🟠 Near Capacity"
        )

    else:
        st.error(
            "🔴 Upgrade Anchor"
        )

    report_data = {

        "Pump Weight":
            pump_weight,

        "Flow":
            duty_flow,

        "Head":
            head,

        "Pipe Length":
            pipe_length,

        "Anchor":
            anchor,

        "Hole Size":
            f"Ø {hole}",

        "Embedment":
            f"{embedment:.0f} mm",

        "Load/Anchor":
            f"{anchor_load:.2f} kN",

        "Utilization":
            f"{utilization:.1f}%"
    }

    pdf = create_pdf(
        report_data
    )

    with open(pdf, "rb") as file:

        st.download_button(
            label="📄 Download Report",
            data=file,
            file_name="Anchor_Design_Report.pdf",
            mime="application/pdf"
        )

# ============================
# CONCRETE GUIDE
# ============================

with st.expander("📘 Concrete Grade Guide"):

    st.markdown("""
### M20
Light-duty foundations

### M25
Typical pump foundations

### M30
Heavy-duty machine foundations

### M35
Industrial equipment foundations

### M40
Critical heavy-duty installations
""")
