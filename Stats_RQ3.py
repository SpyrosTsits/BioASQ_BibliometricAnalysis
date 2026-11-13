import pandas as pd
from collections import Counter

# 1. Φόρτωση Δεδομένων
file_path = "scopus_data_BioASQ_Core.csv"
df = pd.read_csv(file_path)

affil_series = df['Affiliations'].dropna()

all_affiliations = []
for row in affil_series:
    parts = str(row).split(';')
    for p in parts:
        p = p.strip()
        if p:
            all_affiliations.append(p)

unique_institutions = list(set(all_affiliations))
total_unique = len(unique_institutions)

# 2. Λίστα Top 100 Πανεπιστημίων με Έξυπνα Aliases (Λεξικό)
official_top_100_dict = {
    "Massachusetts Institute of Technology (MIT)": ["massachusetts institute of technology", "mit"],
    "Imperial College London": ["imperial college london", "imperial college"],
    "Stanford University": ["stanford university", "stanford"],
    "University of Oxford": ["university of oxford", "oxford university", "oxford"],
    "Harvard University": ["harvard university", "harvard"],
    "University of Cambridge": ["university of cambridge", "cambridge university", "cambridge"],
    "ETH Zurich": ["eth zurich", "eth zürich", "swiss federal institute of technology"],
    "National University of Singapore (NUS)": ["national university of singapore", "nus"],
    "UCL (University College London)": ["university college london", "ucl"],
    "California Institute of Technology (Caltech)": ["california institute of technology", "caltech"],
    "The University of Hong Kong": ["university of hong kong", "hku"],
    "Nanyang Technological University (NTU)": ["nanyang technological university", "nanyang technological", "ntu"],
    "University of Chicago": ["university of chicago", "uchicago"],
    "Peking University": ["peking university", "pku"],
    "University of Pennsylvania": ["university of pennsylvania", "upenn", "penn"],
    "Cornell University": ["cornell university", "cornell"],
    "Tsinghua University": ["tsinghua university", "tsinghua"],
    "University of California, Berkeley (UCB)": ["university of california berkeley",
                                                 "university of california, berkeley", "uc berkeley", "ucb",
                                                 "berkeley"],
    "The University of Melbourne": ["university of melbourne", "melbourne university"],
    "UNSW Sydney": ["university of new south wales", "unsw", "unsw sydney"],
    "Yale University": ["yale university", "yale"],
    "EPFL": ["epfl", "école polytechnique fédérale de lausanne", "ecole polytechnique federale de lausanne"],
    "Technical University of Munich": ["technical university of munich", "technische universität münchen", "tum"],
    "Johns Hopkins University": ["johns hopkins university", "johns hopkins", "jhu"],
    "University of Sydney": ["university of sydney", "sydney university", "usyd"],
    "Princeton University": ["princeton university", "princeton"],
    "McGill University": ["mcgill university", "mcgill"],
    "PSL Research University Paris": ["psl research university", "université psl", "universite psl"],
    "University of Toronto": ["university of toronto", "utoronto", "uoft"],
    "Fudan University": ["fudan university", "fudan"],
    "King's College London": ["king's college london", "kcl", "kings college london"],
    "Australian National University (ANU)": ["australian national university", "anu"],
    "Chinese University of Hong Kong": ["chinese university of hong kong", "cuhk"],
    "University of Edinburgh": ["university of edinburgh", "edinburgh university"],
    "University of Manchester": ["university of manchester", "manchester university"],
    "Monash University": ["monash university", "monash"],
    "The University of Tokyo": ["university of tokyo", "tokyo university", "utokyo"],
    "Seoul National University": ["seoul national university", "snu"],
    "Columbia University": ["columbia university", "columbia"],
    "University of British Columbia": ["university of british columbia", "ubc"],
    "Institut Polytechnique de Paris": ["institut polytechnique de paris", "ip paris"],
    "University of Queensland": ["university of queensland", "uq"],
    "Northwestern University": ["northwestern university", "northwestern"],
    "HKUST": ["hong kong university of science and technology", "hkust"],
    "University of Michigan-Ann Arbor": ["university of michigan", "umich", "michigan university"],
    "UCLA": ["university of california los angeles", "ucla"],
    "Shanghai Jiao Tong University": ["shanghai jiao tong university", "sjtu"],
    "Delft University of Technology": ["delft university of technology", "tu delft"],
    "Zhejiang University": ["zhejiang university", "zju"],
    "Yonsei University": ["yonsei university", "yonsei"],
    "University of Bristol": ["university of bristol", "bristol university"],
    "Carnegie Mellon University": ["carnegie mellon university", "carnegie mellon", "cmu"],
    "The University of Amsterdam": ["university of amsterdam", "uva"],
    "Hong Kong Polytechnic University": ["hong kong polytechnic university", "polyu"],
    "New York University (NYU)": ["new york university", "nyu"],
    "LSE": ["london school of economics", "lse"],
    "Kyoto University": ["kyoto university", "kyoto"],
    "Ludwig-Maximilians-Universität München": ["ludwig-maximilians-universität", "ludwig maximilians", "lmu munich"],
    "Universiti Malaya": ["universiti malaya", "university of malaya"],
    "KU Leuven": ["ku leuven", "katholieke universiteit leuven"],
    "Korea University": ["korea university"],
    "Duke University": ["duke university", "duke"],
    "City University of Hong Kong": ["city university of hong kong", "cityu"],
    "National Taiwan University (NTU)": ["national taiwan university"],
    "The University of Auckland": ["university of auckland"],
    "UC San Diego": ["university of california san diego", "ucsd", "uc san diego"],
    "King Fahd University": ["king fahd university", "kfupm"],
    "University of Texas at Austin": ["university of texas at austin", "ut austin"],
    "Brown University": ["brown university", "brown"],
    "UIUC": ["university of illinois at urbana-champaign", "uiuc", "university of illinois"],
    "Paris-Saclay University": ["paris-saclay", "paris saclay"],
    "Lund University": ["lund university", "lund"],
    "Sorbonne University": ["sorbonne university", "sorbonne"],
    "The University of Warwick": ["university of warwick", "warwick"],
    "Trinity College Dublin": ["trinity college dublin", "tcd"],
    "University of Birmingham": ["university of birmingham", "birmingham university"],
    "The University of Western Australia": ["university of western australia", "uwa"],
    "KTH Royal Institute of Technology": ["kth royal institute of technology", "kth"],
    "University of Glasgow": ["university of glasgow", "glasgow university"],
    "Universität Heidelberg": ["universität heidelberg", "heidelberg university", "university of heidelberg"],
    "University of Washington": ["university of washington", "uw", "uofw"],
    "The University of Adelaide": ["university of adelaide", "adelaide university"],
    "Pennsylvania State University": ["pennsylvania state university", "penn state", "psu"],
    "Universidad de Buenos Aires": ["universidad de buenos aires", "uba"],
    "Tokyo Institute of Technology": ["tokyo institute of technology", "tokyo tech"],
    "University of Leeds": ["university of leeds", "leeds university"],
    "University of Southampton": ["university of southampton", "southampton university"],
    "Boston University": ["boston university", "bu"],
    "Freie Universität Berlin": ["freie universität berlin", "free university of berlin"],
    "Purdue University": ["purdue university", "purdue"],
    "The University of Osaka": ["university of osaka", "osaka university"],
    "The University of Sheffield": ["university of sheffield", "sheffield university"],
    "Uppsala University": ["uppsala university"],
    "Durham University": ["durham university", "durham"],
    "University of Alberta": ["university of alberta", "ualberta"],
    "University of Technology Sydney": ["university of technology sydney", "uts"],
    "The University of Nottingham": ["university of nottingham", "nottingham university"],
    "Karlsruhe Institute of Technology (KIT)": ["karlsruhe institute of technology", "kit"],
    "Politecnico di Milano": ["politecnico di milano", "polimi"],
    "University of Zurich": ["university of zurich", "uzh"]
}

import re

top_100_count = 0
found_top_100_institutions = []

for inst in unique_institutions:
    inst_lower = inst.lower()
    matched = False

    # Ελέγχουμε κάθε πανεπιστήμιο και τις παραλλαγές του
    for official_name, aliases in official_top_100_dict.items():
        for alias in aliases:
            # Το \b εξασφαλίζει ότι θα βρει ολόκληρη τη λέξη (π.χ. το 'mit' δεν θα κάνει match το 'smith')
            if re.search(rf'\b{re.escape(alias)}\b', inst_lower):
                matched = True
                found_top_100_institutions.append(official_name)
                break  # Αν βρούμε ένα alias, σταματάμε να ελέγχουμε τα υπόλοιπα γι' αυτό το πανεπιστήμιο
        if matched:
            top_100_count += 1
            break  # Προχωράμε στο επόμενο μοναδικό ίδρυμα

percentage_top_100 = (top_100_count / total_unique) * 100 if total_unique > 0 else 0



# =====================================================================
# 3. ΑΠΟΛΥΤΑ ΕΞΕΙΔΙΚΕΥΜΕΝΗ ΓΕΩΓΡΑΦΙΚΗ ΚΑΤΑΝΟΜΗ (Βασισμένη στο BioASQ Core)
# =====================================================================
# Αυτό το λεξικό δημιουργήθηκε έπειτα από ανάλυση των "ωμών" (raw) ιδρυμάτων
# του αρχείου BioASQ_Core_Morfopoihmeno.xlsx. Περιλαμβάνει πόλεις, πανεπιστήμια,
# ερευνητικά κέντρα (π.χ. DFKI, NCBI) και εταιρείες (π.χ. Atypon, Salesforce).


# =====================================================================
# 2.  ΓΕΩΓΡΑΦΙΚΗ ΚΑΤΑΝΟΜΗ
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
        "item national lab"
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
        "northwestern polytechnical", "university of international business and economics", "zhongyuan"
    ],
    "UK": [
        "uk", "united kingdom", "london", "edinburgh", "exeter", "cambridge", "oxford",
        "bristol", "manchester", "sheffield", "glasgow", "nhs", "ucl", "kcl", "imperial college",
        "warwick", "birmingham", "leeds", "southampton", "nottingham", "durham", "lancaster",
        "moorfields", "astrazeneca", "better", "metadvice", "ochre bio", "robert gordon", "rowett institute", "ulster"
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
        "netaji subhas", "pimpri chinchwad", "visvesvaraya"
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

country_counts = Counter()
mapped_affiliations_count = 0
unmapped_institutions = []

for inst in all_affiliations:
    inst_lower = inst.lower()
    matched_country = None

    for country, keywords in country_keywords.items():
        if any(re.search(rf'\b{re.escape(kw)}\b', inst_lower) for kw in keywords):
            matched_country = country
            break

    if matched_country:
        country_counts[matched_country] += 1
        mapped_affiliations_count += 1
    else:
        unmapped_institutions.append(inst)

# =====================================================================
# 4. ΕΚΤΥΠΩΣΗ ΤΕΛΙΚΩΝ ΑΠΟΤΕΛΕΣΜΑΤΩΝ
# =====================================================================
print(f"--- ΣΤΑΤΙΣΤΙΚΑ ΣΥΜΜΕΤΟΧΩΝ (RQ3) ---")
print(f"Συνολικά Μοναδικά Ιδρύματα (έπειτα από split): {total_unique}")
print(f"Ιδρύματα στο Επίσημο Top 100: {top_100_count} (Ποσοστό επί των μοναδικών: {percentage_top_100:.1f}%)\n")

print("--- ΓΕΩΓΡΑΦΙΚΗ ΚΑΤΑΝΟΜΗ (Top 10 Χώρες) ---")
print(f"Επιτυχής ταυτοποίηση χώρας στο {(mapped_affiliations_count / len(all_affiliations)) * 100:.1f}% των δεδομένων.")
for country, count in country_counts.most_common(10):
    pct = (count / mapped_affiliations_count) * 100 if mapped_affiliations_count > 0 else 0
    print(f"- {country}: {count} αναφορές (Ποσοστό: {pct:.1f}%)")