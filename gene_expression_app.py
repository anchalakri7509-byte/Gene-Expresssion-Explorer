import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Gene Expression Explorer", layout="wide")

# Sidebar
page = st.sidebar.selectbox(
    "Navigate",
    ["🏠 Home", "📂 Submit Data", "📊 Results", "👥 Team"]
)

# -------------------------------
# 🏠 HOME PAGE
# -------------------------------
if page == "🏠 Home":


    col1, col2 = st.columns([4, 1])

    with col1:
        st.title("🧬 Gene Expression Explorer")

    with col2:
        st.image(
            "https://portal.cofa.org.ar/wp-content/uploads/2018/04/adn-4.jpg",
            width=120
        )

    st.markdown("""
    ### 🔬 About the Project
    This application analyzes gene expression datasets from the 
    NCBI GEO database and provides biological insights.

    ### 🚀 Features
    - Upload gene expression datasets
    - Visualization of expression patterns
    - PCA
    - Comparison of Multiple Samples
    - Volcano plot for biomarker discovery
    - Identification of highly expressed genes

    ### 🧠 Applications
    - Cancer research  
    - Biomarker identification  
    - Genomics learning  

    ### ⚙️ Technologies  
    Python<br>
    Streamlit<br>
    Pandas<br>
    Matplotlib<br>
    NumPy<br>
    Scikit-learn<br>
    """, unsafe_allow_html=True)

# -------------------------------
# 📂 SUBMISSION PAGE
# -------------------------------
elif page == "📂 Submit Data":

    st.title("📂 Upload Dataset")

    file = st.file_uploader("Upload your CSV file", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.session_state["data"] = df
        st.success("✅ File uploaded successfully!")

# -------------------------------
# 📊 RESULTS PAGE
# -------------------------------
elif page == "📊 Results":

    st.title("📊 Analysis Results")

    if "data" not in st.session_state:
        st.warning("⚠️ Please upload a dataset first!")
    else:
        df = st.session_state["data"]

        df = df.set_index(df.columns[0])
        df = df.apply(pd.to_numeric, errors='coerce')
        df = df.fillna(df.mean())

        numeric_cols = df.columns

        # -------------------------------
        # Histogram
        # -------------------------------
        st.subheader("📊 Expression Distribution")
        col = st.selectbox("Select Sample", numeric_cols)

        fig, ax = plt.subplots()
        ax.hist(df[col], color='purple')
        ax.set_xlabel("Expression Value")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        # -------------------------------
        # Highest & Lowest
        # -------------------------------
        df["Mean"] = df.mean(axis=1)

        high = df["Mean"].idxmax()
        low = df["Mean"].idxmin()

        st.write(f"🔴 Highest Gene: {high}")
        st.write(f"🔵 Lowest Gene: {low}")

        fig2, ax2 = plt.subplots()
        ax2.bar([high, low],
                [df.loc[high, "Mean"], df.loc[low, "Mean"]],
                color=['red', 'blue'])
        ax2.set_xlabel("Gene")
        ax2.set_ylabel("Mean Expression")
        st.pyplot(fig2)

        
        # 📦 Boxplot Comparison (Multiple Samples)
        # -------------------------------
        st.subheader("📦 Boxplot Comparison Across Samples")

        # Select multiple samples
        selected_cols = st.multiselect(
        "Select Samples to Compare",
        numeric_cols,
        default=list(numeric_cols[:3])  # default first 3
        )

        if len(selected_cols) > 0:
            # Prepare data
            box_data = df[selected_cols]

            fig_box, ax_box = plt.subplots()

            sns.boxplot(data=box_data, ax=ax_box, palette="Set2")

            ax_box.set_xlabel("Samples")
            ax_box.set_ylabel("Gene Expression Level")
            ax_box.set_title("Expression Distribution Across Samples")

            st.pyplot(fig_box)

        else:
            st.warning("Please select at least one sample")

        # -------------------------------
        # Heatmap
        # -------------------------------
        st.subheader("🔥 Correlation Heatmap")
        fig3, ax3 = plt.subplots()
        sns.heatmap(df[numeric_cols].corr(), cmap="coolwarm", ax=ax3)
        ax3.set_xlabel("Samples")
        ax3.set_ylabel("Samples")
        st.pyplot(fig3)

        # -------------------------------
        # PCA
        # -------------------------------
        st.subheader("📉 PCA Analysis")

        scaler = StandardScaler()
        scaled = scaler.fit_transform(df[numeric_cols])

        pca = PCA(n_components=2)
        pca_res = pca.fit_transform(scaled)

        fig4, ax4 = plt.subplots()
        ax4.scatter(pca_res[:,0], pca_res[:,1], color='green')
        ax4.set_xlabel("PC1")
        ax4.set_ylabel("PC2")
        st.pyplot(fig4)

        # -------------------------------
        # Volcano Plot
        # -------------------------------
        st.subheader("🌋 Volcano Plot")

        logFC = df[numeric_cols].mean(axis=1)
        pvals = np.random.rand(len(df))  # simulated p-values

        volcano = pd.DataFrame({
            "logFC": logFC,
            "-log10(p)": -np.log10(pvals)
        })

        fig5, ax5 = plt.subplots()
        ax5.scatter(volcano["logFC"], volcano["-log10(p)"], color='orange')
        ax5.set_xlabel("Log Fold Change")
        ax5.set_ylabel("-log10(p-value)")
        st.pyplot(fig5)


        # -------------------------------
        # Download
        # -------------------------------
        st.subheader("⬇️ Download Results")

        csv = df.to_csv().encode('utf-8')

        st.download_button(
            "Download Processed Data",
            csv,
            "results.csv",
            "text/csv"
        )

# -------------------------------
# 👥 TEAM PAGE
# -------------------------------
elif page == "👥 Team":
    
    st.title("👥 Project Team")

    st.markdown("""
    **Anchala Kumari**<br>
    M.Sc. Bioinformatics<br>
    DES Pune University<br>  anchalakri7509@gmail.com<br><br>

    **Dr. Kushagra Kashyap (Project Guide)**<br> 
    Assistant Professor<br>
    DES Pune University<br>
    kushagra.kashyap@despu.edu.in  
""", unsafe_allow_html=True)
