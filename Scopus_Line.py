import pandas as pd
import matplotlib.pyplot as plt

# 1. ΦΟΡΤΩΣΗ ΔΕΔΟΜΕΝΩΝ SCOPUS
file_core_qa = "scopus_BioASQ_QA.csv"
file_ext_qa  = "Scopus_Data_Expanded_QA_Full.csv"
file_core_si = "scopus_BioASQ_SI.csv"
file_ext_si  = "Scopus_Data_Expanded_SI_Full.csv"

try:
    df_core_qa = pd.read_csv(file_core_qa)
    df_ext_qa  = pd.read_csv(file_ext_qa)
    df_core_si = pd.read_csv(file_core_si)
    df_ext_si  = pd.read_csv(file_ext_si)
except FileNotFoundError as e:
    print(f"⚠️ Σφάλμα: Δεν βρέθηκε το αρχείο {e.filename}.")
    exit()

# Τυποποίηση του ονόματος της στήλης του τίτλου για όλα τα DataFrames
for df in [df_core_qa, df_ext_qa, df_core_si, df_ext_si]:
    if 'Document title' in df.columns:
        df.rename(columns={'Document title': 'Title'}, inplace=True)

# 2. ΣΥΝΕΝΩΣΗ ΚΑΙ ΚΑΘΑΡΙΣΜΟΣ
# Ενώνουμε τα Core και Extended για να έχουμε το συνολικό πεδίο (Total QA / Total SI)
df_total_qa = pd.concat([df_core_qa, df_ext_qa]).drop_duplicates(subset=['Title'])
df_total_si = pd.concat([df_core_si, df_ext_si]).drop_duplicates(subset=['Title'])

# Κρατάμε μόνο τις γραμμές που έχουν έτος και το μετατρέπουμε σε ακέραιο
df_total_qa = df_total_qa.dropna(subset=['Year'])
df_total_qa['Year'] = df_total_qa['Year'].astype(int)

df_total_si = df_total_si.dropna(subset=['Year'])
df_total_si['Year'] = df_total_si['Year'].astype(int)

# 3. ΥΠΟΛΟΓΙΣΜΟΣ ΔΗΜΟΣΙΕΥΣΕΩΝ ΑΝΑ ΕΤΟΣ
qa_trend = df_total_qa.groupby('Year').size().reset_index(name='QA_Count')
si_trend = df_total_si.groupby('Year').size().reset_index(name='SI_Count')

# Ενοποίηση σε ένα DataFrame (γεμίζουμε με 0 αν κάποιο έτος λείπει)
trend_df = pd.merge(qa_trend, si_trend, on='Year', how='outer').fillna(0).sort_values('Year')

# 4. ΣΧΕΔΙΑΣΜΟΣ ΤΟΥ ΓΡΑΦΗΜΑΤΟΣ (LINE CHART)
plt.figure(figsize=(12, 7), facecolor='white')
plt.rcParams['font.family'] = 'sans-serif'

# Περιορισμός στο εύρος 2012-2026 (αν υπάρχουν outliers)
trend_df = trend_df[(trend_df['Year'] >= 2012) & (trend_df['Year'] <= 2026)]

plt.plot(trend_df['Year'], trend_df['QA_Count'], marker='o', markersize=8, linestyle='-', linewidth=3, color='#2CA02C', label='Total Biomedical QA')
plt.plot(trend_df['Year'], trend_df['SI_Count'], marker='s', markersize=8, linestyle='--', linewidth=3, color='#D62728', label='Total Biomedical SI')

plt.title('Global Scopus Trend: Biomedical QA vs SI (2012-2026)', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Publication Year', fontsize=14, labelpad=10)
plt.ylabel('Number of Publications', fontsize=14, labelpad=10)

plt.xticks(trend_df['Year'], fontsize=11, rotation=45)
plt.yticks(fontsize=11)

plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.grid(True, axis='x', linestyle=':', alpha=0.4)

plt.legend(fontsize=12, loc='upper left', frameon=True, shadow=True, facecolor='white')

# 5. ΑΠΟΘΗΚΕΥΣΗ
plt.tight_layout()
output_file = 'Scopus_Trend_LineChart.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"🎉 Το γράφημα τάσης για το Scopus δημιουργήθηκε: '{output_file}'\n")
plt.show()