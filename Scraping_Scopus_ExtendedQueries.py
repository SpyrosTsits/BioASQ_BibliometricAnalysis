import requests
import pandas as pd
import time

# 1. Διαπιστευτήρια και ρυθμίσεις
API_KEY = ""
SEARCH_URL = 'https://api.elsevier.com/content/search/scopus'

headers = {
    'Accept': 'application/json',
    'X-ELS-APIKey': API_KEY
}

# 2. Τα Τελικά Διευρυμένα Queries (Χωρίς συντακτικά λάθη)
queries = {
    'Expanded_QA': 'TITLE-ABS-KEY ( ( biomedical OR medical OR clinical OR healthcare OR "life sciences" ) AND ( "question answering" OR "machine reading comprehension" OR chatbot OR "conversational agent" OR "RAG" ) ) AND NOT TITLE-ABS-KEY ( BioASQ )',

    'Expanded_SI': 'TITLE-ABS-KEY ( ( biomedical OR medical OR clinical OR healthcare OR "life sciences" ) AND ( "semantic indexing" OR "semantic annotation" OR "text mining" OR "information extraction" OR "named entity recognition" OR NER ) ) AND NOT TITLE-ABS-KEY ( BioASQ )'
}


# 3. Συνάρτηση που τραβάει τα δεδομένα με σελιδοποίηση και φίλτρο έτους
def fetch_scopus_data(query_string, year):
    all_results = []
    start_index = 0
    count = 25

    while True:
        params = {
            'query': query_string,
            'count': count,
            'start': start_index,
            'view': 'COMPLETE',
            'date': str(year)  # <--- Η ΣΩΣΤΗ ΛΥΣΗ: Το ενσωματωμένο φίλτρο του API!
        }

        try:
            response = requests.get(SEARCH_URL, headers=headers, params=params, timeout=30)
        except requests.exceptions.RequestException as e:
            print(f"  [Σφάλμα Δικτύου] Ξαναπροσπαθώ... ({e})")
            time.sleep(5)
            continue

        if response.status_code == 429:
            print("  [Rate Limit] Αναμονή 5 δευτερόλεπτα...")
            time.sleep(5)
            continue
        elif response.status_code != 200:
            print(f"  [Σφάλμα] Το API επέστρεψε κωδικό {response.status_code}")
            break

        data = response.json()
        search_results = data.get('search-results', {})
        entries = search_results.get('entry', [])

        if not entries:
            break

        all_results.extend(entries)
        total_results = int(search_results.get('opensearch:totalResults', 0))

        # Εκτύπωση προόδου
        print(f"    -> Φορτώθηκαν {min(start_index + count, total_results)} / {total_results} άρθρα...")

        start_index += count
        if start_index >= total_results:
            break

        time.sleep(0.3)

    return all_results


# 4. Η Κύρια Λούπα Εκτέλεσης (Year Slicing)
for name, base_q_string in queries.items():
    print(f"\n{'=' * 50}\n🚀 Ξεκινάει η λήψη για το σύνολο: {name}\n{'=' * 50}")
    all_years_results = []

    for year in range(2012, 2027):
        print(f"📅 Ανάκτηση δεδομένων για το έτος {year}...")

        # Περνάμε το αρχικό καθαρό query και τη χρονιά ξεχωριστά στη συνάρτηση!
        results = fetch_scopus_data(base_q_string, year)

        if results:
            all_years_results.extend(results)
            print(f"  ✓ Αποθηκεύτηκαν {len(results)} εγγραφές για το {year}.")
        else:
            print("  - Δεν βρέθηκαν εγγραφές.")

    # 5. Καθαρισμός και Αποθήκευση
    if all_years_results:
        print("\n⏳ Γίνεται καθαρισμός και μορφοποίηση...")
        cleaned_data = []
        for item in all_years_results:
            authors_data = item.get('author', [])
            author_names = [auth.get('authname') for auth in authors_data if
                            isinstance(auth, dict) and 'authname' in auth]
            final_authors = "; ".join(author_names) if author_names else item.get('dc:creator', 'Άγνωστος')

            cleaned_data.append({
                'Author(s)': final_authors,
                'Document title': item.get('dc:title', 'Χωρίς Τίτλο'),
                'Year': item.get('prism:coverDate', '')[:4],
                'Source title': item.get('prism:publicationName', ''),
                'Citation count': item.get('citedby-count', '0'),
                'DOI': item.get('prism:doi', ''),
                'Abstract': item.get('dc:description', 'Δεν υπάρχει περίληψη'),
            })

        df = pd.DataFrame(cleaned_data)
        initial_count = len(df)
        df = df.drop_duplicates(subset=['Document title', 'Year'])
        final_count = len(df)

        if initial_count != final_count:
            print(f"  * Αφαιρέθηκαν {initial_count - final_count} διπλότυπες εγγραφές.")

        filename = f'Scopus_Data_{name}_Full.csv'
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f" ΤΕΛΟΣ {name}! Αποθηκεύτηκαν {final_count} μοναδικές εγγραφές στο '{filename}'.\n")