import pandas as pd
import matplotlib.pyplot as plt

# 1. Φόρτωση και προετοιμασία δεδομένων
df = pd.read_csv('scopus_data_BioASQ_Core_with_Countries.csv')
df['Text'] = df['Document title'].fillna('') + " " + df['Abstract'].fillna('') + " " + df['Keywords'].fillna('')
df = df.dropna(subset=['Text', 'Year'])

# 2. Λίστα Stop Words
custom_stopwords_list = {
    'bioasq', 'question', 'answer', 'answers', 'performance', 'phase', 'text', 'clef', 'participation', 'team',
    'semantic', 'indexing', 'snippet', 'specific', 'large scale', 'lab', 'best', 'research',
    'large language', 'show', 'overview', 'expert', 'proposed', 'propose', 'yes', 'list', 'part', 'concept',
    'natural language', 'language processing', 'framework', 'hybrid', 'benchmark', 'experiment', 'state', 'art', 'set',
    'end', 'type',
    'large', 'scale', 'language', 'natural', 'context', 'passage', 'technique', 'relevant', 'types', 'various',
    'address', 'aim', 'one', 'second',
    'multiple', 'given', 'score', 'system', 'systems', 'model', 'models', 'retrieval', 'domain', 'knowledge',
    'result', 'results', 'present', 'presents', 'task', 'tasks', 'dataset', 'datasets',
    'medical', 'qa', 'training', 'approach', 'approaches', 'information',
    'document', 'documents', 'evaluation', 'methods', 'method',
    'language models', 'language model', 'semantic indexing', 'biomedical',
    'answering', 'challenge', 'based', 'using', 'paper', 'used', 'achieved',
    'provide', 'b', 'two', 'three', 'new', 'well', 'clinical', 'different',
    'use', 'work', 'data', 'questions', 'article', 'literature', 'need',
    'processing', 'techniques', 'architecture', 'baseline', 'corpus', 'query',
    'sentence', 'snippets', 'articles', 'term', 'tool', 'improve', 'improvement',
    'challenges', 'prediction', 'demonstrate', 'evaluated', 'evaluate', 'compared',
    'describe', 'achieve', 'including', 'available', 'current', 'existing', 'first',
    'top', 'exact', 'solution', 'stage', 'track', 'field', 'study', 'analysis',
    'experiments', 'submission', 'adaptation', 'representation', 'pre', 'trained',
    'feature', 'source', 'rank', 's', 'year', 'english', 'novel', 'ideal', 'accuracy',
    'experts', 'shared', 'outperform', 'application', 'several', 'number', 'due',
    'across', 'order', 'high', 'scientific', 'significant', 'obtained', 'developed',
    'development', 'generate', 'generated', 'combine', 'finding', 'provided',
    'setting', 'process', 'procedure', 'terms', 'four', 'th', 'ir', 'metric',
    'participated', 'resource', 'test', 'better', 'quality', 'human', 'support', 'applications', 'output', 'achieves',
    'problem', 'disease', 're', 'f', 'via', 'spanish', 'previous', 'mesinesp', 'forum', 'labs', 'multilingual',
    'content', 'word',
    'learning', 'open', 'competitive', 'scores', 'candidate', 'aims', 'teams',
    'batches', 'batch', 'micro', 'strategies', 'resources', 'passages', 'effective',
    'effectiveness', 'related', 'achieving', 'experimental', 'additional',
    'provides', 'overall', 'specifically', 'within', 'concepts', 'texts'
}

def clean_text(text):
    words = str(text).lower().split()
    return " ".join([word for word in words if word not in custom_stopwords_list])

df['Clean_Text'] = df['Text'].apply(clean_text)

# 3. Το ΠΡΟΣΑΡΜΟΣΜΕΝΟ λεξικό (ΜΟΝΟ 2 Κατηγορίες)
tech_groups = {
    'Traditional ML & Baselines': ['machine learning', 'svm', 'knn', 'k-nn', 'mti', 'logistic'],
    'Deep Learning': [
        # Βασικοί όροι DL
        'deep learning', 'deep', 'neural network', 'cnn',
        # BERT & Transformers
        'bert', 'biobert', 'roberta', 'pubmedbert', 'transformer', 'transformers',
        # LLMs, GPT, RAG & Fine-Tuning
        'fine-tuning', 'fine-tune', 'finetuning',
        'rag', 'augmented generation',
        'llm', 'llms', 'gpt', 'chatgpt', 'large language model', 'large language models'
    ]
}

# 4. Υπολογισμός συνολικών δημοσιεύσεων ανά έτος
papers_per_year = df.groupby('Year').size()
normalized_data = pd.DataFrame(index=papers_per_year.index)

# 5. Υπολογισμός κανονικοποιημένης συχνότητας
for tech_name, keywords in tech_groups.items():
    pattern = '|'.join([r'\b{}\b'.format(k) for k in keywords])
    df['has_term'] = df['Clean_Text'].str.contains(pattern, na=False)

    term_counts = df[df['has_term']].groupby('Year').size()
    normalized_data[tech_name] = (term_counts / papers_per_year).fillna(0) * 100

# 6. Σχεδιασμός Γραφήματος (ΜΟΝΟ 2 ΓΡΑΜΜΕΣ)
plt.figure(figsize=(12, 6), facecolor='white')
plt.rcParams['font.family'] = 'sans-serif'

# Επιλέγουμε δύο ευδιάκριτα χρώματα: Κόκκινο και Μπλε
colors = ['#d62728', '#1f77b4']

for (i, column) in enumerate(normalized_data.columns):
    plt.plot(normalized_data.index, normalized_data[column], marker='o', linewidth=3, markersize=8, color=colors[i], label=column)

plt.title('Evolution of Core NLP Technologies in BioASQ: Traditional vs Deep Learning', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Publication Year', fontsize=14, labelpad=10)
plt.ylabel('Percentage of Total Papers (%)', fontsize=14, labelpad=10)
plt.xticks(normalized_data.index.astype(int), fontsize=11)
plt.yticks(fontsize=11)

plt.legend(title='Methodologies', fontsize=12, title_fontsize=13, loc='upper left', frameon=True, shadow=True)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

output_file = 'Normalized_BioASQ_Technologies_Binary.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Το γράφημα με τις 2 βασικές κατηγορίες αποθηκεύτηκε ως '{output_file}'")
plt.show()