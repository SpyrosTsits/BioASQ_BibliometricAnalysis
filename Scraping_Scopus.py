import requests
import pandas as pd
import time

# Βάλε εδώ το API Key
API_KEY =""
SEARCH_URL = 'https://api.elsevier.com/content/search/scopus'

headers = {
    'Accept': 'application/json',
    'X-ELS-APIKey': API_KEY
}

# Τα δύο queries που χρειαζόμαστε για το project
queries = {
    'BioASQ_Core': 'TITLE-ABS-KEY("BioASQ")',
    'General_Field': 'TITLE-ABS-KEY("biomedical question answering" OR "biomedical semantic indexing") AND NOT TITLE-ABS-KEY("BioASQ")'
}


def fetch_scopus_data(query_name, query_string):
    print(f"\n--- Ξεκινάει η λήψη για: {query_name} ---")
    all_results = []
    start_index = 0
    count = 25

    while True:
        print(f"Άντληση αποτελεσμάτων από {start_index}...")

        params = {
            'query': query_string,
            'count': count,
            'start': start_index,
            'view': 'COMPLETE' , # Ζητάμε την πλήρη μορφή (Abstracts, Affiliations, Keywords)
            'date': '2012-2026'
        }

        response = requests.get(SEARCH_URL, headers=headers, params=params)

        if response.status_code == 429:
            print("Όριο κλήσεων (Rate Limit). Αναμονή 5 δευτερόλεπτα...")
            time.sleep(5)
            continue
        elif response.status_code != 200:
            print(f"Σφάλμα API: {response.status_code} - {response.text}")
            break

        data = response.json()
        search_results = data.get('search-results', {})
        entries = search_results.get('entry', [])

        if not entries:
            break

        all_results.extend(entries)

        total_results = int(search_results.get('opensearch:totalResults', 0))
        start_index += count

        if start_index >= total_results:
            break

        time.sleep(0.5)  # Μικρή παύση για ασφάλεια

    return all_results


# Εκτέλεση της διαδικασίας για κάθε query
for name, q_string in queries.items():
    results = fetch_scopus_data(name, q_string)

    if results:
        cleaned_data = []
        for item in results:
            # --- Εξαγωγή Affiliations ---
            affiliations = item.get('affiliation', [])
            affil_names = [affil.get('affilname') for affil in affiliations if
                           isinstance(affil, dict) and 'affilname' in affil]

            # --- ΝΕΟ: Εξαγωγή ΟΛΩΝ των Συγγραφέων ---
            authors_data = item.get('author', [])
            author_names = []
            if isinstance(authors_data, list):
                for auth in authors_data:
                    if isinstance(auth, dict) and 'authname' in auth:
                        author_names.append(auth['authname'])

            # Αν για κάποιο λόγο δεν βρει τη λίστα, κρατάει τον 1ο συγγραφέα ως backup
            final_authors = "; ".join(author_names) if author_names else item.get('dc:creator', '')

            # Αντιστοίχιση των επιλογών με τα πεδία του API
            cleaned_data.append({
                # --- Citation information ---
                'Author(s)': final_authors,  # Χρησιμοποιούμε τη νέα μεταβλητή με όλους τους συγγραφείς
                'Document title': item.get('dc:title'),
                'Year': item.get('prism:coverDate', '')[:4],
                'Source title': item.get('prism:publicationName'),
                'Citation count': item.get('citedby-count'),
                'Source & document type': item.get('subtypeDescription'),
                'DOI': item.get('prism:doi'),

                # --- Bibliographical information ---
                'Affiliations': "; ".join(affil_names) if affil_names else "",
                'PubMed ID': item.get('pubmed-id'),

                # --- Abstract & keywords ---
                'Abstract': item.get('dc:description'),
                'Keywords': item.get('authkeywords'),

                # --- Funding details ---
                'Fund Sponsor': item.get('fund-sponsor'),

                # --- Other information ---
                'Conference Information': item.get('meeting', {}).get('meetingName') if isinstance(item.get('meeting'),
                                                                                                   dict) else None
            })

        # Μετατροπή σε DataFrame και αποθήκευση
        df = pd.DataFrame(cleaned_data)
        filename = f'scopus_data_{name}.csv'
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Ολοκληρώθηκε! Αποθηκεύτηκαν {len(df)} εγγραφές στο '{filename}'.")
    else:
        print(f"Δεν βρέθηκαν δεδομένα για το {name}.")