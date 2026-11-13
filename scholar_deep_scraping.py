from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

print(" Εκκίνηση του συστήματος (Ανοίγει το Chrome...)")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

papers_data = []

# Φορτώνουμε την πρώτη σελίδα
first_url = f'https://scholar.google.com/scholar?start=0&q="BioASQ"+thesis'
driver.get(first_url)

print("\n" + "=" * 60)
print(" ΠΡΟΣΟΧΗ: Το Scholar μόλις άνοιξε στο Chrome.")
print("Αν η Google σου ζητάει να λύσεις CAPTCHA, λύσε το τώρα.")
print("Μόλις δεις τα κανονικά αποτελέσματα, έλα εδώ και...")
input(" ΠΑΤΑ ΤΟ ΠΛΗΚΤΡΟ 'ENTER' ΓΙΑ ΝΑ ΞΕΚΙΝΗΣΕΙ Η ΦΑΣΗ 1! ")
print("=" * 60 + "\n")

# --- ΦΑΣΗ 1: ΠΛΟΗΓΗΣΗ ΜΕ URL ---
for start in range(0, 600, 10):
    if start > 0:
        url = f'https://scholar.google.com/scholar?start={start}&q="BioASQ"+thesis'
        driver.get(url)
        time.sleep(2)

    if "sorry/index" in driver.current_url:
        print("\n Η Google έβγαλε CAPTCHA! Λύσε το στο παράθυρο του Chrome.")
        input("Μόλις το λύσεις, πάτα ENTER εδώ για να συνεχίσουμε...")

    print(f"Συλλογή δεδομένων (Αποτελέσματα {start} έως {start + 10})...")

    results = driver.find_elements(By.CSS_SELECTOR, ".gs_ri")
    if len(results) == 0:
        print("Δεν βρέθηκαν άλλα αποτελέσματα. Τέλος Φάσης 1.")
        break

    for res in results:
        try:
            title_el = res.find_element(By.CSS_SELECTOR, ".gs_rt a")
            title = title_el.text
            link = title_el.get_attribute("href")
            papers_data.append({'Title': title, 'URL': link, 'Abstract': ''})
        except:
            continue

print(f"\n Εντοπίστηκαν {len(papers_data)} εργασίες συνολικά! Ξεκινάει η Φάση 2...")

# --- ΦΑΣΗ 2: ΕΞΑΓΩΓΗ ABSTRACT ΜΕΣΩ SELENIUM (REAL BROWSER) ---
# Βάζουμε ένα όριο χρόνου (π.χ. 15 δευτερόλεπτα) για να μην κολλήσει το script αν ένα site έχει πέσει
driver.set_page_load_timeout(15)

for i, paper in enumerate(papers_data):
    url = paper['URL']
    print(f"[{i + 1}/{len(papers_data)}] Ανάκτηση από: {url[:60]}...")

    if url.lower().endswith('.pdf'):
        paper['Abstract'] = "Απευθείας αρχείο PDF (Απαιτείται χειροκίνητος έλεγχος)"
        continue

    try:
        # Χρησιμοποιούμε τον Chrome για να μπούμε στο site του εκδότη
        driver.get(url)
        time.sleep(1.5)  # Περιμένουμε λίγο να φορτώσει η JavaScript της σελίδας

        # Αντλούμε τον HTML κώδικα όπως τον έκανε render ο Chrome
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        abstract_text = ""

        # Στρατηγική Α: Ψάχνουμε τα επίσημα Meta Tags
        meta_tags = soup.find_all('meta', attrs={
            'name': ['citation_abstract', 'DC.description', 'description', 'og:description']})
        for tag in meta_tags:
            content = tag.get('content', '')
            if content and len(content) > 100:
                abstract_text = content
                break

        # Στρατηγική Β: Ψάχνουμε για <div> ή <section> με λέξη abstract
        if not abstract_text:
            abstract_divs = soup.find_all(['div', 'section'], class_=lambda c: c and 'abstract' in c.lower())
            if abstract_divs:
                abstract_text = abstract_divs[0].get_text(separator=' ', strip=True)

        # Στρατηγική Γ: Πρώτες μεγάλες παραγράφοι
        if not abstract_text:
            paragraphs = soup.find_all('p')
            large_paragraphs = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 150]
            if large_paragraphs:
                abstract_text = " ".join(large_paragraphs[:2])

        if abstract_text:
            # Καθαρίζουμε τα πολλά κενά/enters
            paper['Abstract'] = " ".join(abstract_text.split())
        else:
            paper['Abstract'] = "Το κείμενο είναι κλειδωμένο / Δεν βρέθηκε εμφανές abstract"

    except Exception as e:
        paper['Abstract'] = "Timeout ή Σφάλμα φόρτωσης σελίδας"

    # Αποθηκεύουμε ανά 50 άρθρα (ως backup, σε περίπτωση που κοπεί το ρεύμα ή κλείσεις το παράθυρο)
    if (i + 1) % 50 == 0:
        pd.DataFrame(papers_data).to_csv("Scholar_Backup.csv", index=False, encoding='utf-8-sig')

driver.quit()  # Τώρα το κλείνουμε!

# Τελική Αποθήκευση
df = pd.DataFrame(papers_data)
df.to_csv("Scholar_BioASQ_Thesis.csv", index=False, encoding='utf-8-sig')
print(f"\ ΤΕΛΟΣ! Τα αποτελέσματα αποθηκεύτηκαν στο 'Scholar_BioASQ_Thesis.csv'.")