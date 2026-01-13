# **Collsteral Scoring Module - BLueprint v1.0**
*semi-Automated Scoring Engine*

*Prepared by: Angla Li*

*Version: 1.0 (Initial Prototype)*

---

## **Outline (Version 1 Prototype)**
- [1. Purpose & Scope](#1-purpose--scope)
- [2. Required Documents & Data Sources](#2-required-documents--data-sources)
- [3. Data Inputs (Version 1)](#3-data-inputs-version-1)
- [4. Scoring Framework](#4-scoring-framework)
  - [4.1 Scoring Variables](#41-scoring-variables)
  - [4.2 Weighting Methodology](#42-weighting-methodology)
  - [4.3 Score Calculation Logic](#43-score-calculation-logic)
  - [4.4 Pass/Review Thresholds](#44-passreview-thresholds)
- [5. Flagging Mechanism (High-Level)](#5-flagging-mechanism-high-level)
- [6. Override Mechanism (High-Level)](#6-override-mechanism-high-level)
- [7. System Workflow (V1)](#7-system-workflow-v1)
- [8. Outputs](#8-outputs)
- [9. Known Limitations (Version 1)](#9-known-limitations-version-1)
- [10. Future Enhancements](#10-future-enhancements)


---

## **1. Purpose & Scope**
The **Collateral** module provides a *structural framework* for assessing the security property used for the loan. 

Version 1 (v1.0) focuses on establishing the **foundational scoring structure**, while recognising that many assessment elements will still require **manual judgment**. 

The objective of this prototype are to: 
* Define a consistent set of inputs sourced from the **Valuation Report**
* Introduce a standardised method for capturing and interpreting property risk factors
* Highlight cases that may require manual review or escalation
* Create a modular scoring framework that can be progressively automated in future versions

---

## **2. Required Documents (Data Sources)**

### **2.1 Required for Version 1 (V1 Prototype)**

For Version 1, the **Collateral scoring module relies exclusively on the Valuation Report** provided by an accredited valuer (e.g., PropertyPRO, Opteon, API valuers).
No additional documents are required at this stage.

The valuation report is currently the **sole authoritative document** used by the credit team to assess property security risk.
V1 mirrors this process and focuses only on fields already reviewed manually today.

---

## **2.2 Core Data Required from the Valuation Report (V1 Scope)**

The **minimum dataset** needed to run Collateral scoring consists primarily of:

### **A. The 8 Valuer Risk Analysis Ratings (Primary Inputs for V1)**

These are the **core drivers** of Collateral scoring.
Each rating ranges from **10 to 100** (100 = low risk, 10 = high risk).

1. **Location / Neighbourhood Risk**
2. **Land Risk** (planning, title, zoning)
3. **Environmental Issues Risk**
4. **Improvements / Building Condition Risk**
5. **Market Direction (Price Trend)**
6. **Market Activity**
7. **Local / Regional Economy Impact**
8. **Market Segment Conditions**

---

## **2.3 Current Data Access Model (Today’s State)**

* Credit assessors manually review the valuation report when performing Collateral assessment.
* Assessors will enter selected property details into the CRM system.
* For V1, the scoring tool can rely on:

  * **Manual user input** (entered into the Streamlit form), and/or
  * **Future CRM field exports** (if needed for automation).

V1 does **not require automated document parsing**; this may be introduced in future versions.

---

## **2.4 Source-of-Truth Statement**

For Version 1, the **Valuation Report** is the **single source of truth** for all Collateral scoring inputs.
Future versions may incorporate:

* External market datasets
* Risk overlays (flood, bushfire, environmental maps)
* CRM-integrated data pipelines
* Automated extraction from valuation PDFs
  
---

## **3. Data Inputs Extracted from Valuation Report**
The following fields are expected to be parsed manually in V1 and automatically in V2. 

### **3.1 Location / Neighbourhood Risk**
Measures how the surrounding neighbourhood affects property stability, demand, and resale recoverability. 

**Main factors**:
* Property Address
* Zoning
* LGA
* Marketability

> [!TIP]
> For detailed data source information for each Valuer, please [view detailed data source documentation](./data_source.md)


### **3.2 Land Risk**
Assesses constraints affecting use, development, title clarity, or land value volatility. 

**Valuer Considers**:
* Zoning category
* Planning restrictions
* Title encumbrances (easements, coenants, shared access)
* Flood overlays / heritage controls
* Land size suitability
* Site shape & topography
* Any adverse planning notices

### **3.3 Environmental Issues Risk**
Evaluates exposure to natural hazards or environmental contamination. 

**Valuer Considers**:
* Flood risk
* Bushfire zones
* Coastal erosion
* Contamination or environmental remediation
* Noise & air pollution (highways, industrial zones)
* Surrounding hazardous facilities
* Soil stability

### **3.4 Improvements / Building Condition Risk**

Assesses physical condition, age, quality, and maintenance of the dwelling. 

**Valuer Considers**:
* Age of building
* Construction quality
* Wear & tear / required repairs
* Structural movement (cracks, dampness, subsidence)
* Renovation quality
* Maintenance history
* Defects notes during inspection
* Compliance with building codes

### **3.5 Marekt Direction**

Reflects the direction of property values in the immediate area. 

**Valuer Considers**:
* Recent comparable sales
* Local price movement trends
* Buyer demand growth or decline
* Market cycle position (Rising, stable, declining)

### **3.6 Marekt Acitivity**

Measures how active the market is in terms of new listings, sales turnover, and liquidity

**Valuer Considers**:
* Days on market (DOM)
* Volume of transactions
* Auction clearance environment
* New listings supply levels
* Off-the-plan competition nearby

### **3.7 Local / Regional Economy Impact**

Assesses risk from the economic conditions affecting the suburb or region

**Valuer Considers**: 
* Local employment stability
* Infrastructure projects (positive or negative)
* Local business closures
* Economic reliance on a single industry
* Population growth or decline

### **3.8 Market Segment Conditions**
Measure risk within the specific market segment (e.g., apartments vs houses, luxury vs affordable)

**Valuer Considers**:
* Relative demand for this property type
* Competition from similar stock
* Segment-specific supply pressures
* Buyer demographics stability
* Performance or similar properties (rental vs sale markets)

---

## **4. Scoring Variables (Used in V1)**
Only the following variables will contirbute to scoring in Version 1: 
| Variable               | Type             | Weight           | Data Source      |
| ---------------------- | ---------------- | ---------------- | ---------------- |
| Location/Neighbourhood     | categorical      | 14%              | Valuation report & APIs |
| Land      | categorical      | 14%              | Valuation report |
| Environmental Issues | categorical          | 14%              | Valuation report |
| Improvements      | categorical             | 14% | Valuation report |
| Market Direction   | categorical      | 14%              | Valuation report |
| Market Activity     | categorical | 14%              | Valuation report |
| Local/Regional Economy Impact  | categorical      | 8%              | Valuation report |
| Market Segment Conditions  | categorical      | 8%              | Valuation report |

Total scoring weight = **100%** (flags override score)

---

## **5. Flagging Rules (System Flags Requiring Manual Review)**
The tool will raise a **FLAG** whenever elevated risk is detected. 

### **5.1 Automatic Flags**
* **Structural issues present** (cracks, major defects, damp, safety issues)
* **Restricted marketability**
* Property is **high-density unit < 40 sqm**
* Property located in **high-risk postcode** (mapping to be provided by lender)
* **Environmental overlays** (flood, bushfire, contamination -> if mentioned)
* **Valuer assigns HIGH risk rating**
* Over-capitalisation concerns
* Property is **company title** or **leasehold** (if mentioned)

### **5.2 Flag Behaviour**
* System score is still calculated
* Module cannot auto-approve Collateral
* Senior credit assessor must manually review and override
* Tool records: "Flag raised: Manual review required before proceeding."

---

## **6. Override Rules (Senior Lender Authorisation Required)**
The following flagged items may be overridden by authorised personnel: 

### **Override Flags**
* High-density but LVR < 60%
* Restricted marketability but strong resale evidence exists
* Minor structural issues but valuer confirms minimal impact
* High risk rating but strong compensating factors (e.g., very low LVR)

### **Non-Overridable (Hard Fail)**
* Severe structural instability (foundation, major cracks)
* Property deemed unsuitable as security by valuer
* Non-residential property presented for residential loan
* Illegal or unapproved construction

Override decisions must be logged in the credit file.

---

## **7. Scoring Logic (Version 1 Prototype)**
### **7.1 Scoring Scale**

Each variable contributes a weighted score between 0-100. 

### **7.2 Proposed Grading Bands**
| Score Range | Grade | Meaning                            |
| ----------- | ----- | ---------------------------------- |
| 85–100      | A     | Excellent security                 |
| 70–84       | B     | Acceptable security                |
| 55–69       | C     | Borderline security                |
| < 55        | D     | High risk → requires manual review |

### **7.3 Interaction Between Score & Flags**
* If **any critical flag triggers -> auto manual review**, regardless of score
* If no flags + score ≥ passing threshold -> auto-proceed to next C

### **7.4 Simple Example**
A standard suburban apartment with:
* No issues
* Medium risk rating
* Acceptable marketability

Likely scores: 
> ⭐ Type Risk (15/15)
> 
> ⭐ Location (18/20)
> 
> ⭐ Marketability (18/20)
> 
> ⭐ High-density (8/10)
> 
> ⭐ Risk Rating Medium (18/25)
> 
> ⭐ Environmental (8/10)

Final score = **85 -> Grade A -> Pass**

---

## **8. Output**
The Collateral module produces:
> ✔ Collateral Score (0-100)
> 
> ✔ Grade (A/B/C/D)
> 
> ✔ Flags Summary
> 
> ✔ Override Required? (Y/N)
> 
> ✔ Recommended next step (Proceed / Manual Review Required)

---

> [!TIP]
> This is a tip.

> [!WARNING]
>

> [!IMPORTANT]
> Something important here.

****
---

