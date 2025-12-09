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
| Sub-Criteria                           | Data Source (Valuation Report)           | Data Type        | Quantified?                           | Manual Review Trigger                                      |
| -------------------------------------- | ------------------------------ | ---------------- | ------------------------------- | ---------------------------------------------------------- |
| Suburb quality                         | Section 4 – “Location”         | Qualitative text | ✔ Convert to presence/absence patterns | If mentioned **“inferior”**, **“limited”**, **“poor amenity”**                   |
| Proximity to transport, shops, schools | Section 4 – “Location”         | Qualitative text | ✔ Key word search                         | If valuer does **not** mention accessibility -> requires manual judgment                                 |
| Neighbourhood character                | Section 4 – “Neighbourhood”    | Qualitative      | ✔                               | If valuer notes **"mixed-use"**, **"industrial influence"**                     |
| Streetscape quality                    | Section 4 – “Neighbourhood”    | Qualitative      | ✔                               | If described as **"poor"**, **"traffic-heavy"**                          |
| Noise / traffic                        | Section 4 – “Site Description” | Qualitative      | ✔                               | If explicityly stated **"noise"**, **"busy road"**                              |
| Adverse influences                     | Section 4                      | Qualitative      | ✔                               | If stated **"no significant views"** -> neutral; if stated **undesirable elements** -> flag  |
