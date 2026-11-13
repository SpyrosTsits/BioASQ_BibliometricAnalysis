import pandas as pd
import matplotlib.pyplot as plt

# 1. Φόρτωση του αρχείου Google Scholar Core
filename = "scholar_BioASQ_Core_final.csv"
try:
    df = pd.read_csv(filename)
    # Προαιρετικός καθαρισμός NBSP για απόλυτη ασφάλεια
    df = df.replace('\xa0', ' ', regex=True)
    print(f" Φορτώθηκαν επιτυχώς {len(df)} papers από το αρχείο: {filename}")
except FileNotFoundError:
    print(f" Το αρχείο '{filename}' δεν βρέθηκε. Βεβαιώσου ότι είσαι στον σωστό φάκελο.")
    exit()

# 2. Καθαρισμός και ομαδοποίηση ανά χρονιά
# Φιλτράρισμα τυχόν κενών εγγραφών στη στήλη Year και μετατροπή σε ακέραιους
df = df.dropna(subset=['Year'])
df['Year'] = df['Year'].astype(int)

papers_per_year = df['Year'].value_counts().sort_index()

# 3. Στήσιμο του Γραφήματος (Bar Chart)
plt.figure(figsize=(12, 6))

# Σχεδιασμός στις μπάρες με το ίδιο μπλε χρώμα και μαύρο περίγραμμα
bars = plt.bar(
    papers_per_year.index,
    papers_per_year.values,
    color='#4C72B0',
    edgecolor='black',
    zorder=2
)

# 4. Μορφοποίηση αισθητικής (Τίτλοι, Άξονες, Grid)
plt.title(
    f'Number of Google Scholar (BioASQ Core) Publications  ({papers_per_year.index.min()}-{papers_per_year.index.max()})',
    fontsize=14,
    fontweight='bold',
    pad=15
)
plt.xlabel('Year', fontsize=12, fontweight='bold')
plt.ylabel('Number of Papers', fontsize=12, fontweight='bold')

# Ρύθμιση ετικετών στον άξονα Χ
plt.xticks(papers_per_year.index, rotation=45, fontsize=11)
plt.yticks(fontsize=11)

# Προσθήκη οριζόντιων διακεκομμένων γραμμών στο παρασκήνιο
plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=1)

# 5. Προσθήκη του ακριβούς αριθμού πάνω από κάθε μπάρα
max_val = max(papers_per_year.values)
for bar in bars:
    yval = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2.0,
        yval + (max_val * 0.012),
        int(yval),
        ha='center',
        va='bottom',
        fontsize=10,
        fontweight='bold'
    )

# 6. Αποθήκευση εικόνας υψηλής ανάλυσης (300 DPI)
plt.tight_layout()
output_image = 'Scholar_BioASQ_Publications_Per_Year.png'
plt.savefig(output_image, dpi=300)
print(f" Το γράφημα δημιουργήθηκε και αποθηκεύτηκε ως: '{output_image}'")

# 7. Εμφάνιση του γραφήματος
plt.show()