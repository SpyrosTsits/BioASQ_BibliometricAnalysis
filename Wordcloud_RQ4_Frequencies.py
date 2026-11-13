import pandas as pd
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

# 1. Φόρτωση και προετοιμασία δεδομένων
filename = 'scopus_data_BioASQ_Core_with_Countries.csv'
try:
    df = pd.read_csv(filename)
except FileNotFoundError:
    print(f"Το αρχείο '{filename}' δεν βρέθηκε.")
    exit()

# Ενοποίηση του κειμένου
df['Text'] = df['Document title'].fillna('') + " " + df['Abstract'].fillna('') + " " + df['Keywords'].fillna('')
df = df.dropna(subset=['Text'])

# Μετατροπή όλου του κειμένου σε πεζά
full_text = " ".join(df['Text'].tolist()).lower()

# 2. Στοχευμένη λίστα μεθόδων και τεχνικών (NLP/ML)
target_methods = [
    'classification', 'ranking', 'transformer', 'transformers', 'factoid', 'entity recognition',
    'named entity recognition', 'ner', 'embedding', 'embeddings', 'generation', 'deep learning',
    'machine learning', 'bert', 'biobert', 'roberta', 'pubmedbert', 'llm', 'llms', 'gpt',
    'chatgpt', 'rag', 'fine-tuning', 'extraction', 'semantic indexing', 'question answering',
    'summarization', 'ensemble', 'neural network', 'cnn', 'svm', 'k-nn', 'logistic regression',
    'information retrieval', 'attention', 'transfer learning', 'data augmentation', 'word2vec',
    'biomedical language model', 'generative', 'extractive'
]

# 3. Υπολογισμός Συχνότητας (Frequency)
frequencies = {}
for term in target_methods:
    # Χρήση Regex για να βρούμε ακριβείς λέξεις/φράσεις, αγνοώντας σημεία στίξης (π.χ. fine-tuning ή fine tuning)
    pattern = r'\b' + re.escape(term).replace(r'\-', r'[- ]?') + r'\b'
    count = len(re.findall(pattern, full_text))
    if count > 0:
        frequencies[term] = count

# Συγχώνευση παρόμοιων όρων για πιο καθαρό Wordcloud (π.χ. transformer & transformers -> transformer)
merged_frequencies = Counter()
for term, count in frequencies.items():
    if term in ['transformers', 'transformer']:
        merged_frequencies['transformer'] += count
    elif term in ['embedding', 'embeddings']:
        merged_frequencies['embedding'] += count
    elif term in ['llm', 'llms']:
        merged_frequencies['llm'] += count
    elif term in ['named entity recognition', 'ner', 'entity recognition']:
        merged_frequencies['entity recognition (NER)'] += count
    else:
        merged_frequencies[term] += count

# Εκτύπωση των συχνοτήτων (για χρήση στο Report)
print("=== ΣΥΧΝΟΤΗΤΕΣ ΜΕΘΟΔΩΝ & ΤΕΧΝΙΚΩΝ ===")
sorted_freqs = merged_frequencies.most_common()
for word, freq in sorted_freqs:
    print(f"{word}: {freq}")

# 4. Δημιουργία Wordcloud από τις συχνότητες (generate_from_frequencies)
wc = WordCloud(
    width=1200,
    height=800,
    background_color='white',
    colormap='viridis',  # Επαγγελματική χρωματική παλέτα
    max_words=50,
    contour_width=0,
    prefer_horizontal=0.8  # Το 80% των λέξεων να είναι οριζόντιες για καλύτερη αναγνωσιμότητα
)

# Δημιουργία με βάση το λεξικό συχνοτήτων
wc.generate_from_frequencies(merged_frequencies)

# 5. Εμφάνιση και Αποθήκευση
plt.figure(figsize=(14, 9), facecolor='white')
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title('Top Research Terms in BioASQ Publications By Frequency', fontsize=18, fontweight='bold', pad=20)

plt.tight_layout()
output_file = 'Wordcloud_RQ4_Frequencies.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nΤο στοχευμένο Wordcloud αποθηκεύτηκε ως '{output_file}'")
plt.show()