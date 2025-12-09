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
### **2.1 Required for Version 1**
**Valuation Report (PropertyPRO)** (Question: Does which companys matter? For the Valuation Report?)

Provide all core fields needed for Collateral scoring: 
* Property type
* Property location
* High-density indicators
* Structural integrity
* Environmental risks
* Marketability
* Valuer comments
* Final valuation amount
* Risk rating (Low/Med/High)

This document serves as **the single source of truth** for Collateral scoring in V1. 

### **2.2 Future Enhancements (For v2.0)**
> [!IMPORTANT]
> This may be incorporated in V2.0

**Contract of Sale**
* Confirms property purchase details
* Mainly contributes to "Conditions C"

**Title Search / First Mortgage Registration**
* Confirms lender's ability to take first mortgage
* Only available pre-settlement -> not used in V1

**Deposit Receipt**
* Supporting document only
* **Not part of Collateral risk assessment**

---

## **3. Data Inputs Extracted from Valuation Report**
The following fields are expected to be parsed manually in V1 and automatically in V2. 

### **3.1 Property Characteristics**
* Property type (house / townhouse / apartment / high-rise unit)
* Floor area (sqm)
* Year built
* Number of bedrooms / bathrooms
* Car spaces

### **3.2 Location & Environmental**
* Address & postcode
* Metro / non-metro classification
* Location risk rating (if provided)
* Flood risk (if mentioned)
* Bushfire zoning (if mentioned)
* Environmental overlays (if mentioned)

### **3.3 Structural & Physical Condition**
* Structural issues notes (Y/N)
* Maintenance condition (good/fair/poor)
* Evidence of defects
* Evidence of over-capitalisation

### **3.4 Marketability & Valuer Commentart**
* Restricted marketability (Y/N)
* Market demand indicators
* High-density building flag
* Valuer's risk rating (Low/Medium/High)
* Any special comments impacting loan security

### **3.5 Valuation Data**
* Final valuation amount
* Method used (direct comparison/summation/capitalisation)
* Comparable sales
* LVR calculation (requires loan amount -> provided by assessor)

---

## **4. Scoring Variables (Used in V1)**
Only the following variables will contirbute to scoring in Version 1: 
| Variable               | Type             | Weight           | Data Source      |
| ---------------------- | ---------------- | ---------------- | ---------------- |
| Property Type Risk     | categorical      | 15%              | Valuation report |
| Location Category      | categorical      | 20%              | Valuation report |
| High-Density Indicator | boolean          | 10%              | Valuation report |
| Structural Issues      | flag             | Mandatory Review | Valuation report |
| Marketability Rating   | categorical      | 20%              | Valuation report |
| Environmental Risk     | categorical/flag | 10%              | Valuation report |
| Valuation Risk Rating  | categorical      | 25%              | Valuation report |

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

