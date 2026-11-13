import pandas as pd
import re
import csv

input_file = "scopus_data_BioASQ_Core.csv"

print(f"⏳ Φόρτωση αρχείου: {input_file}...")
try:
    # Προσπάθεια ανάγνωσης με το προεπιλεγμένο κόμμα
    df = pd.read_csv(input_file).replace('\xa0', ' ', regex=True)

    # Έλεγχος: Αν το Pandas είδε μόνο 1 στήλη, το αρχείο είχε διαχωριστικό ερωτηματικό
    if len(df.columns) == 1:
        print(" Εντοπίστηκε 1 στήλη. Δοκιμή ανάγνωσης με ερωτηματικό (;)...")
        df = pd.read_csv(input_file, sep=';').replace('\xa0', ' ', regex=True)

except FileNotFoundError:
    print(f" Το αρχείο {input_file} δεν βρέθηκε.")
    exit()

# Ορισμός των Regex Patterns
qa_pattern = re.compile(r'\b(question answering|qa|machine reading comprehension|chatbot|conversational agent|rag)\b', re.IGNORECASE)

si_pattern = re.compile(r'\b(semantic indexing|semantic annotation|text mining|information extraction|named entity recognition|ner|mesh|indexing|annotation)\b', re.IGNORECASE)


def check_categories(row):
    title = str(row.get('Document title', row.get('Title', '')))
    abstract = str(row.get('Abstract', ''))
    keywords = str(row.get('Keywords', ''))
    full_text = f"{title} {abstract} {keywords}"

    is_qa = bool(qa_pattern.search(full_text))
    is_si = bool(si_pattern.search(full_text))
    return is_qa, is_si


df[['is_QA', 'is_SI']] = df.apply(lambda row: pd.Series(check_categories(row)), axis=1)

# Δημιουργία των τελικών συνόλων (συμπεριλαμβάνονται και τα "Both" άρθρα)
qa_df = df[df['is_QA']].drop(columns=['is_QA', 'is_SI'])
si_df = df[df['is_SI']].drop(columns=['is_QA', 'is_SI'])

# -------------------------------------------------------------
# ΕΞΑΓΩΓΗ ΣΕ CSV (Αυστηρή μορφοποίηση με QUOTE_ALL)
# -------------------------------------------------------------
out_qa = "scopus_BioASQ_QA.csv"
out_si = "scopus_BioASQ_SI.csv"

# Το csv.QUOTE_ALL εγγυάται ότι τα μεγάλα κείμενα δεν θα χαλάσουν τη δομή
qa_df.to_csv(out_qa, index=False, encoding='utf-8-sig', sep=',', quoting=csv.QUOTE_ALL)
si_df.to_csv(out_si, index=False, encoding='utf-8-sig', sep=',', quoting=csv.QUOTE_ALL)

print(f"\nΤα αρχεία CSV δημιουργήθηκαν με επιτυχία και αυστηρή δομή:")
print(f"  -> {out_qa}")
print(f"  -> {out_si}")