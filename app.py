import streamlit as st
import pandas as pd
from datetime import datetime
from data_handler import save_data, load_data, search_data, delete_report
from visualizations import create_rejection_summary_chart, create_daily_production_chart
from pdf_generator import create_pdf_report

def calculate_total_cans(row):
    """Calculate total cans including all rejections and samples"""
    base_cans = row['TotalCase'] + row['LooseCans']
    rejection_fields = [
        'EmptyRejection', 'FilledRejection', 'BreakdownRejection',
        'ManpowerDentRejection', 'HighPressureRejection', 'WaterCanRejection',
        'MachineDentCans', 'FadeCans', 'UnprintedCans', 'ScratchedCans',
        'LidRejection', 'QASample', 'QAOtherSample'
    ]
    rejection_total = sum(row[field] for field in rejection_fields)
    return base_cans + rejection_total

def main():
    st.title("Production Daily Report Entry System")

    # Sidebar navigation
    page = st.sidebar.selectbox("Choose a page", ["Daily Entry", "View Reports", "Analytics"])

    if page == "Daily Entry":
        st.header("Daily Production Report Form")

        # Data entry form
        with st.form("report_form"):
            st.markdown("### Basic Information")
            col1, col2, col3 = st.columns(3)
            with col1:
                date = st.date_input("📅 Report Date", datetime.now())
            with col2:
                variant_name = st.text_input("🏷️ Variant Name")
            with col3:
                batch_code = st.text_input("📦 Batch Code")

            st.markdown("### Production Quantities")
            col4, col5, col6 = st.columns(3)
            with col4:
                total_case = st.number_input("📦 Total Case", min_value=0, help="Enter the total number of cases")
            with col5:
                loose_cans = st.number_input("🥫 Loose Cans", min_value=0, help="Enter number of loose cans")
            with col6:
                wip_cans = st.number_input("⚙️ WIP Cans", min_value=0, help="Work in progress cans")

            # QA Samples Section
            st.markdown("### QA Samples")
            col7, col8, col9 = st.columns(3)
            with col7:
                qa_sample = st.number_input("🔍 QA Sample", min_value=0)
            with col8:
                qa_other_sample = st.number_input("🔍 QA Other Sample", min_value=0)
            with col9:
                empty_sample = st.number_input("🔍 Empty Sample", min_value=0)

            # Rejections Section
            st.markdown("### Rejections")

            # Primary Rejections
            col10, col11, col12 = st.columns(3)
            with col10:
                empty_rejection = st.number_input("Empty Rejection", min_value=0)
                filled_rejection = st.number_input("Filled Rejection", min_value=0)
                breakdown_rejection = st.number_input("Breakdown Rejection", min_value=0)
            with col11:
                manpower_dent_rejection = st.number_input("Manpower Dent", min_value=0)
                high_pressure_rejection = st.number_input("High Pressure", min_value=0)
                water_can_rejection = st.number_input("Water Can", min_value=0)
            with col12:
                machine_dent_cans = st.number_input("Machine Dent", min_value=0)
                fade_cans = st.number_input("Fade Cans", min_value=0)
                lid_rejection = st.number_input("Lid Rejection", min_value=0)

            # Secondary Rejections
            col13, col14 = st.columns(2)
            with col13:
                unprinted_cans = st.number_input("Unprinted Cans", min_value=0)
                scratched_cans = st.number_input("Scratched Cans", min_value=0)
            with col14:
                reject_shipper = st.number_input("Reject Shipper", min_value=0)

            submitted = st.form_submit_button("Submit Report")

            if submitted:
                data = {
                    "Date": date,
                    "VariantName": variant_name,
                    "BatchCode": batch_code,
                    "TotalCase": total_case,
                    "LooseCans": loose_cans,
                    "EmptyRejection": empty_rejection,
                    "EmptySample": empty_sample,
                    "WIPCans": wip_cans,
                    "FilledRejection": filled_rejection,
                    "BreakdownRejection": breakdown_rejection,
                    "ManpowerDentRejection": manpower_dent_rejection,
                    "HighPressureRejection": high_pressure_rejection,
                    "WaterCanRejection": water_can_rejection,
                    "MachineDentCans": machine_dent_cans,
                    "FadeCans": fade_cans,
                    "UnprintedCans": unprinted_cans,
                    "ScratchedCans": scratched_cans,
                    "LidRejection": lid_rejection,
                    "QASample": qa_sample,
                    "QAOtherSample": qa_other_sample,
                    "RejectShipper": reject_shipper
                }
                save_data(data)
                st.success("Daily report saved successfully!")

    elif page == "View Reports":
        st.header("View Daily Reports")

        # Filters
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
            variant_filter = st.text_input("Filter by Variant Name")
        with col2:
            end_date = st.date_input("End Date")
            batch_filter = st.text_input("Filter by Batch Code")

        df = load_data()
        if df is not None and not df.empty:
            filtered_df = search_data(
                df, 
                start_date=start_date,
                end_date=end_date,
                batch_code=batch_filter if batch_filter else None,
                variant_name=variant_filter if variant_filter else None
            )

            # Single delete option with password protection
            st.subheader("Delete Option")
            admin_password = "admin123"  # You should change this password

            password = st.text_input("Admin password:", type="password", key="admin_pass")
            delete_option = st.selectbox("Select delete scope:", 
                                       ["Delete Filtered Reports", "Delete All Reports"])

            if st.button("🗑️ Delete Reports", type="secondary"):
                if password == admin_password:
                    if delete_option == "Delete Filtered Reports":
                        confirm = st.warning("Are you sure you want to delete all filtered reports?", icon="⚠️")
                        if confirm:
                            df = delete_report(
                                df,
                                start_date if start_date == end_date else None,
                                batch_filter if batch_filter else None,
                                variant_filter if variant_filter else None
                            )
                            st.success("Filtered reports deleted successfully!")
                            st.rerun()
                    else:
                        confirm = st.warning("Are you sure you want to delete ALL reports? This cannot be undone!", icon="⚠️")
                        if confirm:
                            df = delete_report(df, delete_all=True)
                            st.success("All reports deleted successfully!")
                            st.rerun()
                else:
                    st.error("Incorrect password!")

            # Display all data in an organized table
            if not filtered_df.empty:
                st.subheader("All Reports Data")

                # Group columns for better organization
                column_groups = {
                    "Basic Info": ['Date', 'VariantName', 'BatchCode', 'TotalCase', 'LooseCans', 'WIPCans'],
                    "Rejection Info": [col for col in filtered_df.columns if 'Rejection' in col] + ['RejectShipper'],
                    "QA Info": ['QASample', 'QAOtherSample', 'EmptySample']
                }

                # Create tabs for different views
                tabs = st.tabs(["Complete View"] + list(column_groups.keys()))

                # Complete view tab
                with tabs[0]:
                    st.dataframe(
                        filtered_df,
                        hide_index=True,
                        use_container_width=True,
                        column_config={
                            "Date": st.column_config.DateColumn("Date", help="Report date"),
                            "VariantName": st.column_config.TextColumn("Variant Name", help="Product variant name", width="medium"),
                            "BatchCode": st.column_config.TextColumn("Batch Code", help="Production batch code", width="medium"),
                            "TotalCase": st.column_config.NumberColumn("Total Cases", help="Number of total cases", format="%d"),
                            "LooseCans": st.column_config.NumberColumn("Loose Cans", help="Number of loose cans", format="%d"),
                            "EmptyRejection": st.column_config.NumberColumn("Empty Rej.", help="Empty can rejections", format="%d"),
                            "FilledRejection": st.column_config.NumberColumn("Filled Rej.", help="Filled can rejections", format="%d"),
                            "QASample": st.column_config.NumberColumn("QA Samples", help="Quality assurance samples", format="%d"),
                        },
                        height=400
                    )

                # Group-specific tabs
                for idx, (group_name, columns) in enumerate(column_groups.items(), 1):
                    with tabs[idx]:
                        st.dataframe(
                            filtered_df[columns],
                            hide_index=True,
                            use_container_width=True
                        )

            # Export buttons columns
            col1, col2 = st.columns(2)

            # CSV Export
            with col1:
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"production_report_{start_date}_to_{end_date}.csv",
                    mime="text/csv"
                )

            # PDF Export
            with col2:
                pdf = create_pdf_report(filtered_df, start_date, end_date)
                st.download_button(
                    label="Download PDF Report",
                    data=pdf,
                    file_name=f"production_report_{start_date}_to_{end_date}.pdf",
                    mime="application/pdf"
                )
        else:
            st.info("No reports available")

    else:  # Analytics page
        st.header("Production Analytics")

        df = load_data()
        if df is not None and not df.empty:
            # Daily production chart
            st.subheader("Daily Production Overview")
            fig_daily = create_daily_production_chart(df)
            st.plotly_chart(fig_daily)

            # Rejection analysis
            st.subheader("Rejection Analysis")
            fig_rejection = create_rejection_summary_chart(df)
            st.plotly_chart(fig_rejection)

            # Summary statistics
            st.subheader("Production Summary")
            summary = df.groupby("VariantName").agg({
                "TotalCase": "sum",
                "EmptyRejection": "sum",
                "FilledRejection": "sum",
                "QASample": "sum"
            }).round(2)
            st.dataframe(summary)
        else:
            st.info("No data available for analytics")

if __name__ == "__main__":
    main()