## 📘 Data Source Reference for Collateral Risk Analysis Variables
This document explains **where each data point comes from, how it should be interpreted**, and **how it will be used** in the Collateral scoring module (Version 1). 

The aim is ensure that everyone has a **consistent understanding** of: 
* What information is available from the Valuation Report
* Which fields can be used directly for scoring
* Which fields require interpretation or manual review

This document acts as the **reference guide** for building and validating the Collateral scoring logic. 

---

### **🧭 Scope (Version 1)**
* Version 1 relies only **on the Valuation Report** as its data source.
* All data must come from sections that credit assessors already use today.
* If a field is not clearly stated in the report, it will not be included in V1 scoring.
* Additional data sources (CRM, external APIs, overlays) may be introduced in future versions.

--- 
### **📑 About the Tables Below**
For each of the **eight Valuer Risk Analysis Variables**, the following information is provided: 
* **Valuer considerations** as reflected in the report
* **Where the data appears** in the Valuation Report (section-by-section)
* **Data type** (numeric, categorical, boolean, qualitative text)
* Whether a field can be **converted into structured scoring logic**
* **Manual review triggers** for cases where automation may not be reliable

---

### **1. Location / Neighbourhood Risk**
| **Factors**        | **Data Source (Valuation Report)**         | **Example**                                                                                                  | **Data Type** | **Quantified**                                                                                           |
|--------------------|---------------------------------------------|--------------------------------------------------------------------------------------------------------------|---------------|-----------------------------------------------------------------------------------------------------------|
| [Property Address](#property-address)   | Section 1 - Property Summary                | 26/16 Middleton Avenue, Castle Hill NSW 2154                                                                 | Text          | Yes, but must link with APIs or a suburb-scoring table                                                    | 
| [Zoning](#zoning)             | Section 1 - Property Summary                | R4 High Density Residential / The Hills LEP 2019                                                             | Text          | Yes, requires a zoning scoring table (e.g., R2–R4 scale)                                                  |
| [LGA](#lga)                | Section 1 - Property Summary                | The Hills Shire Council                                                                                      | Text          | Yes, but must link with APIs or build a council economic index                                            |
| [Marketability](#marketability)      | Section 1 - Property Summary                | Good                                                                                                         | Text          | Yes, create a valuation-level scoring (e.g., Poor / Fair / Good / Very Good)                              |

---
#### **Property Address**:
The property address determines the suburb—and the suburb determines the property’s exposure to:
* socio-economic strength
* crime rate

**These data may come from:**

| Data (High-level only, Version 1.0) | Source | Indices - Benchmarks | Weighting |
|-------------------------------------|--------|---------|---------|
| Suburb socio-economic level | [ABS (Australian Bureau of Statistics)](https://www.abs.gov.au/statistics/people/people-and-communities/socio-economic-indexes-areas-seifa-australia/latest-release#data-downloads) | [IRSD Benchmarks](./benchmarks-&-scorings.md#1111-irsd-benchmarks) & [IRSAD Benchmarks](./benchmarks-&-scorings.md#1112-irsad-benchmarks) | 50% |
| Suburb crime level | [NSW Bureau of Crime Statistics and Research (BOCSAR) – Criminal Offences Open Datasets](https://bocsar.nsw.gov.au/statistics-dashboards/open-datasets/criminal-offences-data.html) | [Suburb Crime Level](./benchmarks-&-scorings.md#112-suburb-crime-level) | 50% |

> [!IMPORTANT]
> Other data or indicators like population growth, infrastructure accessibility, school quality, employment access, etc. can be considered in future versions.
>
> The Suburb IRSD and IRSAD data is stored in [`suburb_irsd_irsad.py`](./data/suburb_irsd_irsad.py) 
>
> Suburb Crime data is stored in [`suburb_crime_risk_12m_2024_07_to_2025_06.py`](./data/suburb_crime_risk_12m_2024_07_to_2025_06.py) 

---

#### **Zoning**:
Zoning determines the **density level** of the area. Density strongly infleunces: 
* supply risk
* potential for oversupply
* neighbourhood stability
* long-term price resilience

**To obtain the data**
| Data                           | Source                                                                                                                                                                                                                                           |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Zoning Category | [NSW Planning Portal – Standard Instrument LEP Residential Zones (Practice Note PN 11-002)](https://www.planning.nsw.gov.au/sites/default/files/2023-04/practice-note-pn-11-002-preparing-leps-using-the-standard-instrument-standard-zones.pdf) |


> [!IMPORTANT]
> Zoning Category captures 80% of zoning risk. LEP rules and development pipeline can be considered in the future versions.
>
> For benchmarks and scorings, please view [Zoning Benchmarks](./benchmarks-&-scorings.md#12-zoning)

---

#### **LGA**: 
Different LGAs vary significantly in:
* economic strength
* safety
* infrastructure quality
* community stability

**Data to obtain**:
| Data             | Source                                |Indices - Benchmarks |
| ---------------- | ------------------------------------- |---------|
| **SEIFA by LGA** | [ABS (Australian Bureau of Statistics)](https://www.abs.gov.au/statistics/people/people-and-communities/socio-economic-indexes-areas-seifa-australia/latest-release#data-downloads) |[IRSAD Benchmarks](./benchmarks-&-scorings.md#131-irsad-benchmark)

> [!IMPORTANT]
> SEIFA by LGA is sufficient for Version 1.0, as it captures overall socio-economic conditions including affluence, education, and employment at the LGA level.
>
> The trimmed dataset for LGA's IRSAD can be found in [`lga_irsad_2021_clean.py`](./data/lga_irsad_2021_clean.py) file
>
> More granular indicators such as infrastructure spending, development approvals, crime rates, and economic specialisation may be considered in future versions once additional data coverage and stability are established.

---

#### **Marketability**:
Marketability reflects the valuer's judgment about 
* ease of sale
* buyer demand
* liquidity
* attractiveness relative to comparable properties

**Reference Table**:
| Level     | Meaning            | Risk Level |
| --------- | ------------------ | ---------- |
| Very Good | High demand        | Low        |
| Good      | Normal demand      | Medium-Low |
| Average   | Slow resale        | Medium     |
| Fair      | Hard to sell       | High       |
| Poor      | Very low liquidity | Very High  |

> [!IMPORTANT]
> Marketability is taken directly from the valuation report as a consolidated expert judgment and is not supplemented with external indices in Version 1.0.
>
> For benchmarks and scorings, please click [here](./benchmarks-&-scorings.md#141-marketability-benchmark)

---

### **2. Land Risk**

| Valuer Lens | Core Question |
|------------|---------------|
| **[Planning & Legal](#planning--legal)** | Is the land legally and planning-wise permitted for its intended use? |
| **[Title & Encumbrance](#title--encumbrance)** | Is the ownership clear and free from material encumbrances? |
| **[Environmental & Physical](#environmental--physical)** | Are there physical or environmental constraints that affect usability or value? |
| **[Site Suitability](#site-suitability)** | Is the site practically usable and readily marketable? |

---

### **Planning & Legal**

| Factor | Source from | Example | Data Type | Quantified | Manual Review Rules |
|-------|-------------|---------|-----------|------------|---------------------|
| **[Zoning Effect](#zoning-effect)** | Section 4 – Land | Permits single residential property | Text | Yes – scoring table based on zoning outcome categories | Yes |
| **[Overlays](#overlays)** | Section 8 – Additional Comments | Unknown, no formal searches undertaken | Text | Yes – scoring table based on overlay status categories | Yes |
| **[Valuation Risk Alerts](#valuation-risk-alerts)** | Section 8 – Additional Comments | No | Text | Yes – binary benchmark table | Yes |

---

#### **Zoning effect**

#### **Purpose**

Zoning effect assesses whether the land is legally permitted for its existing and intended use under the applicable planning framework. It represents a core **Planning & Legal** factor, as zoning controls define allowable land use and development potential. 

#### **Data source and type**

The data is directly sourced from **Valuation Report**, including the zoning classification and a brief description of permitted land use. 

#### **Impact**

It identifies potential legal or planning constraints that may restrict use, redevelopment, or future sale of the property. 

#### **Typical contents**

**For Low Risk:**
| Wording in Valuation Report | 
|----------------------------|
| *Permits single residential property* |
| *Residential use is permitted* | 
| *Zoned for residential purpose* | 
| *Zoning permits residential use* | 
| *Use as a dwelling is permissible* | 
| *Use is permitted under the current zoning* |
| *The existing residential use is permitted* | 
| *Zoning allowes standard residential development* | 
| *The land is appropriately zoned for its current use* |
| *The zoning is consistent with the existing use* | 

---

**For Medium Risk: (Permitted with Conditions)**
| Wording in Valuation Report | 
|----------------------------|
| *Permitted subject to council approval* |
| *Permitted subject to planning consent* | 
| *Permitted subject to development approval* | 
| *Use is permissible subject to conditions* | 
| *Development is subject to planning controls* | 
| *Permitted with restrictions* |

---

**For Medium Risk: (Permitted to redevelop)**
| Wording in Valuation Report | 
|----------------------------|
| *Zoning allows existing use only* |
| *Existing use is permitted, however redevelopment may be limited* | 
| *Zoning permits current use but limits further development* | 
| *Development potential may be restricted* | 
| *Zoning does not encourage redevelopment* | 
| *Further development may be constrained* |

---

**For High Risk: (Non-conforming)**
| Wording in Valuation Report | 
|----------------------------|
| *Non-conforming but existing use* |
| *Existing use rights apply* | 
| *Use is permitted under existing use rights* | 
| *The property benefits from existing use rights* | 
| *The use is not strictly compliant with zoning* | 
| *Use is inconsistent with zoning but tolerated* |

---

**For High Risk: (Materially constrained)**
| Wording in Valuation Report | 
|----------------------------|
| *Zoning may restrict development* |
| *Zoning significantly limits development potential* | 
| *Planning controls adversely affect development* | 
| *Use is restricted under current planning controls* | 
| *Zoning constraints impact the highest and best use* | 

----

**For Very High Risk: (Prohibited use)**
| Wording in Valuation Report | 
|----------------------------|
| *Use prohibited* |
| *Use is not permitted* | 
| *Zoning prohibits the current use* | 
| *The existing use is not permitted under zoning* | 
| *Use is inconsistent and not permissible* | 
| *Development is prohibited* | 
| *The use does not comply with planning controls* | 

> [!IMPORTANT]
> For benchmarks, please view [Zoning Effect Benchmarks](./benchmarks-&-scorings.md#211-zoning-effect)

---

#### **Overlays**

#### **Purpose**
Overlays assess whether additional planning, environmental, heritagem or hazard-related controls apply to the land beyond the base zoning. It imposes supplementary restrictions that affect land use, development feasibility, or approval certainty. 

#### **Data source and type**
The data is sourced directly from the **Valuation Report**. It reflects whether formal overlays searches have been undertaken on whether overlay constraints are known. 

#### **Impact**
Overlays may introduce additional planning or legal constraints that increase approval complexity, restrict development outcomes, or elevate uncertainty around land use. Where overlays are present, unclear, or not formally assessed, the associated land risk increases and may warrant further investigation or manual review. 

#### **Typical contents**

**For Low Risk:**
| Wording in Valuation Report | 
|----------------------------|
| *No overlays affect the subject property* |
| *The property is not affected by any planning overlays* | 
| *No known heritage, environmental or hazard overlays apply* | 
| *No adverse planning overlays identified* | 
| *No material overlays impacting use or development* | 

---

**For Medium RIsk:**
| Wording in Valuation Report | 
|----------------------------|
| *The property may be subject to planning overlays* |
| *Overlays apply but are not considered onerous* | 
| *Flood overlay applies; however, no adverse impact noted* | 
| *Bushfire overlay applies, subject to standard controls* | 
| *Overlays are common to the locality* | 
| *Overlay requirements are manageable* | 

---

**For High Risk:**
| Wording in Valuation Report | 
|----------------------------|
| *Heritage overlay applies* |
| *Environmental protection overlay affects the site* | 
| *Significant flood overlay impacting development* | 
| *Bushfire prone land with BAL requirements* | 
| *Overlays may materially restrict development* | 
| *Additional approvals required due to overlays* |

---

**Very High Risk:**
| Wording in Valuation Report | 
|----------------------------|
| *Unknown, no formal searches undertaken* |
| *Overlay status has not been confirmed* | 
| *No planning certificate has been obtained* | 
| *The valuer has not undertaken formal overlay investigations* | 
| *Further investigation is required to determine overlay impact* | 

---

#### **Valuation Risk Alerts** 

Question for this Valuation Risk Alerts: 

***Is the subject property critically affected by any heritage, location or environmental issues?***

#### **Purpose**
Valuation Risk Alerts assess whether the subject property is **critically affected by any heritage, location, or environmental issues** that may materially impact land use, development feasibility, or market value. 

#### **Data source and type**
The data is sourced directly from **Valuation Report**. It is presented as a **binary qualitative assessment** (e.g. *Yes / No*), based on the valuer's professional judgment rather than detailed technical investigations. 

#### **Impact**
Where valuation risk alerts are identified, they indicate the presence of **material issues** that may adversely affect the property's usability, approval certainty, or value stability. 

| Valuation Risk Alert Response | Practical Meaning | Land Risk Interpretation | Review Implication |
|------------------------------|-------------------|--------------------------|--------------------|
| **No** | The valuer has not identified any critical heritage, location, or environmental issues affecting the subject property | No material exceptional risks identified beyond standard planning considerations | No immediate action required |
| **Yes** | The valuer has identified one or more critical heritage, location, or environmental issues that may materially impact the property | Presence of high-impact, non-standard risks that may affect usability, value, or approval certainty | Mandatory manual review and further due diligence required |

---

### **Title & Encumbrance**

title search:


encumbrance:



### **Environmental & Physical**

environmental disclari:


### **Site Suitability**

site dimensions:


Service: 

