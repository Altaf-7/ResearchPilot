import streamlit as st
import requests

API_URL = "http://localhost:8000/api/research"

st.set_page_config(page_title="ResearchPilot", layout="wide")

st.title("ResearchPilot 🚀")
st.subheader("Autonomous AI Research Agent")

question = st.text_input("What would you like to research?", placeholder="e.g., What are the core components of LangChain?")

if st.button("Generate Report"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Agents are researching... (This may take 10-30 seconds)"):
            try:
                response = requests.post(API_URL, json={"question": question}, timeout=120)
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success("Research Complete!")
                    
                    # Split into columns for Report and Sources
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"### {data['research_question']}")
                        st.markdown("#### Executive Summary")
                        st.markdown(data["executive_summary"])
                        
                        st.markdown("#### Key Findings")
                        for finding in data["key_findings"]:
                            st.markdown(f"- {finding}")
                            
                        st.markdown("#### Detailed Analysis")
                        st.markdown(data["detailed_analysis"])
                        
                        st.markdown("#### Limitations")
                        st.markdown(data["limitations"])
                        
                    with col2:
                        st.markdown("### Sources Cited")
                        if not data["sources"]:
                            st.info("No external sources or documents were cited.")
                        else:
                            for idx, source in enumerate(data["sources"], 1):
                                with st.expander(f"[{idx}] {source['title']}"):
                                    st.write(f"**Type:** {source['source_type']}")
                                    st.write(f"**Location:** {source['url_or_id']}")
                                    if source.get("metadata") and "snippet" in source["metadata"]:
                                        st.write(f"**Snippet:** {source['metadata']['snippet']}")
                else:
                    st.error(f"API Error: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Failed to connect to the API. Is the FastAPI server running on http://localhost:8000?")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
