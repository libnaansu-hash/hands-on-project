import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Page settings
st.set_page_config(page_title="Expense Report Bot")

st.title("🤖 Expense Report Approval Bot")

st.write("""
Upload employee expense reports as CSV.

The bot will:
- Validate receipts
- Check policy limits
- Detect duplicate expenses
- Detect missing descriptions
- Generate an approval report for the Finance Manager
""")

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload Expense CSV",
    type=["csv"]
)

if uploaded_file is not None:

    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)

        st.subheader("Uploaded Expenses")
        st.dataframe(df)

        # Load policy limits
        with open("config.json", "r") as file:
            policy_limits = json.load(file)

        statuses = []
        remarks = []

        # Duplicate detection
        duplicate_mask = df.duplicated(
            subset=[
                "employee_name",
                "date",
                "description",
                "amount"
            ],
            keep=False
        )

        # Process each expense
        for index, row in df.iterrows():

            status = "Approved"
            comment = []

            category = row["category"]
            amount = row["amount"]

            receipt = str(
                row["receipt_attached"]
            ).strip().lower()

            description = str(
                row["description"]
            ).strip()

            # Receipt validation
            if receipt != "yes":
                status = "Flagged"
                comment.append("Receipt Missing")

            # Missing description
            if (
                description == ""
                or description.lower() == "nan"
            ):
                status = "Flagged"
                comment.append("Missing Description")

            # Policy limit check
            limit = policy_limits.get(category)

            if (
                limit is not None
                and amount > limit
            ):
                status = "Flagged"

                comment.append(
                    f"Exceeded {category} limit (${limit})"
                )

            # Duplicate check
            if duplicate_mask[index]:
                status = "Flagged"

                comment.append(
                    "Duplicate Expense"
                )

            statuses.append(status)

            if comment:
                remarks.append(
                    ", ".join(comment)
                )
            else:
                remarks.append(
                    "Valid Expense"
                )

        # Add results
        df["Status"] = statuses
        df["Remarks"] = remarks

        # Display results
        st.subheader("Approval Results")
        st.dataframe(df)

        # Summary
        total = len(df)

        approved = (
            df["Status"] == "Approved"
        ).sum()

        flagged = (
            df["Status"] == "Flagged"
        ).sum()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Expenses",
            total
        )

        col2.metric(
            "Approved",
            approved
        )

        col3.metric(
            "Flagged",
            flagged
        )

        # Save report
        os.makedirs(
            "reports",
            exist_ok=True
        )

        report_name = (
            f"reports/approval_report_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )

        df.to_excel(
            report_name,
            index=False
        )

        st.success(
            "Approval report generated successfully!"
        )

        # Download button
        with open(
            report_name,
            "rb"
        ) as file:

            st.download_button(
                label="📥 Download Approval Report",
                data=file,
                file_name=os.path.basename(
                    report_name
                ),
                mime=(
                    "application/"
                    "vnd.openxmlformats-"
                    "officedocument."
                    "spreadsheetml.sheet"
                )
            )

    except Exception as e:
        st.error(
            f"Error processing file: {e}"
        )



