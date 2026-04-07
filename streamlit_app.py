import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


page = st.sidebar.selectbox(
    "Navigate",
    ["Home", "Gene Expression Analysis", "Team"]
)


if page == "Home":

    st.title("NCBI Gene Expression Explorer")

    st.markdown("""
    ### About the Project
    This tool is designed to analyze gene expression datasets from the 
    NCBI Gene Expression Omnibus (GEO). It allows users to explore, visualize,
    and interpret genomic data easily.

    ### Features
    - Upload GEO datasets (CSV)
    - Data cleaning and preprocessing
    - Gene expression visualization
    - Identification of highest & lowest expressed genes
    - Correlation heatmap
    - PCA analysis
    - Gene search functionality

    ### Applications
    - Cancer gene expression analysis
    - Biomarker discovery (basic level)
    - Genomics research and education

    ### Technologies Used
    - Python
    - Streamlit
    - Pandas, NumPy
    - Matplotlib, Seaborn
    - Scikit-learn
    """)


elif page == "Gene Expression Analysis":

    st.title("Advanced Gene Expression Explorer")

    file = st.file_uploader("Upload GEO Dataset (CSV)", type=["csv"])

    if file:
        df = pd.read_csv(file)

        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        # Set gene names
        df = df.set_index(df.columns[0])
        df = df.apply(pd.to_numeric, errors='coerce')

        # Filling missing values
        st.subheader("Data Cleaning")
        if st.checkbox("Fill Missing Values with Mean"):
            df = df.fillna(df.mean())
            st.success("Missing values filled!")

        numeric_cols = df.select_dtypes(include='number').columns

        if len(numeric_cols) > 0:

            col = st.selectbox("Select Sample Column", numeric_cols)

            if st.checkbox("Apply Log Transformation"):
                df[col] = np.log1p(df[col])

            # Histogram
            st.subheader("Expression Distribution")
            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax)
            st.pyplot(fig)

            # Boxplot
            st.subheader("Distribution Shape")
            fig2, ax2 = plt.subplots()
            sns.boxplot(x=df[col], ax=ax2)
            st.pyplot(fig2)

            # Top genes
            st.subheader("Top 10 Expressed Genes")
            top = df.sort_values(by=col, ascending=False).head(10)
            st.dataframe(top)

            # Highest & Lowest
            st.subheader("Highest & Lowest Expressed Genes")

            df["Mean_Expression"] = df[numeric_cols].mean(axis=1)

            highest_gene = df["Mean_Expression"].idxmax()
            lowest_gene = df["Mean_Expression"].idxmin()

            st.write(f"Highest: {highest_gene}")
            st.write(f"Lowest: {lowest_gene}")

            # Bar graph
            bar_df = pd.DataFrame({
                "Gene": [highest_gene, lowest_gene],
                "Expression": [
                    df.loc[highest_gene, "Mean_Expression"],
                    df.loc[lowest_gene, "Mean_Expression"]
                ]
            })

            fig_bar, ax_bar = plt.subplots()
            ax_bar.bar(bar_df["Gene"], bar_df["Expression"])
            st.pyplot(fig_bar)

            # Heatmap
            st.subheader("Correlation Heatmap")
            fig4, ax4 = plt.subplots()
            sns.heatmap(df[numeric_cols].corr(), cmap="coolwarm", ax=ax4)
            st.pyplot(fig4)

            # PCA
            st.subheader("PCA Analysis")
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(df[numeric_cols])

            pca = PCA(n_components=2)
            pca_result = pca.fit_transform(scaled_data)

            fig5, ax5 = plt.subplots()
            ax5.scatter(pca_result[:,0], pca_result[:,1])
            st.pyplot(fig5)

            # Search
            st.subheader("Search Gene")
            search = st.text_input("Enter Gene Name")
            if search:
                result = df[df.index.str.contains(search, case=False)]
                st.dataframe(result)

            # Stats
            st.subheader("Summary Statistics")
            st.write(df.describe())

        else:
            st.warning("No numeric columns found!")

elif page == "Team":

    st.title("Project Team")

    st.markdown("""
    ### Team Members
    - **Anchala Kumari**   anchalakri7509@gmail.com 
    - **Dr. Kushagra Kashyap (Project Guide)**    kushagra.kashyap@despu.edu.in


    ### Course
    M.Sc Bioinformatics  

    ### Institution
    DES Pune University

    ### Acknowledgement
    I sincerely thank my project guide for his constant guidance and support in completing this project.

    """)
