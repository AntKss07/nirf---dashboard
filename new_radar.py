import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

OVERALL_URL = "https://www.nirfindia.org/Rankings/2025/OverallRanking.html"      # [web:2]
UNIV_URL    = "https://www.nirfindia.org/Rankings/2025/UniversityRanking.html"   # [web:1]
CLG_URL = "https://www.nirfindia.org/Rankings/2025/CollegeRanking.html"         # [web:3]
RESEARCH_URL= "https://www.nirfindia.org/Rankings/2025/ResearchRanking.html" # [web:4]
ENGINEERING_URL="https://www.nirfindia.org/Rankings/2025/EngineeringRanking.html" # [web:5]
MANAGEMENT_URL="https://www.nirfindia.org/Rankings/2025/ManagementRanking.html" # [web:6]
PHARMACY_URL="https://www.nirfindia.org/Rankings/2025/PharmacyRanking.html"   # [web:7]
MEDICAL_URL="https://www.nirfindia.org/Rankings/2025/MedicalRanking.html"     # [web:8]
DENTAL_URL="https://www.nirfindia.org/Rankings/2025/DentalRanking.html"     # [web:9]
ARCHITECTURE_URL="https://www.nirfindia.org/Rankings/2025/ArchitectureRanking.html" # [web:10]
LAW_URL="https://www.nirfindia.org/Rankings/2025/LawRanking.html"           # [web:11]
INNOVATION_URL="https://www.nirfindia.org/Rankings/2025/InnovationRanking.html" # [web:12]
AGRI_URL="https://www.nirfindia.org/Rankings/2025/AgricultureRanking.html" # [web:14]
STATE_URL="https://www.nirfindia.org/Rankings/2025/STATEPUBLICUNIVERSITYRanking.html"   # [web:15]


def fetch_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; HackathonBot/1.0)"
    }
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    return resp.text

def get_top10_from_url(url):
    """
    Generic loader for a NIRF ranking page.
    Returns Top‑10 with Rank, Institute ID, Name, Score.
    """
    html = fetch_html(url)

    # FutureWarning-safe: wrap HTML string in StringIO before read_html. [web:16]
    tables = pd.read_html(StringIO(html))
    df = tables[0].copy()
    df.columns = [c.strip() for c in df.columns]

    # Keep only needed columns if present
    keep = ["Rank", "Institute ID", "Name", "Score"]
    keep = [c for c in keep if c in df.columns]
    df = df[keep]

    # Clean and sort
    df["Rank"] = pd.to_numeric(df["Rank"], errors="coerce")
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
    df = df.dropna(subset=["Rank"]).sort_values("Rank")

    top10 = df[df["Rank"] <= 10].reset_index(drop=True)

    # Remove trailing "More Details ..." from Name. [web:2][web:1]
    top10["Name"] = top10["Name"].str.replace(r"More Details.*", "",
                                              regex=True).str.strip()
    return top10

def make_score_radar(df, title):
    """
    Radar where each axis is an institute and radius is its overall Score. [web:29]
    """
    names = df["Name"].tolist()
    scores = df["Score"].tolist()

    N = len(names)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    scores += scores[:1]

    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)

    ax.plot(angles, scores, linewidth=2, linestyle="solid")
    ax.fill(angles, scores, alpha=0.25)

    plt.xticks(angles[:-1], names, fontsize=8)
    ax.set_rlabel_position(30)
    plt.yticks([20, 40, 60, 80], ["20", "40", "60", "80"],
               color="grey", size=7)
    plt.ylim(0, 100)

    plt.title(title)
    plt.tight_layout()
    plt.show()

def main():
    # ---------- Overall ----------
    overall_top10 = get_top10_from_url(OVERALL_URL)
    print("Overall – Top 10:")
    print(overall_top10[["Rank", "Institute ID", "Name", "Score"]])
    overall_top10.to_csv("nirf_2025_top10_overall.csv", index=False)

    # ---------- University ----------
    univ_top10 = get_top10_from_url(UNIV_URL)
    print("\nUniversity – Top 10:")
    print(univ_top10[["Rank", "Institute ID", "Name", "Score"]])
    univ_top10.to_csv("nirf_2025_top10_university.csv", index=False)

    clg_top10 = get_top10_from_url(CLG_URL)
    print("\nCollege – Top 10:")
    print(clg_top10[["Rank", "Institute ID", "Name", "Score"]])
    clg_top10.to_csv("nirf_2025_top10_clg.csv", index=False)

    research_top10 = get_top10_from_url(RESEARCH_URL)
    print("\nResearch – Top 10:")
    print(research_top10[["Rank", "Institute ID", "Name", "Score"]])
    research_top10.to_csv("nirf_2025_top10_research.csv", index=False)

    engi_top10 = get_top10_from_url(ENGINEERING_URL)
    print("\nEngineering – Top 10:")
    print(engi_top10[["Rank", "Institute ID", "Name", "Score"]])
    engi_top10.to_csv("nirf_2025_top10_engineering.csv", index=False)

    univ_top10 = get_top10_from_url(UNIV_URL)
    print("\nUniversity – Top 10:")
    print(univ_top10[["Rank", "Institute ID", "Name", "Score"]])
    univ_top10.to_csv("nirf_2025_top10_university.csv", index=False)

    man_top10 = get_top10_from_url(MANAGEMENT_URL)
    print("\nManagement – Top 10:")
    print(man_top10[["Rank", "Institute ID", "Name", "Score"]])
    man_top10.to_csv("nirf_2025_top10_management.csv", index=False)

    pharm_top10 = get_top10_from_url(PHARMACY_URL)
    print("\n Pharmacy – Top 10:")
    print(pharm_top10[["Rank", "Institute ID", "Name", "Score"]])
    pharm_top10.to_csv("nirf_2025_top10_pharmacy.csv", index=False)

    medi_top10 = get_top10_from_url(MEDICAL_URL)
    print("\nMedical – Top 10:")
    print(medi_top10[["Rank", "Institute ID", "Name", "Score"]])
    medi_top10.to_csv("nirf_2025_top10_medical.csv", index=False)

    dental_top10 = get_top10_from_url(DENTAL_URL)
    print("\nDental – Top 10:")
    print(dental_top10[["Rank", "Institute ID", "Name", "Score"]])
    dental_top10.to_csv("nirf_2025_top10_dental.csv", index=False)

    arch_top10 = get_top10_from_url(ARCHITECTURE_URL)
    print("\nArchitecture – Top 10:")
    print(arch_top10[["Rank", "Institute ID", "Name", "Score"]])
    arch_top10.to_csv("nirf_2025_top10_architecture.csv", index=False)

    law_top10 = get_top10_from_url(LAW_URL)
    print("\nLaw – Top 10:")
    print(law_top10[["Rank", "Institute ID", "Name", "Score"]])
    law_top10.to_csv("nirf_2025_top10_law.csv", index=False)

    agri_top10 = get_top10_from_url(AGRI_URL)
    print("\nAgriculture – Top 10:")
    print(agri_top10[["Rank", "Institute ID", "Name", "Score"]])
    agri_top10.to_csv("nirf_2025_top10_agriculture.csv", index=False)

    state_top10 = get_top10_from_url(STATE_URL)
    print("\nState Public University – Top 10:")
    print(state_top10[["Rank", "Institute ID", "Name", "Score"]])
    state_top10.to_csv("nirf_2025_top10_state_public_university.csv", index=False)

    # ---------- Charts ----------
   # make_score_radar(overall_top10,
    #                 "NIRF 2025 Overall – Top 10 (Score radar)")     # [web:2]
   # make_score_radar(univ_top10,
   #                  "NIRF 2025 University – Top 10 (Score radar)")  # [web:1]

if __name__ == "__main__":
    main()
