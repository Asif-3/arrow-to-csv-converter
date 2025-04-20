import streamlit as st
import pandas as pd
import pyarrow as pa
import io

st.set_page_config(page_title="Arrow to CSV Converter", layout="centered")
st.title("🔁 Hugging Face Arrow to CSV Converter")

uploaded_file = st.file_uploader("Upload a Hugging Face `.arrow` file", type=["arrow"])

if uploaded_file:
    try:
        # Read the raw arrow file (record batch format)
        buffer = uploaded_file.read()
        reader = pa.ipc.RecordBatchStreamReader(pa.py_buffer(buffer))
        table = reader.read_all()
        df = table.to_pandas()

        st.success("File loaded successfully!")
        st.dataframe(df.head())

        # Convert to CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)

        st.download_button(
            label="📥 Download CSV",
            data=csv_buffer.getvalue(),
            file_name="converted.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"⚠️ Error reading Arrow file: {e}")
else:
    st.info("Please upload a `.arrow` file (like from Hugging Face datasets).")
