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
| **Factors**        | **Data Source (Valuation Report)**         | **Example**                                                                                                  | **Data Type** | **Quantified**                                                                                           | **Manual Review Trigger**                       |
|--------------------|---------------------------------------------|--------------------------------------------------------------------------------------------------------------|---------------|-----------------------------------------------------------------------------------------------------------|--------------------------------------------------|
| [Property Address](#property-address)   | Section 1 - Property Summary                | 26/16 Middleton Avenue, Castle Hill NSW 2154                                                                 | Text          | Yes, but must link with APIs or a suburb-scoring table                                                    | If the score for this suburb is low             |
| [Zoning](#zoning)             | Section 1 - Property Summary                | R4 High Density Residential / The Hills LEP 2019                                                             | Text          | Yes, requires a zoning scoring table (e.g., R2–R4 scale)                                                  | If the score for zoning is low                  |
| [LGA](#lga)                | Section 1 - Property Summary                | The Hills Shire Council                                                                                      | Text          | Yes, but must link with APIs or build a council economic index                                            | If the LGA score is low                         |
| [Marketability](#marketability)      | Section 1 - Property Summary                | Good                                                                                                         | Text          | Yes, create a valuation-level scoring (e.g., Poor / Fair / Good / Very Good)                              | If marketability is assessed as low             |

---
#### **Property Address**:
The property address determines the suburb—and the suburb determines the property’s exposure to:
* socio-economic strength
* crime rate

**These data may come from:**

| Data (High-level only, Version 1.0) | Source | Indices - Benchmarks |
|-------------------------------------|--------|---------|
| Suburb socio-economic level | [ABS (Australian Bureau of Statistics)](https://www.abs.gov.au/statistics/people/people-and-communities/socio-economic-indexes-areas-seifa-australia/latest-release#data-downloads) | [IRSD Benchmarks](./benchmarks-&-scorings.md#1111-irsd-benchmarks) & [IRSAD Benchmarks](./benchmarks-&-scorings.md#1112-irsad-benchmarks) |
| Suburb crime level | [NSW Bureau of Crime Statistics and Research (BOCSAR) – Criminal Offences Open Datasets](https://bocsar.nsw.gov.au/statistics-dashboards/open-datasets/criminal-offences-data.html) | [Suburb Crime Level](./benchmarks-&-scorings.md#112-suburb-crime-level) |

> [!IMPORTANT]
> Other data or indicators like population growth, infrastructure accessibility, school quality, employment access, etc. can be considered in future versions.

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
| **SEIFA by LGA** | [ABS (Australian Bureau of Statistics)](https://www.abs.gov.au/statistics/people/people-and-communities/socio-economic-indexes-areas-seifa-australia/latest-release#data-downloads) |[IRSAD Benchmarks](./benchmarks-&-scorings.md#131-irsad-benchmarks)

> [!IMPORTANT]
> SEIFA by LGA is sufficient for Version 1.0, as it captures overall socio-economic conditions including affluence, education, and employment at the LGA level.
>
> More granular indicators such as infrastructure spending, development approvals, crime rates, and economic specialisation may be considered in future versions once additional data coverage and stability are established.

---

#### **Marketability**:
Marketability reflects the valuer's judgment about 
* ease of sale
* buyer demand
* liquidity
* attractiveness relative to comparable properties

**The benchmarks**:
| Level     | Meaning            | Risk Level |
| --------- | ------------------ | ---------- |
| Very Good | High demand        | Low        |
| Good      | Normal demand      | Medium-Low |
| Average   | Slow resale        | Medium     |
| Fair      | Hard to sell       | High       |
| Poor      | Very low liquidity | Very High  |

**Data Obtain**:
Directly from the valuation report. 

> [!IMPORTANT]
> Delete factors which are considered as too complex at this stage. These data should be carried further in the future version.
---

