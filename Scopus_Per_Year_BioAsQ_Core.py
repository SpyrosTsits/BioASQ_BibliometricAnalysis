import pandas as pd
import matplotlib.pyplot as plt

# 1. Φόρτωση του αρχείου Scopus Core
filename = "scopus_data_BioASQ_Core.csv"
try:
    df = pd.read_csv(filename)
    # Καθαρισμός NBSP χαρακτήρων
    df = df.replace('\xa0', ' ', regex=True)
    print(f" Φορτώθηκαν επιτυχώς {len(df)} papers από το αρχείο: {filename}")
except FileNotFoundError:
    print(f" Το αρχείο '{filename}' δεν βρέθηκε. Βεβαιώσου ότι είσαι στον σωστό φάκελο.")
    exit()

# 2. Καθαρισμός και ομαδοποίηση ανά χρονιά
df = df.dropna(subset=['Year'])
df['Year'] = df['Year'].astype(int)

papers_per_year = df['Year'].value_counts().sort_index()

# 3. Στήσιμο του Γραφήματος (Bar Chart)
plt.figure(figsize=(12, 6))

bars = plt.bar(
    papers_per_year.index,
    papers_per_year.values,
    color='#4C72B0',
    edgecolor='black',
    zorder=2
)

# 4. Μορφοποίηση αισθητικής (Τίτλοι, Άξονες, Grid)
plt.title(
    f'Number of Scopus (BioASQ Core) Publications  ({papers_per_year.index.min()}-{papers_per_year.index.max()})',
    fontsize=14,
    fontweight='bold',
    pad=15
)
plt.xlabel('Year', fontsize=12, fontweight='bold')
plt.ylabel('Number of Papers', fontsize=12, fontweight='bold')

plt.xticks(papers_per_year.index, rotation=0, fontsize=11)
plt.yticks(fontsize=11)
plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=1)

# 5. Προσθήκη του ακριβούς αριθμού πάνω από κάθε μπάρα
max_val = max(papers_per_year.values)
for bar in bars:
    yval = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2.0,
        yval + (max_val * 0.015),
        int(yval),
        ha='center',
        va='bottom',
        fontsize=10,
        fontweight='bold'
    )

# 6. Αποθήκευση εικόνας υψηλής ανάλυσης
plt.tight_layout()
output_image = 'Scopus_BioASQ_Publications_Per_Year.png'
plt.savefig(output_image, dpi=300)
print(f" Το γράφημα δημιουργήθηκε και αποθηκεύτηκε ως: '{output_image}'")

# 7. Εμφάνιση του γραφήματος
plt.show()