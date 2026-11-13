import pandas as pd

# 1. Φόρτωση του αρχείου με τις χώρες
input_file = "scopus_data_BioASQ_Core_with_Countries.csv"

print(f"⏳ Φόρτωση αρχείου: {input_file}...\n")
try:
    df = pd.read_csv(input_file)

    # 2. Κρατάμε μόνο όσα έχουν χαρτογραφηθεί επιτυχώς (αφαιρούμε τα 'Unmapped' και τα κενά)
    df_mapped = df.dropna(subset=['Countries'])
    df_mapped = df_mapped[df_mapped['Countries'] != "Unmapped"]

    # 3. Φιλτράρισμα: Ένα paper έχει συνεργασία αν η στήλη 'Countries' περιέχει κόμμα (',')
    df_collab = df_mapped[df_mapped['Countries'].str.contains(',', na=False)]

    total_mapped = len(df_mapped)
    total_collab = len(df_collab)
    percentage = (total_collab / total_mapped) * 100

    print("=" * 100)
    print(" 🌍 ΣΤΑΤΙΣΤΙΚΑ ΔΙΕΘΝΩΝ ΣΥΝΕΡΓΑΣΙΩΝ (International Collaborations)")
    print("=" * 100)
    print(f"• Συνολικά χαρτογραφημένα άρθρα: {total_mapped}")
    print(f"• Άρθρα με διεθνή συνεργασία (>= 2 χώρες): {total_collab}")
    print(f"• Ποσοστό Διεθνούς Συνεργασίας: {percentage:.2f}%\n")

    # 4. Εμφάνιση δείγματος 5 συνεργασιών
    print("--- ΔΕΙΓΜΑ 5 ΣΥΝΕΡΓΑΤΙΚΩΝ PAPERS ---")
    sample_collab = df_collab[['Document title', 'Countries']].head(5)
    for index, row in sample_collab.iterrows():
        print(f"📄 Τίτλος: {row['Document title']}")
        print(f"🤝 Χώρες: {row['Countries']}\n")

    # 5. Αποθήκευση σε νέο CSV για το Παράρτημα/Ανάλυσή σου
    output_file = "Collaborative_Papers_BioASQ.csv"

    # Κρατάμε τις πιο σημαντικές στήλες για το νέο αρχείο
    export_df = df_collab[['Document title', 'Year', 'Affiliations', 'Countries']]
    export_df.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"Δημιουργήθηκε το αρχείο: '{output_file}' με τη λίστα όλων των συνεργασιών.")

except FileNotFoundError:
    print(f" Το αρχείο '{input_file}' δεν βρέθηκε.")
except Exception as e:
    print(f" Προέκυψε ένα σφάλμα: {e}")