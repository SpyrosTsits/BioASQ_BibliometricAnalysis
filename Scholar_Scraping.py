from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib.parse
import re

# 1. Τα Αυστηρά Queries (Ακριβώς η ίδια λογική με το Scopus)
queries = {
    'BioASQ_Core': 'BioASQ',
    'General_Field': 'biomedical "question answering" OR biomedical "semantic indexing" -BioASQ'
}

# 2. Ενημέρωση Χρονολογίας μέχρι σήμερα (2026)
start_year = 2012
end_year = 2026

print("Άνοιγμα του Chrome Browser...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

for name, query in queries.items():
    print(f"\n{'=' * 50}")
    print(f"--- Ξεκινάει η αναζήτηση για: {name} (Ανά Έτος) ---")
    print(f"{'=' * 50}")

    encoded_query = urllib.parse.quote(query)
    all_results = []

    for year in range(start_year, end_year + 1):
        print(f"\n[Σάρωση Έτους: {year}]")
        page = 0

        while True:
            start_param = page * 10
            # 3. Προσθήκη &filter=0 για να παρακάμψουμε την απόκρυψη των "παρόμοιων" άρθρων
            url = f"https://scholar.google.com/scholar?start={start_param}&q={encoded_query}&hl=en&as_ylo={year}&as_yhi={year}&filter=0"

            driver.get(url)
            time.sleep(3)  # Μικρή παύση για να φορτώσει η σελίδα

            # ΕΞΥΠΝΟΣ ΕΛΕΓΧΟΣ CAPTCHA (Κλασικό recaptcha)
            while "recaptcha" in driver.page_source.lower() or "sorry, we can't verify" in driver.page_source.lower() or "id=\"gs_captcha_c\"" in driver.page_source.lower():
                input(
                    f" ΕΝΤΟΠΙΣΤΗΚΕ CAPTCHA (Έτος {year}, Σελίδα {page + 1})! Λύσε το στον browser και ΠΑΤΑ ENTER εδώ για να συνεχίσουμε...")
                driver.get(url)
                time.sleep(3)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            articles = soup.find_all('div', class_='gs_ri')

            # 4. ΕΛΕΓΧΟΣ ΤΕΡΜΑΤΙΣΜΟΥ (Βελτιωμένος για "Scholar Mirage" vs Σιωπηλό Μπλόκο)
            if not articles:
                page_text = driver.page_source.lower()
                # Ελέγχει αν η Google γράφει ξεκάθαρα ότι δεν βρήκε τίποτα / τελείωσαν τα άρθρα
                if "did not match any articles" in page_text or "δεν ταιριάζει" in page_text or "did not match" in page_text:
                    print(f"Τέλος αποτελεσμάτων για το {year} (πραγματικό τέλος).")
                    break
                else:
                    # Αν η σελίδα είναι άδεια αλλά ΔΕΝ λέει ότι τελείωσαν, είναι ΜΠΛΟΚΟ!
                    user_check = input(
                        f"\n Στοπ! Η Σελίδα {page + 1} ({year}) είναι άδεια, αλλά ίσως είναι ΜΠΛΟΚΟ!\nΚοίτα τον Browser:\n- Αν δεις ότι ΤΕΛΕΙΩΣΑΝ τα άρθρα (ή η λίστα είναι άδεια), γράψε 'ναι' και πάτα Enter.\n- Αν δεις σελίδα 'Unusual traffic', λύσε το CAPTCHA (ή άλλαξε IP), άσε το κενό και πάτα ENTER για επαναφόρτωση: ")

                    if user_check.strip().lower() in ['ναι', 'nai']:
                        print(f"Χειροκίνητη επιβεβαίωση: Τέλος για το {year}.")
                        break
                    else:
                        print("Επαναφόρτωση της σελίδας...")
                        continue

            for article in articles:
                # Τίτλος
                title_tag = article.find('h3', class_='gs_rt')
                title = title_tag.text if title_tag else ''
                title = re.sub(r'^\[.*?\]\s*', '', title)  # Καθαρισμός από [HTML], [PDF] κλπ.

                # Συγγραφείς, Περιοδικό, Έτος
                author_info = article.find('div', class_='gs_a')
                author_text = author_info.text if author_info else ''

                authors = ''
                source_title = ''
                extracted_year = str(year)

                parts = author_text.split(' - ')
                authors = parts[0]
                if len(parts) > 1:
                    source_title = re.sub(r',?\s*\b(19|20)\d{2}\b', '', parts[1]).strip()

                # Περίληψη (Snippet)
                snippet_tag = article.find('div', class_='gs_rs')
                snippet = snippet_tag.text if snippet_tag else ''

                # Link
                link_tag = title_tag.find('a') if title_tag else None
                link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else ''

                # --- ΑΝΤΙΣΤΟΙΧΙΣΗ ΜΕ ΤΑ ΠΕΔΙΑ ΤΟΥ SCOPUS ---
                all_results.append({
                    'Authors': authors,
                    'Author(s) ID': '',
                    'Title': title,
                    'Year': extracted_year,
                    'Source title': source_title,
                    'Volume': '',
                    'Issue': '',
                    'Art. No.': '',
                    'Page start': '',
                    'Page end': '',
                    'Page count': '',
                    'Cited by': '',
                    'DOI': '',
                    'Link': link,
                    'Affiliations': '',
                    'Authors with affiliations': '',
                    'Abstract': snippet,
                    'Author Keywords': '',
                    'Index Keywords': '',
                    'Document Type': '',
                    'Publication Stage': '',
                    'Open Access': '',
                    'Source': 'Google Scholar',
                    'EID': ''
                })

            print(f"  -> Σελίδα {page + 1}: Αντλήθηκαν {len(articles)} άρθρα.")
            page += 1
            time.sleep(4)  # Κρίσιμη παύση για anti-bot

    # --- ΑΠΟΘΗΚΕΥΣΗ ΔΕΔΟΜΕΝΩΝ ---
    if all_results:
        df = pd.DataFrame(all_results)
        initial_count = len(df)
        df.drop_duplicates(subset=['Title'], inplace=True)

        # Εξασφαλίζουμε ότι η σειρά των στηλών είναι ΑΚΡΙΒΩΣ όπως στο Scopus
        scopus_columns = ['Authors', 'Author(s) ID', 'Title', 'Year', 'Source title', 'Volume', 'Issue', 'Art. No.',
                          'Page start', 'Page end', 'Page count', 'Cited by', 'DOI', 'Link', 'Affiliations',
                          'Authors with affiliations', 'Abstract', 'Author Keywords', 'Index Keywords', 'Document Type',
                          'Publication Stage', 'Open Access', 'Source', 'EID']
        df = df[scopus_columns]

        filename = f'scholar_{name}_final.csv'
        df.to_csv(filename, index=False, encoding='utf-8-sig')

        print(f"\n Ολοκληρώθηκε το {name}:")
        print(f" - Αποθηκεύτηκαν {len(df)} ΜΟΝΑΔΙΚΕΣ εγγραφές στο '{filename}'.")
        print(" - Οι στήλες είναι 100% συμβατές με το format του Scopus.\n")
    else:
        print(f"\nΔεν βρέθηκαν καθόλου αποτελέσματα για το {name}.\n")

print("Η διαδικασία scraping ολοκληρώθηκε! Κλείσιμο browser...")
driver.quit()