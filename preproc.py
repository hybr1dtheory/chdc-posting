import pandas as pd
from dbmanage import DBManager


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
    "щ": "shch", "ь": "", "ю": "iu", "я": "ia",
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
    if "guided aerial bomb" in narrative:
        return "Airstrike"
    elif "missile" in narrative:
        return "Rockets & Missiles"
    elif "loitering munition" in narrative:
        return "Long Range Attack"
    elif "short-range combat UAV" in narrative:
        return "Short Range Attack"
    elif "MLRS" in narrative:
        return "Rockets & Missiles"
    elif "round" in narrative:
        return "Artillery"
    return ""


def process_raw_data(
    raw_df: pd.DataFrame, obl_tr: dict | None = None,
    rai_tr: dict | None = None, hrom_tr: dict | None = None
) -> pd.DataFrame:
    data = []
    for i, r in raw_df.iterrows():
        text = r["Narrative"]
        actor1 = parse_actor(text)
        act = parse_act(text)
        if obl_tr:
            oblast = obl_tr.get(r["Oblast"].replace(" область", ""), "")
        else:
            oblast = r["Oblast"].replace(" область", "")
        if rai_tr:
            raion = rai_tr.get(r["Raion"].replace(" район", ""), "")
        else:
            raion = r["Raion"].replace(" район", "")
        if hrom_tr:
            hromada = hrom_tr.get(r["Hromada"].replace(" громада", ""), "")
        else:
            hromada = r["Hromada"].replace(" громада", "")
        settl = transliterate(r["Settlement"])
        incident = {
            "Date": r["Date"],
            "Time": None,
            "Oblast": oblast,
            "Raion": raion,
            "Hromada": hromada,
            "Settlement": settl,
            "Narrative": text,
            "Location type": "International Border",
            "Actor 1": actor1,
            "Actor 2": "Ukrainian Army",
            "Act": act
        }
        data.append(incident)

    return pd.DataFrame(data)


raw_df = pd.read_excel("raw_data.xlsx")
# obl_trans: dict
# rai_trans: dict
# hrom_trans: dict
dbman = DBManager("regions.db")
obl_trans = dbman.get_translit_dict("oblast")
rai_trans = dbman.get_translit_dict("raion")
hrom_trans = dbman.get_translit_dict("hromada")

res = process_raw_data(raw_df, obl_trans, rai_trans, hrom_trans)
res.to_excel("test.xlsx", sheet_name="Sheet1")
    