import pandas as pd
import matplotlib.pyplot as plt

# 1. Φόρτωση των δεδομένων από το Table 2
filename = "Table_2_Country_Statistics.csv"
try:
    df = pd.read_csv(filename)
except FileNotFoundError:
    print(f" Το αρχείο '{filename}' δεν βρέθηκε. Βεβαιώσου ότι έχεις τρέξει το προηγούμενο script.")
    exit()

# Εξαιρούμε την κατηγορία 'Generic / Unidentifiable' από τα γραφήματα (αν υπάρχει)
df = df[df['Country'] != 'Generic / Unidentifiable'].reset_index(drop=True)

print(" Δημιουργία Γραφημάτων...")

# ==========================================
# ΓΡΑΦΗΜΑ 1: Bar Chart (Top 15 Χώρες)
# ==========================================
top_15 = df.head(15)

plt.figure(figsize=(12, 6))
bars = plt.bar(top_15['Country'], top_15['Total_Mentions'], color='#4C72B0', edgecolor='black', zorder=2)

plt.title('Top 15 Countries by Research Contribution in BioASQ', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Country', fontsize=12, fontweight='bold')
plt.ylabel('Number of Mentions', fontsize=12, fontweight='bold')

# Περιστροφή των ονομάτων για να διαβάζονται εύκολα
plt.xticks(rotation=45, ha='right', fontsize=11)
plt.yticks(fontsize=11)
plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=1)

# Προσθήκη του ακριβούς νούμερου πάνω από κάθε μπάρα
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, int(yval),
             ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
output_bar = 'BioASQ_Top15_Countries_Bar.png'
plt.savefig(output_bar, dpi=300)
print(f" Το ραβδόγραμμα αποθηκεύτηκε ως '{output_bar}'")
plt.show()

# ==========================================
# ΓΡΑΦΗΜΑ 2: Pie Chart (Top 10 vs Άλλες Χώρες)
# ==========================================
top_10 = df.head(10)
# Ομαδοποίηση όλων των υπολοίπων χωρών
other_mentions = df['Total_Mentions'][10:].sum()

# Φτιάχνουμε τις νέες λίστες για την πίτα
pie_labels = list(top_10['Country']) + ['Other Countries']
pie_values = list(top_10['Total_Mentions']) + [other_mentions]

plt.figure(figsize=(10, 8))
# Χρήση επαγγελματικής χρωματικής παλέτας
colors = plt.cm.tab20.colors[:len(pie_labels)]

plt.pie(pie_values, labels=pie_labels, autopct='%1.1f%%', startangle=140,
        colors=colors, wedgeprops={'edgecolor': 'black', 'linewidth': 1},
        textprops={'fontsize': 11})

plt.title('Geographical Distribution of Research Contributions in BioASQ', fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
output_pie = 'BioASQ_Country_Distribution_Pie.png'
plt.savefig(output_pie, dpi=300)
print(f" Το κυκλικό διάγραμμα αποθηκεύτηκε ως '{output_pie}'")
plt.show()