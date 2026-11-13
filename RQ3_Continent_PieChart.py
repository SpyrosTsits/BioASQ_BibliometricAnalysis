import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Φόρτωση των δεδομένων
filename = "Table_2_Country_Statistics.csv"
try:
    df = pd.read_csv(filename)
except FileNotFoundError:
    print(f"Το αρχείο '{filename}' δεν βρέθηκε.")
    exit()

df = df[df['Country'] != 'Generic / Unidentifiable'].reset_index(drop=True)

# 2. Λεξικό Αντιστοίχισης (Χώρες σε Ηπείρους)
continent_mapping = {
    "Greece": "Europe", "UK": "Europe", "Germany": "Europe", "France": "Europe",
    "Spain": "Europe", "Italy": "Europe", "Switzerland": "Europe", "Bulgaria": "Europe",
    "Portugal": "Europe", "Romania": "Europe", "Belgium": "Europe", "Poland": "Europe",
    "Norway": "Europe", "Czech Republic": "Europe", "Netherlands": "Europe", "Sweden": "Europe",
    "Ireland": "Europe", "Denmark": "Europe", "Lithuania": "Europe",
    "USA": "North America", "Canada": "North America",
    "China": "Asia", "Russia": "Asia", "Japan": "Asia", "South Korea": "Asia",
    "India": "Asia", "Singapore": "Asia", "Turkey": "Asia", "Pakistan": "Asia",
    "Taiwan": "Asia", "Israel": "Asia", "Bangladesh": "Asia",
    "Australia": "Oceania",
    "Colombia": "South America", "Brazil": "South America",
    "Algeria": "Africa", "Tunisia": "Africa", "Morocco": "Africa"
}

df['Continent'] = df['Country'].map(continent_mapping).fillna('Other')

# Ομαδοποίηση ανά Ήπειρο
continent_df = df.groupby('Continent')['Total_Mentions'].sum().reset_index()
continent_df = continent_df.sort_values(by='Total_Mentions', ascending=False)

pie_labels = list(continent_df['Continent'])
pie_values = list(continent_df['Total_Mentions'])

# 3. Σχεδιασμός Γραφήματος
plt.figure(figsize=(12, 9))
colors = plt.cm.Set2.colors[:len(pie_labels)]


# Εμφανίζουμε ποσοστά ΜΟΝΟ αν είναι >= 3%
def autopct_generator(pct):
    return ('%1.1f%%' % pct) if pct >= 3.0 else ''


wedges, texts, autotexts = plt.pie(
    pie_values, labels=pie_labels, autopct=autopct_generator, startangle=140,
    colors=colors, wedgeprops={'edgecolor': 'black', 'linewidth': 1},
    textprops={'fontsize': 12}, pctdistance=0.75, labeldistance=1.1
)

for autotext in autotexts:
    autotext.set_fontweight('bold')

# 4. Annotations (Βελάκια) για τα μικρά ποσοστά (< 3%)
bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center")

total = sum(pie_values)
for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1) / 2. + p.theta1
    pct = (pie_values[i] / total) * 100

    if pct < 3.0:
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        plt.annotate(f"{pct:.1f}%", xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                     horizontalalignment=horizontalalignment, **kw, fontsize=11, fontweight='bold')

plt.title('Geographical Distribution of Research Contributions in BioASQ By Continent', fontsize=16,
          fontweight='bold', pad=30)
plt.tight_layout()

output_pie = 'BioASQ_Continent_Distribution_Pie_Final.png'
plt.savefig(output_pie, dpi=300)
print(f"Το  κυκλικό διάγραμμα αποθηκεύτηκε ως '{output_pie}'")
plt.show()