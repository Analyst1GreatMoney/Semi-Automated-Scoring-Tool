# **Collsteral Scoring Module - BLueprint v1.0**
*semi-Automated Scoring Engine*

*Prepared by: Angla Li*

*Version: 1.0 (Initial Prototype)*

---

## **1. Purpose & Scope**
The **Collateral** module assesses the *quality, risk,and recoverability* of the security property used for the loan. 

The purpose of this scoring module is to:
* Identify risks associated with the property as loan security
* Automate key parts of the Collateral evaluation
* Flag cases requiring manual review by a senior credit assessor
* Provide an objective, consistent scoring standard for the Five-C framework

This module is **Version 1 (Prototype)** and focuses only on the information available from the **Valuation Report**. 

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

---

