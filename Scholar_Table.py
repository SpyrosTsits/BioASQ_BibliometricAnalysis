import matplotlib.pyplot as plt
import pandas as pd




# Αριθμοί για τον πυρήνα του BioASQ
bioasq_qa = 2042
bioasq_si = 699
bioasq_overlap = 418

# Δημιουργία των δεδομένων του Πίνακα
data = [

    ['BioASQ Core', str(bioasq_qa), str(bioasq_si), str(bioasq_overlap)]
]

columns = ['Category', 'Question Answering (QA)', 'Semantic Indexing (SI)', 'Overlap (QA & SI)']

df = pd.DataFrame(data, columns=columns)

# ==========================================
# ΣΧΕΔΙΑΣΜΟΣ ΤΟΥ ΠΙΝΑΚΑ ΩΣ ΕΙΚΟΝΑ
# ==========================================
fig, ax = plt.subplots(figsize=(10, 3), dpi=300)
ax.axis('off')  # Κρύβουμε τους άξονες

# Δημιουργία του πίνακα
table = ax.table(
    cellText=df.values,
    colLabels=df.columns,
    cellLoc='center',
    loc='center'
)

# Μορφοποίηση του πίνακα (χρώματα, γραμματοσειρές)
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1, 2)  # Προσαρμογή ύψους/πλάτους κελιών

# Χρωματισμός Κεφαλίδων (Headers)
for j, col in enumerate(columns):
    cell = table[0, j]
    cell.set_facecolor('#4C72B0')  # Μπλε χρώμα για την κεφαλίδα
    cell.set_text_props(color='white', weight='bold')

# Έντονη γραφή για την πρώτη στήλη (Κατηγορίες)
for i in range(1, len(df) + 1):
    table[i, 0].set_text_props(weight='bold')
    table[i, 0].set_facecolor('#f2f2f2') # Ελαφρύ γκρι background

plt.title('Google Scholar Publications: QA vs SI ',
          fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
output_file = 'Scholar_Data_Table.png'
plt.savefig(output_file, bbox_inches='tight', facecolor='white')
print(f"Ο πίνακας αποθηκεύτηκε επιτυχώς ως '{output_file}'")
plt.show()