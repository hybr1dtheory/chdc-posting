import pandas as pd
from dbmanage import DBManager


# Dcicts for transliteration
UPDICT = {
    "А": "A", "Б": "B", "В": "V", "Г": "H", "Ґ": "G",
    "Д": "D", "Е": "E", "Є": "Ye", "Ж": "Zh", "З": "Z",
    "И": "Y", "І": "I", "Ї": "Yi", "Й": "Y", "К": "K",
    "Л": "L", "М": "M", "Н": "N", "О": "O", "П": "P",
    "Р": "R", "С": "S", "Т": "T", "У": "U", "Ф": "F",
    "Х": "Kh", "Ц": "Ts", "Ч": "Ch", "Ш": "Sh", "Щ": "Shch",
    "Ь": "", "Ю": "Yu", "Я": "Ya",
}

LOWDICT = {
    "'": "", "а": "a", "б": "b", "в": "v", "г": "h",
    "ґ": "g", "д": "d", "е": "e", "є": "ie", "ж": "zh",
    "з": "z", "и": "y", "і": "i", "ї": "i", "й": "i",
    "к": "k", "л": "l", "м": "m", "н": "n", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh",
    "щ": "shch", "ь": "", "ю": "iu", "я": "ia", "’": ""
}

EXCEPTDICT = {"Зг": "Zgh", "зг": "zgh"}


def transliterate(name: str) -> str:
    """Function for transliteration of Ukrainian names in accordance with 
    the “Rules for spelling Ukrainian geographical names” 
    (Order №282 of the Ministry of Agrarian Policy)"""
    name = name.strip()
    res = ""
    for k, v in EXCEPTDICT.items():
        if k in name:
            name.replace(k, v)
    for s in name:
        if s in UPDICT:
            res += UPDICT[s]
        elif s in LOWDICT:
            res += LOWDICT[s]
        else:
            res += s
    return res


def parse_actor(narrative: str) -> str:
    if narrative.startswith("RA "):
        return "Russian Army"
    elif narrative.startswith("RuAF "):
        return "Russian Airforce"
    return ""


def parse_act(narrative: str) -> str:
    if "guided aerial bomb" in narrative or "airstrike" in narrative:
        return "Airstrike"
    elif "missile" in narrative:
        return "Rockets & Missiles"
    elif "loitering munition" in narrative:
        return "Long Range Attack"
    elif "short-range combat UAV" in narrative:
        return "Short Range Attack"
    elif "MLRS" in narrative:
        if "mortar" in narrative or "artillery" in narrative:
            return "Artillery/Other"
        return "Rockets & Missiles"
    elif "grenade launcher" in narrative:
        return "Light Weapons"
    elif "round" in narrative:
        return "Artillery"
    elif "tank cannon" in narrative:
        return "Fighting Vehicle"
    elif "helicopter" in narrative:
        return "Helicopter"
    return ""


def process_incident(
    inc: pd.Series, obl_tr: dict | None = None,
    rai_tr: dict | None = None, hrom_tr: dict | None = None
) -> dict:
    """Function to process and transform raw incident data.
    inc - pandas.Series or dict-like object with the incident data.
    obl_tr, rai_tr, hrom_tr - dicts with transliteration ukr -> eng.
    Returns a dict with data prepared for uploading."""
    text = inc["Narrative"].strip()
    while "  " in text:
        text.replace("  ", " ")
    actor1 = parse_actor(text)
    act = parse_act(text)
    if obl_tr:
        oblast = obl_tr.get(inc["Oblast"].replace(" область", ""), "")
    else:
        oblast = inc["Oblast"].replace(" область", "")
    if rai_tr:
        raion = rai_tr.get(inc["Raion"].replace(" район", ""), "")
    else:
        raion = inc["Raion"].replace(" район", "")
    if hrom_tr:
        hromada = hrom_tr.get(inc["Hromada"].replace(" громада", ""), "")
    else:
        hromada = inc["Hromada"].replace(" громада", "")
    settl = transliterate(inc["Settlement"])
    incident = {
        "Date": inc["Date"], "Time": inc.get("Time", None),
        "Oblast": oblast, "Raion": raion, "Hromada": hromada,
        "Settlement": settl, "Narrative": text,
        "Location type": "International Border", "Actor 1": actor1,
        "Actor 2": "Ukrainian Army", "Act": act, "WARNINGS": "",
    }
    return incident


def process_raw_data(data_path: str, db_path: str) -> pd.DataFrame:
    """Function reads data from xls file at <data_path>,
    process and transform it row-by-row.
    Returns pandas.DataFrame object with processed data."""
    raw_df = pd.read_excel(data_path)
    dbman = DBManager(db_path)
    valid_set = dbman.get_locations_set()
    obl_trans = dbman.get_translit_dict("oblast")
    rai_trans = dbman.get_translit_dict("raion")
    hrom_trans = dbman.get_translit_dict("hromada")
    data = []
    for i, row in raw_df.iterrows():
        incident = process_incident(
            row, obl_trans, rai_trans, hrom_trans
        )
        loc_row = (
            row["Oblast"].replace(" область", ""),
            row["Raion"].replace(" район", ""),
            row["Hromada"].replace(" громада", ""),
            row["Settlement"]
        )
        if loc_row not in valid_set:
            incident["WARNINGS"] = "Location error"
        data.append(incident)
    return pd.DataFrame(data)


if __name__ == "__main__":
    res = process_raw_data("raw_data.xlsx", "regions.db")
    res.to_excel("test.xlsx", sheet_name="Sheet1")
