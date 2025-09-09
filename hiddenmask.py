from html import escape

def generate_h_text(platform: str) -> str:
    if platform == "All":
        texts = """
            LG,SAMSUNG,TV,Luckydigital,LD,ลัคกี้ดิจิตอล,ลัคกี้,Waaa, got me!
            """
    elif platform == "JJT":
        texts = """
            LG Smart TV 2025,LG OLED TV 2025,LG QLED TV 2025,LG TV 2025,สมาร์ททีวี LG,LG,SAMSUNG,TV,Jingjungto,JJT,จริงจังโต,จริงจัง,Waaa, got me!
            """
        
    # Use a color close to background (white) and small font
    style = "font-size:8px;color:#f9f9f9;"
    h_html = ''.join(
        f'<span style="{style}">{escape(texts)}</span>'
    )
    return h_html
    

