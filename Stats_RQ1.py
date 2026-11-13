import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Φόρτωση του αρχείου
file_name = 'RQ1_Diaxwrismos_Ergasiwn_Updated.csv'
try:
    df = pd.read_csv(file_name, encoding='utf-8')
except FileNotFoundError:
    print(f"File {file_name} not found. Please check the filename.")
    exit()
except UnicodeDecodeError:
    df = pd.read_csv(file_name, encoding='iso-8859-7', encoding_errors='replace')

# Βρίσκουμε αυτόματα το σωστό όνομα της στήλης
level_col = 'New Level' if 'New Level' in df.columns else 'Level'

# 2. Υπολογισμός Στατιστικών
counts = df[level_col].value_counts()
percentages = df[level_col].value_counts(normalize=True) * 100

# Δημιουργία πίνακα με τα αποτελέσματα
stats_df = pd.DataFrame({
    'Number of Papers': counts,
    'Percentage (%)': percentages.round(2)
})

# Εκτύπωση στατιστικών στο τερματικό στα Αγγλικά
print("\n=== ACADEMIC LEVEL DISTRIBUTION STATISTICS ===")
print(stats_df)
print(f"\nTotal sample: {len(df)} papers")

# 3. Σχεδιασμός Γραφήματος
plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")

order = ['MSc', 'PhD', 'BSc', 'Other / Student Papers']
order = [x for x in order if x in stats_df.index]

ax = sns.barplot(
    x=stats_df.loc[order].index,
    y=stats_df.loc[order]['Percentage (%)'],
    palette="viridis"
)

for p in ax.patches:
    ax.annotate(f'{p.get_height():.1f}%',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom',
                fontsize=12, fontweight='bold', color='black',
                xytext=(0, 5), textcoords='offset points')

# Μορφοποίηση στα Αγγλικά
plt.title('Distribution of Academic Levels in BioASQ Papers', fontsize=16, fontweight='bold')
plt.xlabel('Academic Level', fontsize=14)
plt.ylabel('Percentage of Total (%)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.ylim(0, max(stats_df['Percentage (%)']) + 10)
plt.tight_layout()

# Αποθήκευση εικόνας
plt.savefig('Academic_Level_Distribution.png', dpi=300)
print("\nChart successfully saved as 'Academic_Level_Distribution.png'")
plt.show()