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
| **Sub-Criteria**                                         | **Data Source (Valuation Report)**                                 | **Data Type**    | **Quantified?**                                                | **Manual Review Trigger**                                                                              |
| -------------------------------------------------------- | ------------------------------------------------------------------ | ---------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Suburb quality & demographics**                        | Section 4 – *Location*                                             | Qualitative text | ✔ Convert to indicators (e.g., “established”, “inferior”)      | If terms like **“inferior”**, **“poor amenity”**, **“limited appeal”** appear                          |
| **Proximity to employment, transport, shops, amenities** | Section 4 – *Location*                                             | Qualitative text | ✔ Keyword search (“close to”, “within walking distance”, etc.) | If valuer does **not** mention accessibility → manual judgment                                         |
| **Neighbourhood character**                              | Section 4 – *Neighbourhood*                                        | Qualitative      | ✔                                                              | If valuer mentions **“mixed-use”**, **“industrial influence”**, **“commercial encroachment”**          |
| **Streetscape quality**                                  | Section 4 – *Neighbourhood*                                        | Qualitative      | ✔                                                              | If described as **“poor streetscape”**, **“untidy surrounds”**, **“dense traffic”**                    |
| **Noise / traffic exposure**                             | Section 4 – *Site Description*                                     | Qualitative      | ✔                                                              | If explicitly mentions **“noise”**, **“busy road”**, **“traffic-heavy”**                               |
| **Crime & safety perception**                            | Section 4 – *Neighbourhood*, Section 4 – *Location* (if mentioned) | Qualitative      | ✔ Convert to sentiment (safe / neutral / unsafe)               | If words like **“high crime”, “safety concern”, “undesirable area”** appear                            |
| **Adverse environmental / visual influences**            | Section 4 – *Location / Neighbourhood / Site*                      | Qualitative      | ✔                                                              | If mentions **“power lines”, “substation”, “industrial site”, “waste facility”, “unsightly elements”** |

