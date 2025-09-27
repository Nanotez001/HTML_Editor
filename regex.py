import re
import pandas as pd

def extract_tv_details(sku_list):

#     sku_list = [
#     "OLED65G36PSA",
#     "QA98QN990FKXXT",
#     "65C835",
#     "UA55CU8000KXXT",
#     "TCL100P745"
# ]
    
    patterns = {
    # LG: 65QNED86ASA, 55NANO80TNA, 75OLED77TNA, 50LED80TNA, 43UQ8000PSA
    "LG": r"^(\d{2,3})?(OLED|NANO|QNED|LED|UQ|UT|UR)([A-Z0-9]+)$",

    # Samsung: 75Q80A, 50AU8000KXXT, 65S95CAKXXT, 65U8HQ, 100U9GQ
    # - QLED: QxxA, QNxx
    # - Crystal UHD: AUxxxx, CUxxxx, BUxxxx
    # - OLED: S95C
    # - U/E/A models: U8HQ, U7KQ, A7H, E7H, U9GQ
    "Samsung": r"^(?:QA|UA)?(\d{2,3})(QN|Q|AU|CU|BU|S|U|E|A)([A-Z0-9]+)(?:KXXT)$",

    # TCL: 43P615, 32C635, 65C835, 100C955
    "TCL": r"^(\d{2,3})([CPS])(\d{3,4})$",

    # Sony: XR65A80K, KD55X80K, XR75X95L, KD43X77L
    "Sony": r"^(XR|KD)(\d{2,3})([A-Z0-9]+)$",

    # Hisense: 65U8HQ, 55U7KQ, 50A7H, 75E7H, 100U9GQ
    "Hisense": r"^(\d{2,3})(U|A|E)([A-Z0-9]+)$",

    # Panasonic: TH65JX750T, TH55LX650T, TH43MX800T, TH77LZ2000T
    "Panasonic": r"^TH(\d{2,3})([A-Z]+)([0-9]+[A-Z]?)$",
}


    results = []
    for sku_input in sku_list:
        matched = False
        for brand, pattern in patterns.items():
            match = re.search(pattern, sku_input)
            if match:
                matched = True
                row = {"SKU": sku_input, "Brand": brand, "Size": None, "Type": None, "Model Code": None}

                if brand == "LG":
                    row["Size"] = match.group(1)
                    row["Type"] = match.group(2)
                    if match.lastindex and match.lastindex >= 3 and match.group(3):
                        row["Model Code"] = match.group(3)

                elif brand == "Samsung":
                    row["Size"] = match.group(2)
                    row["Type"] = type_samsung_check(match.group(3))
                    if match.lastindex and match.lastindex >= 3 and match.group(3):
                        row["Model Code"] = match.group(3)

                elif brand == "TCL":
                    row["Size"] = match.group(1)
                    row["Model Code"] = match.group(2)
                    row["Type"] = None

                row["Year"] = None  # Placeholder for future use
                results.append(row)
                break

        if not matched:
            results.append({"SKU": sku_input, "Brand": None, "Size": None, "Type": None, "Model Code": None})

    df = pd.DataFrame(results)
    return df

def type_samsung_check(model_code):
    if model_code.startswith(("C","AU")):
        return "Crystal UHD"
    elif model_code.startswith("Q"):
        return "QLED"
    elif model_code.startswith("QN"):
        return "Neo QLED"
    elif model_code.startswith("H"):
        return "HD"
    elif model_code.startswith("S"):
        return "OLED"
    else:
        return None

def check_extract():
    sku = [
    # 🔹 LG
    "65QNED86ASA", "55NANO80TNA", "75OLED77TNA", "50LED80TNA",
    "86QNED99PSA", "48OLEDC26PSA", "43UQ8000PSA", "55QNED75UQA",

    # 🔹 Samsung
    "75Q80A", "65Q70A", "55Q60A", 
    "50AU8000KXXT", "85QN90CAKXXT", "98QN990FKXXT", "43CU7000KXXT",
    "65S95CAKXXT",   # Samsung OLED
    "55BU8500KXXT",  # Budget UHD

    # 🔹 TCL
    "43P615", "32C635", "65C835", "75P745", "55S5400", "100C955",

    # 🔹 Sony
    "XR65A80K", "KD55X80K", "XR75X95L", "KD43X77L",

    # 🔹 Hisense
    "65U8HQ", "55U7KQ", "50A7H", "75E7H", "100U9GQ",

    # 🔹 Panasonic
    "TH65JX750T", "TH55LX650T", "TH43MX800T", "TH77LZ2000T"
]

    df = extract_tv_details(sku)
    print(df)
if __name__ == "__main__":
    check_extract()
