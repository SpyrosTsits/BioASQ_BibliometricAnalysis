import pandas as pd
import matplotlib.pyplot as plt

# 1. Φόρτωση του τελικού ενιαίου αρχείου
filename = "All_BioASQ_Papers_RQ2.csv"
try:
    df = pd.read_csv(filename)
    print(f" Φορτώθηκαν επιτυχώς {len(df)} papers από το αρχείο: {filename}")
except FileNotFoundError:
    print(f" Το αρχείο '{filename}' δεν βρέθηκε. Βεβαιώσου ότι είσαι στον σωστό φάκελο.")
    exit()

# 2. Ομαδοποίηση και καταμέτρηση των papers ανά χρονιά
# To sort_index() εξασφαλίζει ότι οι χρονιές θα μπουν με τη σωστή χρονολογική σειρά
papers_per_year = df['Year'].value_counts().sort_index()

# 3. Στήσιμο του Γραφήματος (Bar Chart)
plt.figure(figsize=(12, 6)) # Μέγεθος εικόνας (Πλάτος, Ύψος)

# Σχεδιασμός στις μπάρες με ωραίο μπλε χρώμα και μαύρο περίγραμμα
bars = plt.bar(papers_per_year.index, papers_per_year.values, color='#4C72B0', edgecolor='black', zorder=2)

# 4. Μορφοποίηση αισθητικής (Τίτλοι, Άξονες, Grid)
plt.title('Number of Publications (Proceedings) in BioASQ  (2013-2025)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Year', fontsize=12, fontweight='bold')
plt.ylabel('Number of Papers', fontsize=12, fontweight='bold')

# Ορίζουμε να φαίνονται καθαρά όλες οι χρονιές στον άξονα Χ
plt.xticks(papers_per_year.index, rotation=0, fontsize=11)
plt.yticks(fontsize=11)

# Προσθήκη οριζόντιων γραμμών στο παρασκήνιο για ευκολότερη ανάγνωση
plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=1)

# 5. Προσθήκη του ακριβούς αριθμού πάνω από κάθε μπάρα
for bar in bars:
    yval = bar.get_height()
    # Τοποθετεί το νούμερο ακριβώς πάνω από τη μπάρα
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.3, int(yval),
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# 6. Αποθήκευση του γραφήματος σε εικόνα υψηλής ανάλυσης (για το Word/LaTeX της διατριβής σου)
plt.tight_layout()
output_image = 'Proceedings_BioASQ_Publications_Per_Year.png'
plt.savefig(output_image, dpi=300) # dpi=300 για ποιότητα εκτύπωσης
print(f" Το γράφημα δημιουργήθηκε και αποθηκεύτηκε ως: '{output_image}'")

# 7. Εμφάνιση του γραφήματος στην οθόνη
plt.show()