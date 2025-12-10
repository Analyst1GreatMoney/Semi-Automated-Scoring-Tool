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
| Zoning             | Section 1 - Property Summary                | R4 High Density Residential / The Hills LEP 2019                                                             | Text          | Yes, requires a zoning scoring table (e.g., R2–R4 scale)                                                  | If the score for zoning is low                  |
| LGA                | Section 1 - Property Summary                | The Hills Shire Council                                                                                      | Text          | Yes, but must link with APIs or build a council economic index                                            | If the LGA score is low                         |
| Marketability      | Section 1 - Property Summary                | Good                                                                                                         | Text          | Yes, create a valuation-level scoring (e.g., Poor / Fair / Good / Very Good)                              | If marketability is assessed as low             |
| Location           | Section 4 - Land                            | Well-serviced suburb (shopping centre, schools, transport); approx. 30 km NW of Sydney CBD                   | Text          | Yes, convert key indicators into a scoring model (transport, amenities, employment corridor strength etc.) | If location-based scoring is low                |
| Neighbourhood      | Section 4 - Land                            | Established residential neighbourhood; mix of dwellings of varying age, style, and construction               | Text          | Yes, identify neighbourhood stability indicators and apply a scoring table                                 | If neighbourhood stability score is low         |

#### **Property Address**:
