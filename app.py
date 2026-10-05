import streamlit as st
import pandas as pd

st.set_page_config(page_title="Deals Hub", layout="wide")

# Yahan apna Dropbox ya direct download link paste karein
# Dropbox link ke end mein ?dl=1 hona lazmi hai
FILE_LINK = "https://drive.google.com/uc?export=download&id=1vzCzVKzIxJaOHc6BcNziggmot8QOAkNR?dl=1"

@st.cache_data
def load_data(url):
    try:
        # Direct URL se CSV load karna
        return pd.read_csv(url) 
    except Exception as e:
        st.error(f"Data load nahi ho saka. Link check karein: {e}")
        return pd.DataFrame()

df = load_data(FILE_LINK)

# Header aur Last Updated Text
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.header("Deals Hub")
with col_h2:
    st.markdown("<p style='text-align: right; color: gray; margin-top: 20px;'>Deals last updated at 10/05/26 09:09 UTC | ↺ Recent exports</p>", unsafe_allow_html=True)

# Confidentiality Warning Banner
st.warning("⚠️ Deals are confidential and can be published only on or after they are published on www.amazon.co.uk. Amazon Prime Big Deal Days dates are confidential and can be communicated only after 15 September 2026 at 06:00 BST. Deal information is subject to change.")

# Export Deals button CSS
st.markdown("""
    <style>
    div.stDownloadButton > button:first-child {
        background-color: #FFD814;
        color: black;
        border-radius: 20px;
        border: 1px solid #FCD200;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- EXACT FILTERS ROW ---
st.write("") 
col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1.2, 1.2, 1.2, 1.2, 1.5, 1.5, 1, 1.5, 1.2])

with col1:
    filter_opt = st.selectbox("Filters", ["Filters (1)", "Best Deal", "Prime Exclusive"], label_visibility="collapsed")
with col2:
    cat_options = ["Category (1)"] + (df['productCategory'].dropna().unique().tolist() if not df.empty and 'productCategory' in df.columns else ["Lawn and Garden", "Home", "Toys"])
    selected_cat = st.selectbox("Category", cat_options, label_visibility="collapsed")
with col3:
    brand_opt = st.selectbox("Top brands", ["Top brands", "Brand A", "Brand B"], label_visibility="collapsed")
with col4:
    date_opt = st.selectbox("Live Dates", ["Live Dates", "Upcoming", "Active"], label_visibility="collapsed")
with col5:
    prev_linked = st.button("Previously Linked", use_container_width=True)
with col6:
    on_storefront = st.button("On Your Storefront", use_container_width=True)
with col7:
    if st.button("Clear filters", type="tertiary"):
        pass
with col8:
    sort_by = st.selectbox("Sort", ["Sort by Recommended", "Lowest Price YTD", "Discount %"], label_visibility="collapsed")
with col9:
    st.download_button("Export deals", data="csv_data_here", file_name="exported_deals.csv", mime="text/csv", use_container_width=True)

# ASIN Search bar
st.write("")
search_asin = st.text_input("🔍 Search by ASIN", placeholder="Exact ASIN yahan enter karein...")

st.markdown("---")

# Table Headers
h_col1, h_col2, h_col3, h_col4, h_col5 = st.columns([4, 2, 2, 2, 2])
with h_col1:
    st.markdown("**Deal Information**")
with h_col2:
    st.markdown("**Category**")
with h_col3:
    st.markdown("**Deal Tags**")
with h_col4:
    st.markdown("**Deal schedule**")
with h_col5:
    st.markdown("**Price history**")

st.divider()

# Data filtering
filtered_df = df.copy()
if not filtered_df.empty and search_asin:
    filtered_df = filtered_df[filtered_df['asin'].str.contains(search_asin, case=False, na=False)]

if not filtered_df.empty and selected_cat != "Category (1)":
    filtered_df = filtered_df[filtered_df['productCategory'] == selected_cat]

# Cards Generation
if not filtered_df.empty:
    for index, row in filtered_df.iterrows():
        c1, c2, c3, c4, c5 = st.columns([4, 2, 2, 2, 2])
        
        with c1:
            st.markdown(f"**[{row.get('deal.title', 'Product Title')}]({row.get('asinUrl', '#')})**")
            st.markdown(f"<h3 style='color: #B12704; margin:0;'>${row.get('promotionPrice', '0.00')} <span style='font-size: 14px; background-color: #cc0c39; color: white; padding: 2px 4px; border-radius: 2px;'>-{row.get('discountPct', 0)}%</span></h3>", unsafe_allow_html=True)
            st.write(f"ASIN: {row.get('asin', 'N/A')}")
            
        with c2:
            st.write(row.get('productCategory', 'Category'))
            if pd.notna(row.get('productSubC', None)):
                st.write(row.get('productSubC', ''))
                
        with c3:
            st.markdown("<span style='background-color: #c45500; color: white; padding: 2px 6px; border-radius: 4px; font-size: 12px;'>Upcoming</span>", unsafe_allow_html=True)
            if row.get('isPrimeOnly') == True:
                st.write("Prime Exclusive")
                
        with c4:
            st.write(f"Start: {row.get('promotionStartDate', 'N/A')}")
            st.write(f"End: {row.get('promotionEndDate', 'N/A')}")
            
        with c5:
            st.write("Lowest price YTD")
            st.write(f"**${row.get('lowestPriceYTD', row.get('promotionPrice', 'N/A'))}**")
            
        st.divider()
else:
    st.info("No deals match your filters. ASIN check karein ya URL verify karein.")
