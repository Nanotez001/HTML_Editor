import streamlit as st
import pandas as pd
import re

# --- Streamlit App ---
st.title("HTML Generator V.1.03")

col1, col2 = st.columns(2)
with col1:
    st.text("Initial Spec Text")
    text = st.text_area("ใส่ข้อมูลที่นี่", height=200)
    if st.button("Generate HTML"):
        if not text.strip():
            st.warning("กรุณาใส่ข้อมูลสเปคก่อน")
            st.stop()
    # ============================================================================

        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
        adjusted_category_headers = [
            "สเปค", "ย่อ", "ภาพรวม", "Display", "Video", "Audio", "Smart Service",
            "Smart Feature", "Game Feature", "Tuner/Broadcasting", "Connectivity",
            "Design", "Additional Feature", "Accessibility", "Power & Eco Solution",
            "Dimension", "Weight", "Accessory"
        ]

        data_rows = []
        current_category = None
        skip_next = False

        for i in range(len(lines)):
            if skip_next:
                skip_next = False
                continue

            line = lines[i].strip()
            if not line:
                continue

            if line in adjusted_category_headers:
                current_category = line
                continue

            spec_name = line
            spec_value = ""

            if (i + 1 < len(lines)) and (lines[i+1].strip() not in adjusted_category_headers):
                spec_value = lines[i+1].strip()
                skip_next = True

            data_rows.append({"Category": current_category, "Specification": spec_name, "Value": spec_value})

        df = pd.DataFrame(data_rows)
        df_cleaned = df[~df['Category'].isin(['สเปค', 'ย่อ'])].copy()

        df_cleaned.loc[df_cleaned['Category'] == 'ภาพรวม', 'Category'] = 'Overall Summary'
        df_cleaned.loc[(df_cleaned['Category'] == 'Overall Summary') & (df_cleaned['Specification'] == 'Refresh Rate'), 'Specification'] = 'Overall Refresh Rate'
        df_cleaned.loc[(df_cleaned['Category'] == 'Overall Summary') & (df_cleaned['Specification'] == 'Resolution'), 'Specification'] = 'Overall Resolution'
        df_cleaned.loc[(df_cleaned['Category'] == 'Overall Summary') & (df_cleaned['Specification'] == 'Video'), 'Specification'] = 'Overall Video Processor'
        df_cleaned.loc[(df_cleaned['Category'] == 'Overall Summary') & (df_cleaned['Specification'] == 'Design'), 'Specification'] = 'Overall Design Style'
        df_cleaned.loc[(df_cleaned['Category'] == 'Overall Summary') & (df_cleaned['Specification'] == 'Product Type'), 'Specification'] = 'Overall Product Type'

        df_cleaned = df_cleaned[df_cleaned['Category'] != 'Overall Summary']
        df_cleaned = df_cleaned.reset_index(drop=True)

        order = [
            "Display", "Video", "Audio", "Smart Service", "Smart Feature",
            "Game Feature", "Tuner/Broadcasting", "Connectivity",
            "Design", "Additional Feature", "Accessibility",
            "Power & Eco Solution", "Dimension", "Weight", "Accessory"
        ]
        df_cleaned['Category'] = pd.Categorical(df_cleaned['Category'], categories=order, ordered=True)
        df_cleaned = df_cleaned.sort_values(['Category', 'Specification'])

        html_head = """
        <html lang="th">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Samsung TV Spec</title>
        <style>
        ul li {
        font-size: 1.5rem;
        }
        body {
        font-family: sans-serif;
        margin: 0;
        padding: 1rem;
        background: #f8f8f8;
        color: #333;
        }
        .container {
        background: #fff;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        font-size: 1.2rem;
        }
        h1 {
        font-size: 2rem;
        margin-bottom: 1rem;
        }
        h3 {
        font-size: 1.6rem;
        margin: 1.5rem 0 0.5rem;
        color: #222;
        }
        table.spec-table {
        width: 100%;
        margin-bottom: 1.2rem;
        font-size: 1.5rem;
        }
        table.spec-table td, table.spec-table th {
        padding: 0.8rem 1rem;
        border-bottom: 1px solid #eee;
        }
        table.spec-table th {
        background-color: #f0f0f0;
        }
        table.spec-table td:first-child {
        font-weight: bold;
        color: #555;
        width: 45%;
        }
        </style>
        </head>
        <body>
        <div class="container">
        """

        summary_list_items = []
        if 'Operating System' in df_cleaned['Specification'].values:
            summary_list_items.append(
                f"<li>ระบบปฏิบัติการ  {df_cleaned[df_cleaned['Specification'] == 'Operating System']['Value'].iloc[0]}</li>"
            )
        if 'HDMI' in df_cleaned['Specification'].values:
            summary_list_items.append(
                f"<li>การเชื่อมต่อ HDMI  {df_cleaned[df_cleaned['Specification'] == 'HDMI']['Value'].iloc[0]} ช่อง</li>"
            )
        if 'Screen Size' in df_cleaned['Specification'].values:
            summary_list_items.append(
                f"<li>ขนาดหน้าจอ  {df_cleaned[df_cleaned['Specification'] == 'Screen Size']['Value'].iloc[0]}</li>"
            )
        if 'Product Type' in df_cleaned['Specification'].values:
            summary_list_items.append(
                f"<li>ประเภทผลิตภัณฑ์  {df_cleaned[df_cleaned['Specification'] == 'Product Type']['Value'].iloc[0]}</li>"
            )

        html_body_content = f"<h3>Title</h3>\n"
        if summary_list_items:
            html_body_content += "<ul>\n" + "\n".join(summary_list_items) + "\n</ul>\n"

        grouped_data = df_cleaned.groupby('Category')
        for category_name, group in grouped_data:
            html_body_content += f"<h3>{category_name}</h3>\n"
            html_body_content += """<table class="spec-table">"""
            for _, row in group.iterrows():
                spec = row['Specification']
                value = row['Value']
                display_value = value if value else "-"
                html_body_content += f"<tr><th>{spec}</th><td>{display_value}</td></tr>\n"
            html_body_content += "</table>\n"

        html_footer = "</div></body></html>"
        full_html_content = html_head + html_body_content + html_footer

# ============================================================================
with col2:
    
    st.text("HTML Code")
    # Show full HTML content in a scrollable text area
    st.text_area(
        label="Copy this HTML",
        value=full_html_content,
        height=200,
        # label_visibility="collapsed"
        )
    # Download button
    st.download_button(
        label="📥 Download HTML",
        data=full_html_content.encode("utf-8"),
        file_name="tv_spec.text",
        mime="text"
    )

# Show HTML preview
st.subheader("📄 Generated HTML Preview")
st.components.v1.html(full_html_content, height=800, scrolling=True)

        
