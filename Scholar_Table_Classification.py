import pandas as pd
import re

# 1. Φόρτωση του αρχείου
file_name = 'scholar_BioASQ_Core_final.csv'
try:
    df = pd.read_csv(file_name)
except FileNotFoundError:
    print(f"Το αρχείο '{file_name}' δεν βρέθηκε.")
    exit()

# Ενοποίηση Τίτλου και Περίληψης
df['Search_Text'] = df['Title'].fillna('') + " " + df['Abstract'].fillna('')
df['Search_Text'] = df['Search_Text'].str.lower()

# 2. ΕΚΤΕΤΑΜΕΝΑ Keywords με χρήση Regular Expressions
# Προστέθηκαν σύγχρονοι όροι (LLMs, prompts, MRC, summarization κλπ)
qa_pattern = r'\b(?:question answering|qa|question|answer|answers|factoid|yes/no|snippet|snippets|retrieval|generation|llms?|chatgpt|gpt|summarization|task b|task 1b|reading comprehension|mrc|dialogue|prompt|conversational)\b'

si_pattern = r'\b(?:semantic indexing|indexing|mesh|annotation|document classification|document retrieval|hierarchical classification|classification|entity|extraction|semantic|task a|task 1a|multi-label|categorization|tagging|ner|named entity)\b'


# 3. Συνάρτηση Διπλής Ταξινόμησης (χωρίς Unclassified)
def classify_paper(text):
    has_qa = bool(re.search(qa_pattern, text))
    has_si = bool(re.search(si_pattern, text))

    # Pass 1: Ξεκάθαρη Ταξινόμηση βάσει Keywords
    if has_qa and has_si:
        return 'Both (QA & SI)'
    elif has_qa:
        return 'QA'
    elif has_si:
        return 'SI'

    # Pass 2: Fallback για τα Unclassified
    # Αν αναφέρεται σε έγγραφα/άρθρα/συλλογές, τείνει προς Semantic Indexing (Task A)
    fallback_si_pattern = r'\b(?:document|documents|article|articles|literature|corpus|database|repository)\b'
    has_fallback_si = bool(re.search(fallback_si_pattern, text))

    if has_fallback_si:
        return 'SI'
    else:
        # Οτιδήποτε άλλο (γενικά μοντέλα γλώσσας, αλγόριθμοι NLP κλπ) πηγαίνει στο QA (Task B)
        return 'QA'


# 4. Εφαρμογή της ταξινόμησης
print("⏳ Γίνεται η ταξινόμηση των άρθρων (Εγγύηση 0 Unclassified)...")
df['BioASQ_Category'] = df['Search_Text'].apply(classify_paper)

# Αφαίρεση της προσωρινής στήλης
df = df.drop(columns=['Search_Text'])

# 5. Αποθήκευση
output_file = 'scholar_BioASQ_Core_Classified.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f" Το αρχείο αποθηκεύτηκε με τη νέα στήλη 'BioASQ_Category' ως '{output_file}'\n")

# 6. Εμφάνιση των τελικών Στατιστικών
counts = df['BioASQ_Category'].value_counts()
print("=== ΤΕΛΙΚΑ ΑΠΟΤΕΛΕΣΜΑΤΑ (GOOGLE SCHOLAR) ===")
print(counts)
print(f"\nΣύνολο άρθρων: {len(df)}")