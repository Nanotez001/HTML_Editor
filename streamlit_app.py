import streamlit as st
import pandas as pd
import re


# Sidebar
# st.sidebar.selectbox(label= "Platform",options = ["LG","Samsung"])
#===========================================================================

st.title("HTML Generator V.1.10")

full_html_content=""

col1, col2 = st.columns(2)
with col1:
    text = st.text_area("Text Here", height=200)
    if st.button("Generate HTML"):
        if not text.strip():
            st.warning("กรุณาใส่ข้อมูลสเปคก่อน")
            st.stop()
    # ============================================================================
        # Cut all Line & Clear Space
        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
        adjusted_category_headers = [
            "ภาพรวม","Product Type","Display","Video","Audio", "Smart Service",
            "Smart Feature", "Game Feature", "Tuner/Broadcasting", "Connectivity",
            "Design", "Additional Feature", "Accessibility", "Power & Eco Solution",
            "Dimension", "Weight", "Accessory"
        ]
        # Del Exceptional Text
        del_line = ["สเปค","ย่อ"]
        lines = [line for line in lines if line not in del_line]

        # Fill in DF
        data_rows = []
        i = 0
        current_category = None
        header_queue = adjusted_category_headers.copy()
        while i < len(lines):
            line = lines[i].strip()

            # Check if this line is the next expected category
            if header_queue and line == header_queue[0]:
                current_category = header_queue.pop(0)
                i += 1
                continue

            spec_name = line
            spec_value = ""

            # If next line exists and is not the next header
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if not (header_queue and next_line == header_queue[0]):
                    spec_value = next_line
                    i += 1  # skip next line

            data_rows.append({
                "Category": current_category,
                "Specification": spec_name,
                "Value": spec_value
            })
            i += 1
        df = pd.DataFrame(data_rows)

        # Change Name
        df.loc[df['Category'] == 'ภาพรวม', 'Category'] = 'Overall'
        
        # Fill empty slot
        mask = df['Value'].isnull() | (df['Value'].astype(str).str.strip() == "")

        df.loc[mask, 'Value'] = df.loc[mask, 'Specification']
        df.loc[mask, 'Specification'] = df.loc[mask, 'Category']
        # ===========================================================================
        # HTML Head
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

        # ===========================================================================
        # Spec Intro
        operating_system =  df[df['Specification'] == 'Operating System']['Value'].iloc[0]
        hdmi = df[df['Specification'] == 'HDMI']['Value'].iloc[0]
        screen_size = df[df['Specification'] == 'Screen Size']['Value'].iloc[0]
        product_type = df[df['Specification'] == 'Product Type']['Value'].iloc[0]
        processor = df[df['Specification'] == 'Video']['Value'].iloc[0]

        summary_list_items = []
        if 'Operating System' in df['Specification'].values:
            summary_list_items.append(
                f"<li>ระบบปฏิบัติการ  {operating_system}</li>"
            )
        if 'Video' in df['Specification'].values:
            summary_list_items.append(
                f"<li>ชิปประมวลผล {processor} </li>"
            )
        if 'HDMI' in df['Specification'].values:
            summary_list_items.append(
                f"<li>การเชื่อมต่อ HDMI x {hdmi}</li>"
            )
        # if 'Screen Size' in df['Specification'].values:
        #     summary_list_items.append(
        #         f"<li>ขนาดหน้าจอ  {screen_size}</li>"
        #     )
        if 'Product Type' in df['Specification'].values:
            summary_list_items.append(
                f"<li> {product_type} Panel</li>"
            )

        # ===========================================================================
        # HTML Body
        html_body_content = f"<h3> [Title] </h3>\n"
        if summary_list_items:
            html_body_content += "<ul>\n" + "\n".join(summary_list_items) + "\n</ul>\n"

        grouped_data = df.groupby('Category', sort=False)

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
    # Show full HTML content in a scrollable text area
    st.text_area(
        label="Copy this HTML (ต้องเปลี่ยน Title ภายหลัง)",
        value=full_html_content,
        height=200,
        # label_visibility="collapsed"
        )
    # Download button
    st.download_button(
        label="📥 Download .TEXT",
        data=full_html_content.encode("utf-8"),
        file_name="tv_spec.text",
        mime="text"
    )

# Show HTML preview
st.subheader("HTML Preview (ใช้ดูคร่าวๆเท่านั้น)")
st.components.v1.html(full_html_content, height=800, scrolling=True)

        
