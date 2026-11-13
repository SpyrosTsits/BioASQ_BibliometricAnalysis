import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# 1. ΦΟΡΤΩΣΗ ΔΕΔΟΜΕΝΩΝ SCOPUS (CORE + EXPANDED)
# -------------------------------------------------------------
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
    print(f" Σφάλμα: Δεν βρέθηκε το αρχείο {e.filename}.")
    exit()

# Τυποποίηση ονομάτων στηλών
for df in [df_core_qa, df_ext_qa, df_core_si, df_ext_si]:
    if 'Document title' in df.columns:
        df.rename(columns={'Document title': 'Title'}, inplace=True)

# -------------------------------------------------------------
# 2. ΚΑΘΑΡΙΣΜΟΣ ΔΕΔΟΜΕΝΩΝ ΓΙΑ ΤΟ GLOBAL TREND (TOTAL)
# -------------------------------------------------------------
df_total_qa = pd.concat([df_core_qa, df_ext_qa]).drop_duplicates(subset=['Title']).dropna(subset=['Year'])
df_total_qa['Year'] = df_total_qa['Year'].astype(int)

df_total_si = pd.concat([df_core_si, df_ext_si]).drop_duplicates(subset=['Title']).dropna(subset=['Year'])
df_total_si['Year'] = df_total_si['Year'].astype(int)

trend_global_qa = df_total_qa.groupby('Year').size().reset_index(name='QA_Count')
trend_global_si = df_total_si.groupby('Year').size().reset_index(name='SI_Count')
global_df = pd.merge(trend_global_qa, trend_global_si, on='Year', how='outer').fillna(0).sort_values('Year')
global_df = global_df[(global_df['Year'] >= 2012) & (global_df['Year'] <= 2026)]

# -------------------------------------------------------------
# 3. ΚΑΘΑΡΙΣΜΟΣ ΔΕΔΟΜΕΝΩΝ ΓΙΑ ΤΟ BIOASQ CORE TREND
# -------------------------------------------------------------
df_core_qa_clean = df_core_qa.drop_duplicates(subset=['Title']).dropna(subset=['Year'])
df_core_qa_clean['Year'] = df_core_qa_clean['Year'].astype(int)

df_core_si_clean = df_core_si.drop_duplicates(subset=['Title']).dropna(subset=['Year'])
df_core_si_clean['Year'] = df_core_si_clean['Year'].astype(int)

trend_core_qa = df_core_qa_clean.groupby('Year').size().reset_index(name='QA_Count')
trend_core_si = df_core_si_clean.groupby('Year').size().reset_index(name='SI_Count')
core_df = pd.merge(trend_core_qa, trend_core_si, on='Year', how='outer').fillna(0).sort_values('Year')
core_df = core_df[(core_df['Year'] >= 2012) & (core_df['Year'] <= 2026)]

# -------------------------------------------------------------
# 4. ΣΧΕΔΙΑΣΜΟΣ ΣΥΓΧΩΝΕΥΜΕΝΟΥ ΓΡΑΦΗΜΑΤΟΣ (SUBPLOTS)
# -------------------------------------------------------------
# Δημιουργία ενός μεγάλου καμβά με 2 γραφήματα σε 1 σειρά και 2 στήλες
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8), facecolor='white')
plt.rcParams['font.family'] = 'sans-serif'

# ----- ΑΡΙΣΤΕΡΟ ΓΡΑΦΗΜΑ (GLOBAL TREND) -----
ax1.plot(global_df['Year'], global_df['QA_Count'], marker='o', markersize=8, linestyle='-', linewidth=3, color='#2CA02C', label='Total Biomedical QA')
ax1.plot(global_df['Year'], global_df['SI_Count'], marker='s', markersize=8, linestyle='--', linewidth=3, color='#D62728', label='Total Biomedical SI')

ax1.set_title('Global Scopus Trend: Biomedical QA vs SI (2012-2026)', fontsize=16, fontweight='bold', pad=15)
ax1.set_xlabel('Publication Year', fontsize=14, labelpad=10)
ax1.set_ylabel('Number of Publications', fontsize=14, labelpad=10)
ax1.set_xticks(range(2012, 2027))
ax1.tick_params(axis='x', rotation=45, labelsize=11)
ax1.tick_params(axis='y', labelsize=11)
ax1.grid(True, axis='y', linestyle='--', alpha=0.7)
ax1.grid(True, axis='x', linestyle=':', alpha=0.4)
ax1.legend(fontsize=12, loc='upper left', frameon=True, shadow=True, facecolor='white')

# ----- ΔΕΞΙ ΓΡΑΦΗΜΑ (BIOASQ CORE TREND) -----
ax2.plot(core_df['Year'], core_df['QA_Count'], marker='o', markersize=8, linestyle='-', linewidth=3, color='#2CA02C', label='BioASQ QA (Scopus)')
ax2.plot(core_df['Year'], core_df['SI_Count'], marker='s', markersize=8, linestyle='--', linewidth=3, color='#D62728', label='BioASQ SI (Scopus)')

ax2.set_title('BioASQ Scopus Trend: QA vs SI (2012-2026)', fontsize=16, fontweight='bold', pad=15)
ax2.set_xlabel('Publication Year', fontsize=14, labelpad=10)
ax2.set_ylabel('Number of Publications', fontsize=14, labelpad=10)
ax2.set_xticks(range(2012, 2027))
ax2.tick_params(axis='x', rotation=45, labelsize=11)
ax2.tick_params(axis='y', labelsize=11)
ax2.grid(True, axis='y', linestyle='--', alpha=0.7)
ax2.grid(True, axis='x', linestyle=':', alpha=0.4)
ax2.legend(fontsize=12, loc='upper left', frameon=True, shadow=True, facecolor='white')

# -------------------------------------------------------------
# 5. ΑΠΟΘΗΚΕΥΣΗ
# -------------------------------------------------------------
plt.tight_layout()
output_file = 'Merged_Scopus_Trends.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f" Το συγχωνευμένο γράφημα δημιουργήθηκε επιτυχώς: '{output_file}'\n")
plt.show()