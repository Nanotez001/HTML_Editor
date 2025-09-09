import streamlit as st
import pandas as pd
import A001_html_temp 
import A002_html_temp
import category_headers
import hiddenmask

# Sidebar
st.set_page_config(
    page_title="HTML Generator",                
    layout="wide"
)
#===========================================================================

st.title("HTML Generator V.1.35")
input_platform = st.sidebar.selectbox(label="Source", options=["LG", "Samsung"])
output_platform = st.sidebar.selectbox(label="Platform", options=["All", "JJT"])
h_text = st.sidebar.checkbox("Hidden Text",value=True)
#===========================================================================


full_html_content=""

# Header
col1, col2 = st.columns(2)
with col1:
    # header_text = st.text_input("Header")
    pass
with col2:
    pass
# Subheader
col1, col2 = st.columns(2)
with col1:
    pass
with col2:
    pass
# Details
col1, col2, col3 = st.columns(3)
with col1:
    text = st.text_area("Text Here", height=200)

    if st.button("Generate HTML"):
        if not text.strip():
            st.warning("กรุณาใส่ข้อมูลสเปคก่อน")
            st.stop()
    # ============================================================================
        # Cut all Line & Clear Space
        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
        if input_platform == "Samsung":
            adjusted_category_headers = category_headers.SAMSUNG_adjusted_category_headers
        elif input_platform == "LG":
            adjusted_category_headers = category_headers.LG_adjusted_category_headers
        else:
            st.error("Platform not supported")
            st.stop()
            
        # Del Exceptional Text
        if input_platform == "Samsung":
            del_line = ["สเปค","ย่อ","ปิด","สเปคทั้งหมด"]
        elif input_platform == "LG":
            del_line = ["ปิด","สเปคทั้งหมด"]#Fill it
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
        st.dataframe(df)
        # ===========================================================================
        # # Change Name
        # df.loc[df['Category'] == 'ภาพรวม', 'Category'] = 'Overall'
        
        # # Fill empty slot
        # mask = df['Value'].isnull() | (df['Value'].astype(str).str.strip() == "")

        # df.loc[mask, 'Value'] = df.loc[mask, 'Specification']
        # df.loc[mask, 'Specification'] = df.loc[mask, 'Category']
        # # ===========================================================================
        # # HTML Header
        # screen_size = df[df['Specification'] == 'Screen Size']['Value'].iloc[0].replace('"', '')
        # product_id = ""
        # header_lines = [x.strip() for x in re.split(r'[" ]{2,}|["]', header_text) if x.strip()]
        # if header_lines:
        #     product_id = header_lines[-1]
        #     product_description = " ".join(header_lines[1:-1])

        # output_header = f"{input_platform} {screen_size} นิ้ว รุ่น {product_id} {product_description}"
        # # ===========================================================================
        # HTML subbody
        if output_platform == "All":
            html_head = A001_html_temp.html_head
        elif output_platform == "JJT":
            # Use A002_html_temp for JJT platform
            html_head = A002_html_temp.html_head
        else:
            st.error("Platform not supported")
            st.stop()

        # # ===========================================================================
        # # Spec Intro
        # operating_system =  df[df['Specification'] == 'Operating System']['Value'].iloc[0]
        # hdmi = df[df['Specification'] == 'HDMI']['Value'].iloc[0]
        # screen_size = df[df['Specification'] == 'Screen Size']['Value'].iloc[0]
        # product_type = df[df['Specification'] == 'Product Type']['Value'].iloc[0]
        # processor = df[df['Specification'] == 'Video']['Value'].iloc[0]

        # summary_list_items = []
        # if 'Operating System' in df['Specification'].values:
        #     summary_list_items.append(
        #         f"<li>ระบบปฏิบัติการ  {operating_system}</li>"
        #     )
        # if 'Video' in df['Specification'].values:
        #     summary_list_items.append(
        #         f"<li>ชิปประมวลผล {processor} </li>"
        #     )
        # if 'HDMI' in df['Specification'].values:
        #     summary_list_items.append(
        #         f"<li>การเชื่อมต่อ HDMI x {hdmi}</li>"
        #     )
        # if 'Product Type' in df['Specification'].values:
        #     summary_list_items.append(
        #         f"<li> {product_type} Panel</li>"
        #     )

        # # ===========================================================================
        # # HTML Body
        html_body_content = ""
        # html_body_content = f"<h3> {output_header} </h3>\n"
        # html_body_content += f"<p> {product_id} </p>\n"
        # html_body_content += "<br>\n"
        # if summary_list_items:
        #     html_body_content += "<ul>\n" + "\n".join(summary_list_items) + "\n</ul>\n"
        #     html_body_content += "<br>\n"

        grouped_data = df.groupby('Category', sort=False)
        # Create tables
        for category_name, group in grouped_data:
            html_body_content += f"""<h3><span style="font-family: 'Noto Sans Thai';">{category_name}</span></h3>\n"""
            html_body_content += """<table class="spec-table">"""
            for _, row in group.iterrows():
                spec = row['Specification']
                value = row['Value']
                display_value = value if value else "-"
                html_body_content += f"""<tr><th><span style="font-family: 'Noto Sans Thai';">{spec}\
                    </span></th><td><span style="font-family: 'Noto Sans Thai';">{display_value}</span></td></tr>\n"""
            html_body_content += "</table>\n"

        # HTML footer
        if output_platform == "All":
            html_footer = A001_html_temp.html_footer
        elif output_platform == "JJT":
            html_footer = A002_html_temp.html_footer
        else:
            st.error("Platform not supported")
            st.stop()

        #Hidden Text
        if h_text:
            h_html = hiddenmask.generate_h_text(output_platform)
            html_body_content += h_html
        
        # Combine all parts
        full_html_content = html_head + html_body_content + html_footer

# ============================================================================
with col2:
    # Show full HTML content in a scrollable text area
    st.text_area(
        label="Copy this HTML ",
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
with col3:
    # Show HTML preview
    st.write("HTML Preview (ใช้ดูคร่าวๆเท่านั้น)")
    st.components.v1.html(full_html_content, height=800, scrolling=True)

        
