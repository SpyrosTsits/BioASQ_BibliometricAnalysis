import pandas as pd

# Ορισμός του ονόματος του αρχικού και του νέου αρχείου
input_file = 'RQ1_Diaxwrismos_Ergasiwn.csv'  # Βάλε το ακριβές όνομα του αρχείου σου
output_file = 'RQ1_Diaxwrismos_Ergasiwn_Updated.csv'

print(f" Φόρτωση αρχείου: {input_file}...")
try:
    # Προσπάθεια ανάγνωσης (καλύπτει utf-8 και ελληνικά)
    try:
        df = pd.read_csv(input_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(input_file, encoding='iso-8859-7', encoding_errors='replace')

    # Εντοπισμός της σωστής στήλης ('New Level' ή 'Level')
    level_col = 'New Level' if 'New Level' in df.columns else 'Level'

    if level_col in df.columns:
        # 1. Υπολογισμός των αρχικών εγγραφών 'Unknown'
        initial_unknown = (df[level_col] == 'Unknown').sum()
        print(f"Βρέθηκαν {initial_unknown} εγγραφές με την τιμή 'Unknown'.")

        # 2. Αντικατάσταση της τιμής
        df[level_col] = df[level_col].replace('Unknown', 'Other / Student Papers')

        # 3. Αποθήκευση στο νέο αρχείο
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"Η μετατροπή ολοκληρώθηκε! Το νέο αρχείο αποθηκεύτηκε ως: '{output_file}'")

        # Εμφάνιση της νέας κατανομής για επιβεβαίωση
        print("\n--- ΝΕΑ ΚΑΤΑΝΟΜΗ ---")
        print(df[level_col].value_counts())

    else:
        print(f"Δεν βρέθηκε στήλη με όνομα 'Level' ή 'New Level' στο αρχείο.")

except FileNotFoundError:
    print(f"Το αρχείο '{input_file}' δεν βρέθηκε. Βεβαιώσου ότι είναι στον ίδιο φάκελο με το script.")