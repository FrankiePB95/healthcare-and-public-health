import streamlit as st


def apply_shared_css():
    """Apply consistent CSS styling across all Streamlit pages"""
    st.markdown("""
    <style>
    /* Dark blue gradient background - regular blue with depth */
    .stApp {
        background: linear-gradient(135deg, #0a1929 0%, #1565c0 50%, #1976d2 100%);
        background-attachment: fixed;
        color: #000000;
    }
    
    /* Content container styling - space blue tones with bold borders */
    .main .block-container {
        background: rgba(72, 118, 191, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        border: 3px solid rgba(100, 100, 120, 0.8);
        font-weight: bold;
    }
    
    /* Header styling - black text, no default underlines (applied selectively in HTML) */
    h1 {
        color: #000000 !important;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        font-size: 3rem !important;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        font-weight: 900;
    }
    
    h1 .emoji, h1 span[role="img"] {
        text-decoration: none !important;
    }
    
    /* Subheader styling - black text, no default underlines (applied selectively in HTML) */
    h2, h3 {
        color: #000000 !important;
        border-bottom: 3px solid #1565c0;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-weight: bold;
    }
    
    h2 .emoji, h2 span[role="img"], h3 .emoji, h3 span[role="img"] {
        text-decoration: none !important;
    }
    
    /* All text elements - bold black text */
    .stMarkdown, .stText, p, div, span, label {
        color: #000000 !important;
        font-weight: bold;
    }
    
    /* Tab styling - blue theme with black text and borders */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: linear-gradient(90deg, #1565c0, #1976d2);
        border-radius: 10px;
        padding: 0.5rem;
        border: 2px solid rgba(100, 100, 120, 0.8);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: #000000 !important;
        font-weight: bold;
        border: 2px solid rgba(100, 100, 120, 0.6);
        padding: 0.8rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(52, 98, 171, 0.9) !important;
        color: #000000 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border: 3px solid rgba(100, 100, 120, 0.9);
        font-weight: bold;
    }
    
    /* Info box styling - blue theme with black text and borders */
    .stAlert > div {
        background: linear-gradient(135deg, #1565c0, #1976d2);
        color: #000000 !important;
        border: 3px solid rgba(100, 100, 120, 0.8);
        border-radius: 10px;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* Expander styling - blue theme with black text and borders */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #1565c0, #1976d2);
        color: #000000 !important;
        border-radius: 8px;
        font-weight: bold;
        border: 2px solid rgba(100, 100, 120, 0.8);
    }
    
    .streamlit-expanderContent {
        background: rgba(52, 98, 171, 0.8);
        border-radius: 8px;
        border: 2px solid #1565c0;
        color: #000000 !important;
        font-weight: bold;
    }
    
    /* DataFrame styling - space blue tones with bold borders */
    .stDataFrame {
        background: rgba(52, 98, 171, 0.9);
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        overflow: hidden;
        color: #000000 !important;
        border: 3px solid rgba(100, 100, 120, 0.8);
        font-weight: bold;
    }
    
    /* Metric cards styling - blue theme with black text and borders */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1565c0, #1976d2);
        border: 3px solid rgba(100, 100, 120, 0.8);
        padding: 1rem;
        border-radius: 10px;
        color: #000000 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        font-weight: bold;
    }
    
    [data-testid="metric-container"] > div {
        color: #000000 !important;
        font-weight: bold;
    }
    
    [data-testid="metric-container"] [data-testid="metric-container-label"] {
        color: #000000 !important;
        font-weight: bold;
    }
    
    [data-testid="metric-container"] [data-testid="metric-container-value"] {
        color: #000000 !important;
        font-weight: bold;
    }
    
    /* Custom card styling - space blue tones with black text and borders */
    .custom-card {
        background: rgba(52, 98, 171, 0.85);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        margin: 1rem 0;
        border-left: 5px solid #1565c0;
        border: 3px solid rgba(100, 100, 120, 0.8);
        font-weight: bold;
    }
    
    /* Button styling - blue theme with black text */
    .stButton > button {
        background: linear-gradient(135deg, #1565c0, #1976d2);
        color: #000000 !important;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
        background: linear-gradient(135deg, #1976d2, #1565c0);
    }
    
    /* Sidebar styling - dark blue theme */
    .css-1d391kg {
        background: linear-gradient(180deg, #0a1929, #1565c0);
    }
    
    /* Input and select styling - bold black text with borders */
    .stSelectbox > div > div {
        background: rgba(52, 98, 171, 0.8);
        color: #000000 !important;
        border: 2px solid #1565c0;
        font-weight: bold;
    }
    
    /* Success/Warning/Error message styling - blue theme with black text and borders */
    .stSuccess {
        background: linear-gradient(135deg, #27ae60, #2ecc71);
        border-radius: 10px;
        color: #000000 !important;
        border: 2px solid rgba(100, 100, 120, 0.8);
        font-weight: bold;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #f39c12, #e67e22);
        border-radius: 10px;
        color: #000000 !important;
        border: 2px solid rgba(100, 100, 120, 0.8);
        font-weight: bold;
    }
    
    .stError {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        border-radius: 10px;
        color: #000000 !important;
        border: 2px solid rgba(100, 100, 120, 0.8);
        font-weight: bold;
    }
    
    /* Ensure bold black text for all elements */
    * {
        color: #000000 !important;
        font-weight: bold;
    }
    
    /* Custom card text - bold */
    .custom-card h2, .custom-card h3, .custom-card p {
        color: #000000 !important;
        font-weight: bold;
    }
    
    /* Text styling improvements - bold */
    .stMarkdown {
        text-align: justify;
        line-height: 1.6;
        color: #000000 !important;
        font-weight: bold;
    }
    
    /* Strong/bold text styling */
    strong, b {
        color: #000000 !important;
        font-weight: 900;
    }
    
    /* List styling - bold */
    ul, ol, li {
        color: #000000 !important;
        font-weight: bold;
    }
    
    /* Code styling - bold with borders */
    code {
        color: #000000 !important;
        background: rgba(52, 98, 171, 0.8);
        border: 2px solid rgba(100, 100, 120, 0.8);
        font-weight: bold;
    }
    
    /* Plotly chart styling - removed double border, kept shadow and background */
    .js-plotly-plot, .plotly {
        border: none !important;
        border-radius: 10px !important;
        background: rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        margin: 1rem 0 !important;
    }
    
    /* Plotly modebar styling */
    .modebar {
        background: rgba(52, 98, 171, 0.8) !important;
        border-radius: 5px !important;
        border: 1px solid rgba(100, 100, 120, 0.6) !important;
    }
    
    /* Remove underlines from images and charts */
    img, .js-plotly-plot *, .plotly *, canvas, svg {
        text-decoration: none !important;
    }
    
    /* Remove underlines from icons and emojis */
    .stMarkdown span, .stText span, p span, div span, h1 span, h2 span, h3 span {
        text-decoration: none !important;
    }
    
    /* Specific emoji and icon styling - no underlines */
    .emoji, [role="img"], .icon {
        text-decoration: none !important;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)
