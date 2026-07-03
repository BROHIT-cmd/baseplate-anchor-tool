import streamlit as st

from calculations import *

from data import *


st.set_page_config(layout="wide")

st.title(
    "Submersible Pump Foundation & Anchor Design Tool"
)

st.header("Inputs")

col1,col2 = st.columns(2)

with col1:

    weight = st.number_input(
        "Pump Weight (kg)",
        value=2000
    )

    flow = st.number_input(
        "Duty Flow (m3/hr)",
        value=100
    )

    head = st.number_input(
        "Head (m)",
        value=10
    )

    pipe_size = st.selectbox(
        "Pipe Size",
        list(PIPE_DATA.keys())
    )

with col2:

    pipe_length = st.number_input(
        "Pipe Length (m)",
        value=10
    )

    orientation = st.selectbox(
        "Pipe Orientation",
        [
            "Horizontal",
            "Vertical"
        ]
    )

    concrete = st.selectbox(
        "Concrete Grade",
        [
            "M20",
            "M25",
            "M30",
            "M35"
        ]
    )


if st.button("Run Analysis"):

    load = calculate_operating_load(weight)

    spacing = support_spacing(pipe_size)

    qty = support_quantity(
        pipe_length,
        spacing
    )

    locations = support_locations(
        pipe_length,
        spacing
    )

    anchor = recommend_anchor(weight)

    hole = ANCHORS[anchor]["hole"]

    slot_width = ANCHORS[anchor]["slot_width"]

    slot_length = ANCHORS[anchor]["slot_length"]

    embedment = ANCHORS[anchor]["embedment"]

    length,width,thickness = (
        recommend_baseplate(weight)
    )

    st.header("Results")

    st.write(
        f"Operating Load : {load:.2f} kN"
    )

    st.write(
        f"Support Spacing : {spacing} m"
    )

    st.write(
        f"Supports Required : {qty}"
    )

    st.write(
        f"Support Locations : {locations}"
    )

    st.write(
        f"Recommended Anchor : {anchor}"
    )

    st.write(
        f"Hole Size : Ø{hole} mm"
    )

    st.write(
        f"Slot Size : {slot_width} x {slot_length} mm"
    )

    st.write(
        f"Embedment Depth : {embedment} mm"
    )

    st.write(
        f"Baseplate Length : {length} mm"
    )

    st.write(
        f"Baseplate Width : {width} mm"
    )

    st.write(
        f"Baseplate Thickness : {thickness} mm"
    )

    st.success(
        "Preliminary recommendation only. Verify through FEA/Hilti/Structural review."
    )
