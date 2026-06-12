# Streamlit UI - CS2 Skin Arbitrage Application (ASCII/UTF-8 safe)

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import logging

from data_fetcher import DataFetcher
from data_manager import DataManager
from price_analyzer import PriceAnalyzer
from commission_calculator import CommissionCalculator
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="CS2 Skin Arbitrage",
    page_icon=":moneybag:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.profit-positive { color: #28a745; font-weight: bold; }
.profit-negative { color: #dc3545; font-weight: bold; }
.rating-high { color: #28a745; }
.rating-medium { color: #ffc107; }
.rating-low { color: #dc3545; }
.source-status { padding: 10px; margin: 5px 0; border-radius: 5px; }
.source-success { background-color: #d4edda; border: 1px solid #c3e6cb; }
.source-failed { background-color: #f8d7da; border: 1px solid #f5c6cb; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_modules():
    data_fetcher = DataFetcher(
        user_agents=config.USER_AGENTS,
        timeout=config.REQUESTS_TIMEOUT,
        retry_count=config.REQUESTS_RETRY_COUNT,
        retry_delay=config.REQUESTS_RETRY_DELAY,
        request_delay_min=config.REQUEST_DELAY_MIN,
        request_delay_max=config.REQUEST_DELAY_MAX,
    )

    commission_calc = CommissionCalculator(
        site_commissions=config.SITE_COMMISSIONS.copy(),
        steam_commission=config.STEAM_COMMISSION_RATE,
    )

    price_analyzer = PriceAnalyzer(commission_calculator=commission_calc)
    data_manager = DataManager()

    return data_fetcher, commission_calc, price_analyzer, data_manager


def load_data_from_sources():
    data_fetcher = st.session_state.modules[0]

    with st.spinner("Fetching data from multiple sources..."):
        progress_bar = st.progress(0)
        status_container = st.container()

        all_data = data_fetcher.fetch_all_data()
        summary = data_fetcher.get_summary()

        with status_container:
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Fetched sources:**")
                for source in summary.get('fetched_sources', []):
                    st.markdown(f"<div class='source-status source-success'>? {source}</div>", unsafe_allow_html=True)

            with col2:
                if summary.get('failed_sources'):
                    st.write("**Failed sources:**")
                    for source in summary.get('failed_sources', []):
                        st.markdown(f"<div class='source-status source-failed'>? {source}</div>", unsafe_allow_html=True)

        progress_bar.progress(100)

    if not all_data:
        st.error("No data could be fetched from any source. Check your internet connection.")
        return []

    st.success(f"Retrieved data from {len(summary.get('fetched_sources', []))} sources ({len(all_data)} items)")
    return all_data


def main():
    st.title("CS2 Skin Arbitrage & Price Comparison")
    st.markdown("Find arbitrage opportunities across marketplaces")

    if "modules" not in st.session_state:
        st.session_state.modules = initialize_modules()

    data_fetcher, commission_calc, price_analyzer, data_manager = st.session_state.modules

    if "raw_data" not in st.session_state:
        st.session_state.raw_data = load_data_from_sources()

    raw_data = st.session_state.raw_data

    if not raw_data:
        st.error("No data available. Please refresh the page.")
        col1, _ = st.columns(2)
        with col1:
            if st.button("Retry Loading Data"):
                st.session_state.raw_data = None
                st.rerun()
        return

    if "df_skins" not in st.session_state:
        df = data_manager.create_skin_dataframe(raw_data)
        st.session_state.df_skins = df
        df_marketplace = data_manager.flatten_marketplace_data()
        st.session_state.df_marketplace = df_marketplace

    df_skins = st.session_state.df_skins
    df_marketplace = st.session_state.df_marketplace

    if df_marketplace.empty:
        st.warning("Marketplace data not available")
        return

    # Sidebar filters
    with st.sidebar:
        st.header("Filters & Settings")
        tabs = st.tabs(["Filters", "Settings", "Statistics"])

        with tabs[0]:
            rating_range = st.slider("Reliability (stars)", 1.0, 5.0, (3.5, 5.0), 0.1)
            profit_range = st.slider("Profit/Loss (%)", -100.0, 100.0, (-50.0, 50.0), 1.0)
            price_range = st.slider("Price Range (USD)", 0.01, 5000.0, (0.01, 500.0), 10.0)
            product_types = st.multiselect("Product Type", options=config.PRODUCT_TYPES, default=config.PRODUCT_TYPES)
            min_volume = st.number_input("Min Daily Volume", min_value=0, max_value=10000, value=config.MIN_DAILY_VOLUME, step=5)
            direction = st.radio("Transaction Direction", options=["Steam -> Cash", "Cash -> Steam"])
            direction_code = "steam_to_cash" if direction == "Steam -> Cash" else "cash_to_steam"

        with tabs[1]:
            st.subheader("Commission Rates (%)")
            updated_commissions = {}
            for site, commission in commission_calc.get_all_commissions().items():
                if site != "steam":
                    new_commission = st.number_input(site.upper(), min_value=0.0, max_value=50.0, value=float(commission), step=0.5)
                    updated_commissions[site] = new_commission
            if st.button("Update Commissions"):
                for site, commission in updated_commissions.items():
                    commission_calc.update_site_commission(site, commission)
                st.success("Commissions updated")
            st.write(f"Steam commission: {config.STEAM_COMMISSION_RATE}%")

        with tabs[2]:
            st.subheader("Data Statistics")
            if not df_skins.empty:
                st.metric("Products", len(df_skins))
                st.metric("Sites", df_marketplace['site'].nunique())
                st.metric("Avg Price", f"${df_skins['steam_price'].mean():.2f}")
                st.metric("Avg Daily Volume", f"{df_skins['daily_volume'].mean():.0f}")
                st.bar_chart(df_skins['product_type'].value_counts())

    col1, col2, col3 = st.columns(3)
    with col1:
        target_balance = st.number_input("Target Balance (USD)", min_value=1.0, max_value=100000.0, value=100.0, step=10.0)
    with col2:
        selected_site = st.selectbox("Transaction Site", options=sorted(df_marketplace['site'].unique()))
    with col3:
        if st.button("Refresh Data"):
            st.session_state.raw_data = load_data_from_sources()
            st.session_state.df_skins = None
            st.session_state.df_marketplace = None
            st.rerun()

    # Main processing
    try:
        df_with_profit = price_analyzer.calculate_profit_percentages(df_marketplace, direction=direction_code)
        df_filtered = data_manager.apply_filters(df=df_with_profit, min_rating=rating_range[0], max_rating=rating_range[1], min_price=price_range[0], max_price=price_range[1], product_types=product_types if product_types else None, min_volume=min_volume)
        df_filtered = df_filtered[(df_filtered['profit_percentage'] >= profit_range[0]) & (df_filtered['profit_percentage'] <= profit_range[1])]

        if df_filtered.empty:
            st.warning("No results found with current filters")
            return

        sort_option = st.selectbox("Sort By", ["Profit % (High to Low)", "Profit % (Low to High)", "Price (Low to High)", "Price (High to Low)", "Reliability (High to Low)"])
        display_count = st.slider("Display Count", min_value=5, max_value=100, value=20, step=5)

        if "Profit % (High to Low)" in sort_option:
            df_filtered = df_filtered.sort_values('profit_percentage', ascending=False)
        elif "Profit % (Low to High)" in sort_option:
            df_filtered = df_filtered.sort_values('profit_percentage', ascending=True)
        elif "Price (Low to High)" in sort_option:
            df_filtered = df_filtered.sort_values('steam_price', ascending=True)
        elif "Price (High to Low)" in sort_option:
            df_filtered = df_filtered.sort_values('steam_price', ascending=False)
        elif "Reliability (High to Low)" in sort_option:
            df_filtered = df_filtered.sort_values('site_rating', ascending=False)

        df_display = df_filtered.head(display_count).copy()
        quantities = []
        for idx, row in df_display.iterrows():
            qty, _, _ = commission_calc.calculate_quantity_needed(target_balance=target_balance, unit_price=row['steam_price'], direction=direction_code, site=row['site'])
            quantities.append(qty)
        df_display['Quantity'] = quantities

        display_df = df_display[['name', 'product_type', 'steam_price', 'site_price', 'site_rating', 'profit_percentage', 'site', 'daily_volume', 'Quantity']].copy()
        display_df.columns = ['Product Name', 'Type', 'Steam Price ($)', 'Site Price ($)', 'Rating', 'Profit/Loss (%)', 'Site', 'Daily Volume', 'Quantity']
        display_df['Steam Price ($)'] = display_df['Steam Price ($)'].apply(lambda x: f"${x:.2f}")
        display_df['Site Price ($)'] = display_df['Site Price ($)'].apply(lambda x: f"${x:.2f}")

        st.subheader(f"Results ({len(display_df)} items)")
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.subheader("Summary Statistics")
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        with col_stat1:
            st.metric("Avg Profit/Loss", f"{df_display['profit_percentage'].mean():.2f}%")
        with col_stat2:
            st.metric("Max Profit", f"{df_display['profit_percentage'].max():.2f}%")
        with col_stat3:
            st.metric("Min Profit", f"{df_display['profit_percentage'].min():.2f}%")
        with col_stat4:
            st.metric("Avg Rating", f"{df_display['site_rating'].mean():.2f}")

        # Export
        csv = display_df.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name=f"arbitrage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime="text/csv")
        try:
            from io import BytesIO
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                display_df.to_excel(writer, index=False, sheet_name='Arbitrage')
            buffer.seek(0)
            st.download_button(label="Download Excel", data=buffer.getvalue(), file_name=f"arbitrage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx", mime="application/vnd.ms-excel")
        except Exception:
            st.info("Excel export requires openpyxl")

    except Exception as e:
        st.error(f"Error: {e}")
        logger.error("Error in main", exc_info=True)


if __name__ == '__main__':
    main()
