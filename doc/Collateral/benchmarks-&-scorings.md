## **Benchmarks and Scorings**

### **1. Location/Neightbourhood Risk**

### **1.1 Property Address**

### **1.1.1 Suburb socio-economic level**: 
The indices for the suburb socio-economic level are: 
* **IRSD**: Index of Relative Socio-economic Disadvantage
* **IRSAD**: Index of Relative Advantage and Disadvantage

---

#### **1.1.1.1 IRSD Benchmarks**:

**IRSD measures socio-economic disadvantage only.**
Lower IRSD deciles indicate **higher levels of socio-economic stress**, such as low income, unemployment, lower education, and welfare dependence.

From a lender’s perspective, higher socio-economic disadvantage is associated with:

* **Higher default sensitivity**
  
  Greater exposure to income and employment shocks.

* **Weaker price resilience**
  
  Property values tend to fall faster during downturns and recover more slowly.

* **Reduced liquidity on exit**
  
  Smaller buyer pools, longer selling periods, and higher forced-sale discounts

     
---

| IRSD Decile | Interpretation              | Score (V1.0) |
| ----------- | --------------------------- | ------------ |
| 1           | Most disadvantaged          | 10           |
| 2           | Very disadvantaged          | 20           |
| 3           | Disadvantaged               | 30           |
| 4           | Below average               | 40           |
| 5           | Average                     | 50           |
| 6           | Slightly above average      | 60           |
| 7           | Above average               | 70           |
| 8           | Good socio-economic profile | 80           |
| 9           | Very good                   | 90           |
| 10          | Most advantaged             | 100          |

This table is stored in the [`irsd_scoring.py`](./data/irsd_scoring.py) file.

---

#### **1.1.1.2 IRSAD Benchmarks**:

**IRSAD captures both socio-economic advantage and disadvantage.**

Higher IRSAD deciles indicate a **stronger overall socio-economic profile**, reflecting higher incomes, education levels, professional employment, and owner-occupier presence.

From a lender’s perspective, higher IRSAD suburbs are typically associated with:

* **Stronger price stability**

  Lower volatility across market cycles and better capital preservation.

* **Higher market liquidity**

  Deeper buyer demand and faster resale under enforcement.

* **Better long-term value retention**

  Greater resilience to macroeconomic shocks.
  
---

| IRSAD Decile | Interpretation        | Score |
| ------------ | --------------------- | ----- |
| 1            | Most disadvantaged    | 10    |
| 2            | Very disadvantaged    | 20    |
| 3            | Disadvantaged         | 30    |
| 4            | Below average         | 40    |
| 5            | Average               | 50    |
| 6            | Slightly advantaged   | 60    |
| 7            | Moderately advantaged | 70    |
| 8            | Advantaged            | 80    |
| 9            | Very advantaged       | 90    |
| 10           | Most advantaged       | 100   |

This table is stored in the [`irsad_scoring.py`](./data/irsad_scoring.py) file.

---
### **1.1.2 Suburb Crime Level**: 

In residential collateral risk assessment, property value is influenced not only by the physical characteristics of the dwelling, but also by the stability, livability, and long-term sustainability of the surrounding neighbourhood.

Suburb crime level is therefore included as a quantifiable proxy to reflect the following factors:

* **Residential safety and livability**
  Areas with higher crime rates tend to be less attractive to owner-occupiers and tenants, which can negatively affect housing demand.

* **Market demand and liquidity**
  Persistently high crime levels may suppress buyer demand, resulting in reduced market liquidity and longer disposal times

* **Price resilience**
  During market downturns, properties located in higher-crime suburbs are generally more susceptible to price declines and tend to recover more slowly

> [!IMPORTANT]
> Due to file size constraints, raw suburb-level crime datasets are not stored in this repository.
> 
> Data can be obtained directly from [the official source](https://bocsar.nsw.gov.au/statistics-dashboards/open-datasets/criminal-offences-data.html)

> [!IMPORTANT]
> A trimmed dataset is stored in [`suburb_crime_risk_12m_2024_07_to_2025_06.py`](./data/suburb_crime_risk_12m_2024_07_to_2025_06.py) file
>
> The Crime rate only refers within the current 12 months.
> 
> Below are the python codes for trimming the dataset:
```python
import pandas as pd

# =====================================================
# 1. Load raw data
# =====================================================
df = pd.read_csv("SuburbData25Q2.csv")

# =====================================================
# 2. Define 12-month rolling window
# =====================================================
months_12 = [
    "Jul 2024", "Aug 2024", "Sep 2024", "Oct 2024",
    "Nov 2024", "Dec 2024",
    "Jan 2025", "Feb 2025", "Mar 2025",
    "Apr 2025", "May 2025", "Jun 2025"
]

# =====================================================
# 3. Keep required columns only
# =====================================================
base_cols = ["Suburb", "Offence category", "Subcategory"]

# 防止月份列缺失导致 KeyError
selected_cols = base_cols + [c for c in months_12 if c in df.columns]
df_12m = df[selected_cols]

# =====================================================
# 4. Aggregate by suburb + offence category
#    (merge all subcategories)
# =====================================================
category_monthly = (
    df_12m
    .groupby(["Suburb", "Offence category"], as_index=False)[months_12]
    .sum()
)

# =====================================================
# 5. Aggregate to suburb total
#    (all offence categories combined)
# =====================================================
suburb_monthly_total = (
    category_monthly
    .groupby("Suburb", as_index=False)[months_12]
    .sum()
)

# =====================================================
# 6. Compute 12-month total crime count
# =====================================================
suburb_monthly_total["crime_12m"] = (
    suburb_monthly_total[months_12].sum(axis=1)
)

# =====================================================
# 7. Rank suburbs by crime volume (higher = riskier)
# =====================================================
suburb_monthly_total["crime_rank"] = (
    suburb_monthly_total["crime_12m"]
    .rank(method="min", ascending=False)
)

# =====================================================
# 8. Normalise into 0–100 crime risk score
# =====================================================
max_rank = suburb_monthly_total["crime_rank"].max()

suburb_monthly_total["crime_risk_score"] = (
    100 * (suburb_monthly_total["crime_rank"] - 1) / (max_rank - 1)
)

# =====================================================
# 9. Sort by risk (optional but recommended)
# =====================================================
suburb_monthly_total_sorted = (
    suburb_monthly_total
    .sort_values("crime_risk_score", ascending=False)
)

# =====================================================
# 10. Preview result
# =====================================================
suburb_monthly_total_sorted.head(10)
```

#### **Benchmark Table (Version 1.0)**:
| Crime Rank Range | Interpretation      | Risk Level     | Crime Risk Score (1–100) | Notes                   |
| ---------------- | ------------------- | -------------- | ------------------------ | ----------------------- |
| **1–20**         | Very low crime      | Very Low Risk  | **99–80**                | Safe, stable suburb     |
| **21–40**        | Lower than average  | Low Risk       | **79–60**                | Minor crime exposure    |
| **41–60**        | Average crime       | Medium Risk    | **59–40**                | Neutral baseline        |
| **61–80**        | Higher than average | High Risk      | **39–20**                | Noticeable crime issues |
| **81–100**       | Very high crime     | Very High Risk | **19–0**                 | Severe crime concerns   |

---

### **1.2 Zoning**

#### **1.2.1 Residential Zoning Benmchmarks** 

| Code | Zoning Name | Description | Benchmark Score |
|------|-------------|-------------|-----------------|
| R1 | General Residential | Broad range of residential densities and housing types, including multi-dwelling and residential flat buildings, with supporting community and neighbourhood services. | 65 |
| R2 | Low Density Residential | Primarily low-density detached housing with limited redevelopment intensity; the most stable and restrictive urban residential zone. | 80 |
| R3 | Medium Density Residential | Medium-density residential accommodation allowing housing diversity and moderate redevelopment potential. | 55 |
| R4 | High Density Residential | High-density residential development such as apartments, with higher supply elasticity and greater market cycle sensitivity. | 30 |
| R5 | Large Lot Residential | Residential housing in a rural or semi-rural setting, often adjacent to urban areas, with lower density but reduced market liquidity. | 50 |

This table is stored in the [`residential_zoning_scoring.py`](./data/residential_zoning_scoring.py) file.

> [!IMPORTANT]
> Benchmark scores reflect the relative suitability of each residential zoning category for residential collateral purposes.
>  
> Higher scores indicate greater zoning stability, residential focus, and long-term market predictability.
>

> [!CAUTION]
> If the property zoning is **not within standard residential zones (R1–R5)**, the collateral should be treated as **Non-Standard Collateral**.
>
> In such cases, the application should:
> - Be flagged for **manual review**, **or**
> - Apply a **higher zoning risk adjustment** within the scoring framework.
>
> Non-residential zoning benchmark scores reflect the **relative suitability** of each zoning category for residential collateral purposes only.
> Higher scores indicate greater residential compatibility, market acceptance, and long-term value predictability,  
> but **do not imply equivalence to standard residential zoning**.

---

#### **1.2.2 Non-Residential Zoning Benchmark**

| Code | Zoning Name | Zoning Category | Description | Benchmark Score |
|------|------------|----------------|-------------|-----------------|
| RU1 | Primary Production | Rural | Commercial primary industry production including agriculture, aquaculture, forestry, mining and extractive industries. | 10 |
| RU2 | Rural Landscape | Rural | Rural land for primary production compatible with conserved ecological or scenic landscape qualities. | 15 |
| RU3 | Forestry | Rural | Land protected for long-term forestry use, including State forests. | 5 |
| RU4 | Primary Production Small Lots | Rural | Commercial primary production on smaller rural holdings, including emerging agricultural uses. | 20 |
| RU5 | Village | Rural | Mixed-use rural village centres providing residential, retail, business and community services. | 60 |
| RU6 | Transition | Rural | Transitional land between intensive rural uses and more sensitive or urbanised areas. | 25 |
| B1 | Neighbourhood Centre | Business | Small-scale centres providing daily convenience retail, business and community uses, with shop-top housing permitted. | 40 |
| B2 | Local Centre | Business | Centres providing a broad range of commercial, civic, cultural and residential uses servicing a wider catchment. | 35 |
| B3 | Commercial Core | Business | Major centres with intensive retail, office, entertainment and community uses linked to major transport routes. | 15 |
| B4 | Mixed Use | Business | Areas encouraging a wide range of commercial, residential, tourist and community uses. | 30 |
| B5 | Business Development | Business | Business and bulky goods retail uses requiring large floor areas, supporting employment generation. | 10 |
| B6 | Enterprise Corridor | Business | Commercial and industrial development along major transport corridors. | 10 |
| B7 | Business Park | Business | Office and light industrial uses, including high technology industries with specialised economic functions. | 5 |
| B8 | Metropolitan Centre | Business | Global strategic centres (Sydney and North Sydney CBDs) with intensive commercial and mixed uses. | 20 |
| IN1 | General Industrial | Industrial | Wide range of industrial and warehouse uses with compatible activities. | 5 |
| IN2 | Light Industrial | Industrial | Light industrial, warehouse and service industries with limited amenity impact. | 10 |
| IN3 | Heavy Industrial | Industrial | Heavy industrial uses requiring separation due to health or environmental risks. | 0 |
| IN4 | Working Waterfront | Industrial | Industrial and maritime uses requiring direct waterfront access. | 0 |
| SP1 | Special Activities | Special Purpose | Sites with unique characteristics unsuitable for standard zoning categories. | 5 |
| SP2 | Infrastructure | Special Purpose | Land for permanent public or strategic infrastructure such as hospitals, utilities, transport and defence facilities. | 0 |
| SP3 | Tourist | Special Purpose | Areas focused on tourism-related development and visitor accommodation. | 20 |
| RE1 | Public Recreation | Recreation | Public open space and recreational areas including parks and community facilities. | 5 |
| RE2 | Private Recreation | Recreation | Privately owned or managed recreational facilities such as golf courses and racecourses. | 15 |
| E1 | National Parks and Nature Reserves | Environment | Protected national parks and conservation reserves. | 0 |
| E2 | Environmental Conservation | Environment | Land protected for high ecological, scientific, cultural or aesthetic values. | 5 |
| E3 | Environmental Management | Environment | Land with environmental or hazard constraints requiring special management. | 15 |
| E4 | Environmental Living | Environment | Low-impact residential development within environmentally sensitive or scenic areas. | 45 |
| W1 | Natural Waterways | Waterway | Protected natural waterways with high ecological and scenic significance. | 0 |
| W2 | Recreational Waterways | Waterway | Waterways supporting recreation, boating and fishing-related activities. | 5 |
| W3 | Working Waterways | Waterway | Waterways used for commercial shipping, ports and maritime industries. | 0 |

This table is stored in the [`non_residential_zoning_scoring.py`](./data/non_residential_zoning_scoring.py) file.

> [!IMPORTANT]
> Non-residential zoning benchmark scores reflect the relative suitability of each zoning category for residential collateral purposes.
> 
> Higher scores indicate greater residential compatibility, market acceptance, and long-term value predictability.

---

### **1.3 LGA**

#### **1.3.1 IRSAD Benchmark**

| IRSAD Decile | Interpretation        | Score |
| ------------ | --------------------- | ----- |
| 1            | Most disadvantaged    | 10    |
| 2            | Very disadvantaged    | 20    |
| 3            | Disadvantaged         | 30    |
| 4            | Below average         | 40    |
| 5            | Average               | 50    |
| 6            | Slightly advantaged   | 60    |
| 7            | Moderately advantaged | 70    |
| 8            | Advantaged            | 80    |
| 9            | Very advantaged       | 90    |
| 10           | Most advantaged       | 100   |

This table is stored in the [`irsad_scoring.py`](./data/irsad_scoring.py) file.

> [!IMPORTANT]
> At the LGA level, only IRSAD is used as a macro-level socio-economic indicator.
> 
> IRSD is excluded at the LGA level to avoid double counting socio-economic disadvantage already captured at the suburb level.
>
> Other SEIFA indexes, including IER and IEO, are not included in Version 1.0 as their informational overlap with IRSAD is high and their incremental explanatory power at the LGA level is limited.

---

### **1.4 Marketability**

#### **1.4.1 Marketability Benchmarks**

| Level         | Meaning            | Marketability Score |
| ------------- | ------------------ | ------------------: |
| **Very Good** | High demand        |             **100** |
| **Good**      | Normal demand      |              **80** |
| **Average**   | Slow resale        |              **60** |
| **Fair**      | Hard to sell       |              **40** |
| **Poor**      | Very low liquidity |              **20** |

This table is stored in the [`marketability.py`](./data/marketability.py) file.

---

# **2. Land Risk**

## **2.1 Planning & Legal**

### **2.1.1 Zoning Effect**
| Zoning Wording (Valuation Report) | Typical Alternative Expressions | Zoning Outcome Interpretation | Zoning Risk Level | Zoning Score |
|----------------------------------|---------------------------------|-------------------------------|-------------------|--------------|
| Permits single residential property | Residential use is permitted; Zoned for residential purposes; Use is permissible under zoning | Use fully aligns with zoning controls | Low | 100 |
| Residential use is permitted | Existing residential use is permitted; Zoning permits residential use | Use permitted under current zoning | Low | 100 |
| Permitted subject to approval | Permitted subject to council consent; Subject to development approval; Subject to planning consent | Use permitted with conditions | Medium | 70 |
| Zoning allows existing use only | Existing use permitted only; Existing use rights apply; Redevelopment discouraged | Existing use allowed, future development constrained | Medium | 60 |
| Development potential may be limited | Development may be constrained; Planning controls restrict development | Development constrained by planning controls | Medium–High | 50 |
| Non-conforming but existing use | Use is non-conforming; Permitted under existing use rights | Legal non-conformity present | High | 40 |
| Zoning may restrict development | Zoning significantly limits development; Planning controls adversely affect use | Material planning constraints | High | 40 |
| Use is not permitted | Use prohibited; Zoning prohibits the current use; Does not comply with zoning | Use prohibited under zoning | Very High | 20 |

> [!IMPORTANT]
> For 'Unknown' Zoning Effect, it will be scored to '50' as the neutral fallback
> 
> Keywords table has been creatde and saved in [`land_risk_zoning_effect.py`](./data/land_risk_zoning_effect.py) file.
---

### **2.1.2 Overlays**
| Overlay Wording (Valuation Report) | Typical Alternative Expressions | Overlay Outcome Interpretation | Overlay Risk Level | Overlay Score |
|----------------------------------|---------------------------------|-------------------------------|-------------------|---------------|
| No overlays affect the subject property | No known planning overlays apply; No adverse overlays identified | No overlay constraints identified | Low | 100 |
| Overlays apply but are not considered onerous | Overlays are common to the locality; Overlay requirements are manageable | Overlay present with limited impact | Medium | 70 |
| Flood overlay applies | Flood-prone land; Subject to flood controls | Hazard overlay with conditional development controls | Medium | 70 |
| Bushfire overlay applies | Bushfire prone land; BAL requirements apply | Hazard overlay increasing development complexity | Medium | 70 |
| Heritage overlay applies | Subject to heritage controls; Heritage listed property | Development subject to material heritage constraints | High | 40 |
| Environmental protection overlay applies | Environmental overlay affects the site | Development constrained by environmental controls | High | 40 |
| Overlays may materially restrict development | Additional approvals required due to overlays | Significant planning limitation | High | 40 |
| Unknown, no formal searches undertaken | Overlay status not confirmed; No planning certificate obtained | Overlay status unverified, uncertainty present | Very High | 20 |
| Overlay status has not been investigated | Further investigation required | Potential hidden planning constraints | Very High | 20 |

> [!IMPORTANT]
> For 'Unkown' overlay, it will be scored to '50' as the neutral fallback
> 
> Keywords table has been creatde and saved in [`land_risk_overlays.py`](./data/land_risk_overlays.py) file.
---

### **2.1.3 Valuation Risk Alerts**
| Valuation Risk Alert Response | Risk Interpretation | Land Risk Level | Risk Score |
|------------------------------|---------------------|----------------|------------|
| **No** | No critical heritage, location, or environmental issues identified by the valuer | Low | 100 |
| **Yes** | One or more critical heritage, location, or environmental issues identified | Very High | 20 |

> [!IMPORTANT]
> If 'Yes', trigger manual review
> 
> Keywords table has been creatde and saved in [`land_risk_valuation_risk_alerts.py`](./data/land_risk_valuation_risk_alerts.py) file.

---

## **2.2 Title & Encumbrance**

### **2.2.1 Title Search Sighted**
| Title Sighted | Score |
| ------------- | ----: |
| Yes           |   100 |
| No            |    30 |

---

### **2.2.2 Encumbrances/Restriction**
| Status           | Score |
| ---------------- | ----: |
| None             |   100 |
| Minor / standard |    70 |
| Significant      |    40 |
| Unknown          |    50 |

---

## **2.3 Environmental & Physical**

### **2.3.1 Environmental Disclaimer**
| Status                       | Score |
| ---------------------------- | ----: |
| No issues noted              |   100 |
| Disclaimer only              |    70 |
| Known contamination / hazard |    30 |

---

## **2.4 Site Suitability**

### **2.4.1 Site dimensions**
| Site Shape           | Score |
| -------------------- | ----: |
| Regular              |   100 |
| Minor irregular      |    80 |
| Irregular            |    60 |
| Severely constrained |    40 |

---

### **2.4.2 Units/Lot Entitlement**

### **2.4.3 Services**
| Services        | Score |
| --------------- | ----: |
| Fully connected |   100 |
| Partially       |    70 |
| Limited         |    40 |

---
