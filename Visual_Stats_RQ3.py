import pandas as pd
import re
from collections import Counter

# =====================================================================
# 1. ΦΟΡΤΩΣΗ ΚΑΙ ΠΡΟΕΤΟΙΜΑΣΙΑ ΔΕΔΟΜΕΝΩΝ
# =====================================================================
file_path = "scopus_data_BioASQ_Core.csv"
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Το αρχείο '{file_path}' δεν βρέθηκε.")
    exit()

if 'Affiliations' not in df.columns:
    print("Δεν βρέθηκε στήλη 'Affiliations' στο CSV.")
    exit()

all_affiliations = []
for row in df['Affiliations'].dropna():
    parts = str(row).split(';')
    for p in parts:
        p = p.strip()
        if p:
            all_affiliations.append(p)


# =====================================================================
# 2. ΑΠΟΛΥΤΑ ΕΞΕΙΔΙΚΕΥΜΕΝΗ ΓΕΩΓΡΑΦΙΚΗ ΚΑΤΑΝΟΜΗ (Εμπλουτισμένη)
# =====================================================================
country_keywords = {
    "USA": [
        "usa", "united states", "california", "massachusetts", "stanford", "harvard",
        "yale", "stony brook", "virginia", "amherst", "ncbi", "kentucky", "oregon",
        "chan zuckerberg", "columbia", "colorado", "texas", "mit", "boston", "johns hopkins",
        "nlm", "salesforce", "nih", "delaware", "tickle college", "college of engineering & mines",
        "michigan", "purdue", "cornell", "pennsylvania", "chicago", "ibm", "microsoft", "google",
        "amazon", "rutgers", "wisconsin", "maryland", "illinois", "georgia", "carnegie mellon",
        "washington", "brown", "princeton", "oak ridge", "siebel school", "keo world",
        "aquinas international academy", "arizona state", "astrazeneca pharmaceuticals lp",
        "cleveland clinic", "duke", "jupiter intelligence", "manning college", "mayo clinic",
        "northwell health", "northwestern", "originai", "san jose state", "pigman college",
        "north carolina at charlotte", "houston", "vagelos college", "walmart labs", "zero to deep learning",
        "item national lab", "emory", "appcubic", "tphs"
    ],
    "Russia": [
        "russia", "kazan", "skolkovo", "moscow", "sber", "lomonosov", "saint petersburg",
        "hse university", "higher school of economics", "skoltech", "itmo"
    ],
    "Greece": [
        "greece", "athens", "demokritos", "atypon", "hellas", "aristotle", "thessaloniki",
        "aegean", "ntua", "ionian", "crete", "patras", "archimedes", "institute for language and speech processing",
        "athena rc", "athena research", "alexander fleming", "hellenic mediterranean",
        "hellenic naval", "institute of informatics & telecommunications", "siliconblast", "ioannina"
    ],
    "China": [
        "china", "chinese", "beijing", "fudan", "shanghai", "tsinghua", "zhejiang",
        "xi'an", "jiaotong", "shenzhen", "guangzhou", "sichuan", "southeast university",
        "dalian", "wuhan", "nanjing", "harbin", "tianjin", "minjiang", "shanxi", "chengdu",
        "alibaba", "beihang", "central south university", "huawei noah", "ping an technology",
        "northwestern polytechnical", "university of international business and economics", "zhongyuan",
        "hong kong", "teaching and resaerch department of university governance"
    ],
    "UK": [
        "uk", "united kingdom", "london", "edinburgh", "exeter", "cambridge", "oxford",
        "bristol", "manchester", "sheffield", "glasgow", "nhs", "ucl", "kcl", "imperial college",
        "warwick", "birmingham", "leeds", "southampton", "nottingham", "durham", "lancaster",
        "moorfields", "astrazeneca", "better", "metadvice", "ochre bio", "robert gordon", "rowett institute",
        "ulster", "liverpool"
    ],
    "Germany": [
        "germany", "münchen", "munich", "berlin", "bielefeld", "jena", "hasso-plattner",
        "regensburg", "karlsruhe", "leipzig", "tübingen", "bonn", "darmstadt", "dfki",
        "transinsight", "gmbh", "max planck", "fraunhofer", "rwth", "universität",
        "siemens healthineers", "zb med"
    ],
    "France": [
        "france", "paris", "grenoble", "toulouse", "lyon", "sorbonne", "marseille",
        "bordeaux", "artois", "montpellier", "strasbourg", "nantes", "cnrs", "inria",
        "alès", "agap", "numérique", "cnam", "inrae", "viseo", "université", "école", "liris",
        "laboratoire d'informatique en image et systèmes d'information", "multimedia, information systems and advanced computing laboratory"
    ],
    "Spain": [
        "spain", "españa", "barcelona", "madrid", "terrassa", "supercomputación",
        "vigo", "valencia", "seville", "ht medica", "artificial intelligence research institute",
        "iiia", "ciencias de la salud", "coruña", "carlos iii", "sabadell", "universitat",
        "hospital universitari", "instituto", "educacion a distancia", "granada", "jaén"
    ],
    "Italy": [
        "italy", "italia", "pisa", "roma", "padova", "milano", "torino", "bologna", "napoli",
        "reveal srl", "translated srl", "srl", "politecnico", "università", "agostino gemelli"
    ],
    "Switzerland": [
        "switzerland", "zürich", "zurich", "lausanne", "epfl", "eth", "geneva",
        "hoffmann-la roche", "idsia dalle molle", "novartis"
    ],
    "Japan": ["japan", "tokyo", "kyoto", "osaka", "nippon", "hokkaido", "tohoku", "nagoya"],
    "Canada": [
        "canada", "montréal", "montreal", "toronto", "mcgill", "british columbia",
        "waterloo", "alberta", "mcmaster", "ottawa", "calgary", "concordia", "dalhousie"
    ],
    "Australia": [
        "australia", "macquarie", "sydney", "melbourne", "csiro", "brisbane",
        "queensland", "commonwealth scientific", "charles sturt", "australian national university", "victoria university"
    ],
    "South Korea": [
        "korea", "seoul", "kaist", "yonsei", "postech", "aigen sciences", "hyundai", "kangwon", "samsung"
    ],
    "India": [
        "india", "delhi", "mumbai", "bangalore", "hyderabad", "chennai", "madras",
        "dhirubhai ambani", "indira gandhi", "amrita vishwa", "jadavpur", "kancheepuram",
        "netaji subhas", "pimpri chinchwad", "visvesvaraya", "galgotias", "maharaja agrasen"
    ],
    "Singapore": [
        "singapore", "nus", "ntu", "nanyang technological", "national university hospital",
        "tan tock seng", "school of chemistry, chemical engineering and biotechnology"
    ],
    "Bulgaria": [
        "bulgaria", "sofia", "institute of information and communication technologies, bulgarian academy of sciences",
        "st. naum", "ontotext"
    ],
    "Portugal": [
        "portugal", "lisboa", "porto", "aveiro", "minho", "águeda", "priberam", "évora"
    ],
    "Colombia": ["colombia", "nacional de colombia", "tecnológica de bolívar"],
    "Turkey": ["turkey", "ankara", "yildirim beyazit", "boğaziçi", "bogazici"],
    "Romania": ["romania", "academia româna", "brașov", "brasov"],
    "Pakistan": ["pakistan", "lahore"],
    "Taiwan": ["taiwan", "academia sinica", "taipei", "national central university"],
    "Belgium": ["belgium", "ku leuven"],
    "Israel": ["israel", "bar-ilan"],
    "Poland": ["poland", "evidence prime"],
    "Norway": ["norway", "forskningsparken"],
    "Algeria": ["algeria", "école militaire polytechnique", "centre de recherche sur l'information scientifique et technique"],
    "Brazil": ["brazil", "ciências da saúde", "centro latino-americano"],
    "Czech Republic": ["czech", "prague", "jetbrains research"],
    "Bangladesh": ["bangladesh", "dhaka", "united international university", "daffodil"],
    "Tunisia": ["tunisia", "sfax", "tunis", "ecole nationale des sciences de l'informatique"],
    "Morocco": ["morocco", "oujda", "mohammed premier", "sidi mohamed", "kénitra"],
    "Netherlands": ["netherlands", "amsterdam", "delft", "elsevier", "leiden", "utrecht", "eindhoven"],
    "Sweden": ["sweden", "stockholm", "lund", "uppsala", "kth"],
    "Ireland": ["ireland", "dublin", "trinity college", "galway"],
    "Denmark": ["denmark", "novo nordisk", "copenhagen", "aarhus"],
    "Lithuania": ["lithuania", "lietuvos"],
}
# Λίστα για το Table 1 (Αναλυτική Χαρτογράφηση)
mapping_data = []
country_counts = Counter()
mapped_affiliations_count = 0

for inst in all_affiliations:
    inst_lower = inst.lower()
    matched_country = "Unmapped (Not Found)"

    for country, keywords in country_keywords.items():
        if any(re.search(rf'\b{re.escape(kw)}\b', inst_lower) for kw in keywords):
            matched_country = country
            break

    mapping_data.append({
        "Affiliation": inst,
        "Mapped_Country": matched_country
    })

    if matched_country != "Unmapped (Not Found)":
        country_counts[matched_country] += 1
        mapped_affiliations_count += 1

# =====================================================================
# 3. ΔΗΜΙΟΥΡΓΙΑ ΚΑΙ ΕΞΑΓΩΓΗ ΠΙΝΑΚΩΝ (DATAFRAMES)
# =====================================================================

# --- Πίνακας 1: Affiliations & Countries ---
df_mapping = pd.DataFrame(mapping_data)
# Ταξινομούμε τον πίνακα αλφαβητικά ανά χώρα για να διαβάζεται εύκολα
df_mapping.sort_values(by=["Mapped_Country", "Affiliation"], inplace=True)
df_mapping.to_csv("Table_1_Affiliations_Mapping.csv", index=False, encoding='utf-8-sig')

# --- Πίνακας 2: Στατιστικά ανά Χώρα ---
stats_data = []
for country, count in country_counts.most_common():
    pct = (count / mapped_affiliations_count) * 100 if mapped_affiliations_count > 0 else 0
    stats_data.append({
        "Country": country,
        "Total_Mentions": count,
        "Percentage_of_Mapped (%)": round(pct, 2)
    })

df_stats = pd.DataFrame(stats_data)
df_stats.to_csv("Table_2_Country_Statistics.csv", index=False, encoding='utf-8-sig')

print(" ΕΠΙΤΥΧΙΑ! Δημιουργήθηκαν δύο αρχεία CSV:")
print("  1. 'Table_1_Affiliations_Mapping.csv' (Λίστα με όλα τα affiliations και τη χώρα τους)")
print("  2. 'Table_2_Country_Statistics.csv' (Συγκεντρωτικός πίνακας με τα νούμερα ανά χώρα)")