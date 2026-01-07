#!/bin/bash
# Railway startup script with proper port handling

# Use Railway's PORT if available, otherwise default to 8501
export STREAMLIT_SERVER_PORT=${PORT:-8501}
export STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run Streamlit
streamlit run app.py
