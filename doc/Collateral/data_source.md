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
* rental demand
* population growth
* infrastructure accessibility
* school quality
* employment access

**These data may come from:**
| Data                 | Source                                |
| -------------------- | ------------------------------------- |
| SEIFA, demographics  | ABS (Australian Bureau of Statistics) |
| Crime rate           | NSW BOCSAR                            |
| Rental data          | SQM Research, Domain API, CoreLogic   |
| Population growth    | ABS                                   |
| Transport access     | TfNSW Open Data                       |
| Distance to CBD/jobs | ABS Journey-to-Work datasets          |

> [!IMPORTANT]
> Delete factors which are considered as too complex at this stage. These data should be carried further in the future version. 

---

#### **Zoning**:
Zoning directly affects allowed density, future supply risk, neighbourhood character, likelihood of oversupply, long-term price stability. 

**To obtain the data**:
| Data                        | Source                                                 |
| --------------------------- | ------------------------------------------------------ |
| Zoning maps                 | NSW Planning Portal                                    |
| LEP zoning rules            | Local Council LEP                                      |
| Future development pipeline | Cordell Construction Database, NSW Planning DA Tracker |

> [!IMPORTANT]
> Delete factors which are considered as too complex at this stage. These data should be carried further in the future version.
---

#### **LGA**: 
LGAs differ significantly in economic strength, infrastructure investment, goverance quality, planning controls, crime and safety, long-term community stability

**For benchmark and indicator data**:
| Data                            | Source                        |
| ------------------------------- | ----------------------------- |
| SEIFA by LGA                    | ABS                           |
| LGA economic indicators         | .idcommunity profiles         |
| Council infrastructure planning | Annual council budget reports |
| Crime                           | BOCSAR                        |
| DA approvals                    | NSW Planning Portal           |

> [!IMPORTANT]
> Delete factors which are considered as too complex at this stage. These data should be carried further in the future version.
---

#### **Marketability**:
Marketability reflects the valuer's judgment about ease of sale, buyer demand, liquidity, and attractiveness relative to comparable properties. 

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

