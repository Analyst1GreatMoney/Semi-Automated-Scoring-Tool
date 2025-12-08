# **Five-C Scoring Tool -- Requirements Intake Template** 

*A structured requirement-gathering document for discussions with lending stakeholders.*

--- 

### **1.Project Overview**
**Purpose:**
To gather functinal and scoring logic requirements for building a semi-automated Five-C credit assessment tool (**A semi-automated lending decision engine**). 

**Stakeholders to Interview:**
* Senior Credit Analyst
* Senior Lender / Lending Manager
* Credit Policy Representative

---

### **2.Current Business Process**

**Questions to Clarify the Existing Workflow:**

**A.Overall Decision Flow**

1. How does the assessor currently move through the Five Cs?
   * Is it strictly sequential (C1 -> C2 -> C3....)?
   * Or do they sometimes revisit earlier Cs?
     
2. What is the current scoring model (if any)?
   * How are scores calculated today?
   * Is there an existing formula, or is it assessor judgment?
     
3. What are the passing thresholds for each C?
   * e.g., "80+ = pass", "65-80 = caution", "<65 = fail"
     
4. When a C fails (score < threshold), what is the exact escalation process?
   * Who performs manual review?
   * What additional checks are required?

-----

**B.Inputs & Data Sources**

5. What data does the assessor pull from CRM today? 
* What does the data looks like in the CRM that is used for credit assessment?
* What are the key information that has to be considered in the credit assessment engine?
* Does all the data are needed in the CRM dataset to be applied in the credit assessment engine?

6. What borrower documents are required for each C?
* For Conditions:
  * fskdjflsd
* For Capacity:
  * sjdfhsdlfl
* For Capital:
  * djkfsdkfjs
* For Character:
  * sdjfkhsdkjfhk
* For Collateral:
  * sdfdjsfhskd

7. Which input fields are structured vs unstructured?
* Structured: salary, NDI, LVR
* Unstructured: valuer comments, employment stability remarks

----

**C.Quantitative vs Qualitative Assessment**

9. For each checklist item, which parts are purely quantitative?
* e.g., DTI, NDI, LVR, Equifax score

10. Which qualitative items must be converted to a numeric score?
* e.g., "employment stability", "location risk", "borrower behaviour"

11. Are there qualitative elements that cannot be quantified and must remain manual?

----

**D.Manual Review & Overrides**

12. Under what conditions does the assessor override the system?
* Can high scores compensate low ones?
* Who authorises overrides?

13. Is there a documented guideline for overrides?
* Or does it depend on assessor judgment?

14. Should the tool recommend manual review or require it?

----

**E.Pain Points & Bottlenecks**

15. Which parts of the current assessment take the most time?
* Reviewing documents?
* Extracting numbers?
* Cross-checking CRM data?

16. Where do inconsistencies occur between assessors?
* Scoring differenes?
* Interpretation of borrower documents?

17. Which manual tasks are most prone to human error?

----

**F.Automation Boundaries**

18. Which steps can be fully automated without losing accuracy?

19. Which steps should remain human-only, and why?
* AML red flags?
* Interpretation of income stability?

20. What level of automation is acceptable?
* 60% automated?

----

**G.Future Integration & Scaling**

21. Should the system store historical scoring results for auditing?

22. Do assessors need a PDF summary report?
   
**Notes:**
* Map out the end-to-end workflow:

  *Borrow submission -> Document collection -> Data extraction -> C-by-C scoring -> Flagging -> Manual review -> Final decision*

* 
---

### **3.Required Inputs (Per C)**
Aligned with Great Money's Five-C Credit Assessment Checklist

### **Conditions**: 
These inputs correspond directly to the business process and responsible lending requirements. 
**Mandatory Inputs**
* Confirmation of adequately verified submission pack
* QA (Quality Assurance) check status
* Loan purpose (e.g., investment, owner-occupied, bridging, interest-only)
* Loan type and repayment structure
* Supporting document required (Y/N + description)
* Evidence that Responsible Lending Final Assessment is completed

**Notes / Logic Questions**
* Which loan purposes increase risk?
* Are certain purposes disallowed or require escalation?
* What constitutes an "adequately verified" pack?

--- 

### **Capacity**
Direcly aligned with the fields in the checklist. 

**Financial Inputs**
* Serviceability calculations
  * Net Disposable Income (NDI)
  * Debt-to-Income ratio (DTI)
  * NSR / other internal ratios
* Credit report key indicators (e/g/. Equifax score, repayment arrears)
* Borrower's gross and net income
  * Income type: PAYG, self-employed, casual, contractor
  * Income stability (months/year in role)
* Net assets and savings
  * Liquidity level
  * Genuine savings
* Employment or business trading history
* Other liabilities and commitments
  * Personal loans
  * Credit cards
  * HECS
  * Child support, etc.

**Notes / Logic Questions**
* What minimum NSR/NDI threshold determines "pass/fail"?
* Does casual income require shading?
* Any hard stops for poor Equifax scores?

---

### **Capital**
Based on equity, assets and liabilities, and wealth position. 

**Inputs Needed**
* Equity level and loan size
  * Loan Amount
  * Property Value
  * Loan-to-Value Ratio (LVR)
* Borrower savings record
  * Demonstrated saving pattern
  * Liquidity assessment
* Asset accumulation evidence
* Assets & Liabilities breakdown
  * Net asset position
  * Negative net wealth triggers?
* Overall equity composition
  * Gifted equity (Y/N)
  * Parental guarantee?
 
**Notes / Logic Questions**
* What minimum LVR tiers correspond to low vs medium vs high risk?
* How is gifted equity treated in scoring?
* Do certain asset classes receive weighting?

---

### **Character**
Based on behavioural, credit history, and stability indicators. 

**Inputs Required**
* Credit history
  * Equifax score
  * Number of negative events (defaults, late payments)
  * Any judgments or bankruptcies
* KYC & AML check results
  * Verification status
  * Any red flags
* Borrower residential stability
  * Length of residence
  * Frequency of moves
  * Rent vs owner-occupier
* Employment or business stability
  * Time in current job/business
  * Gaps in employment
* Asset or income accumulation pattern
  * Consistency over time
  * Irregularities or volatility

**Notes / Logic Questions**
* What constitutes an "unstable" employment pattern?
* Does a certain Equifax score automatically downgrade this C?
* Can Character override other Cs?

---

### **Collateral**
Based on the security property and valuation risk. 

**Inputs Needed**
* Valuation report - overall risk rating
  * Valuer comments
  * Any structural issues
* First registered mortgage confirmation
* Location of the property
  * Metro / non-metro / regional
* Property location category
  * High-risk postcodes
  * Flood, fire, environmental overlays
* Property type
  * House, townhouse, apartment, high-density
* Any valuer flags
  * Restricted marketability
  * Poor condition
  * Over-capitalisation

**Notes / Logic Questions**
* Which property types are considered higher risk?
* Does postcode risk affect LVR thresholds?
* How should valuation risk (Low/Med/High) influence scoring?

--- 

### **4.Required Outputs**
* Score for each individual C
* Weighted total score
* Risk band classification (e.g., "Low / Medium / High")
* System recommendation (Approve / Refer / Decline)
* Supporting reasoning or notes

---

### **5.Scoring Rules and Logic**
**Questions to Ask**:
* Is each C scored independently or interdependently?
* What are the scoring ranges (e.g., 1-5, 1-10?)
* Weighting for each C in total score?
* Minimum score for approval?
* Which rules are strict ("hard declines")
* Which rules allow overrides and who can approve them?

**Rulebook Information Required**:
* Definitions of each scoring band
* Examples of typical borrower profiles and expected scores
* Edge cases (e.g., inconsistent income, no credit file, special-purpose loans)

---

### **6.Validation Requirements**
* Which data points need validation? (e.g., income must be numeric, NSR > 1.0)
* Which missing data should block the assessment?
* Which fields are optional but recommended?

---

### **7.User Experience & Interface Requirements**
* Who are the primary users?
* What does a "simple and clean" UI mean for the team?
* Do they prefer:
  * one-page form?
  * step-by-step wizard?
  * collapsible sections per C?
* Output format needed:
  * on-screen only?
  * PDF report?
  * exportable summary?

--- 

### **8.Review and Approval Process**
* Who'signs off on the scoring logic?
* Who reviews prototype scoring results?
* How many feedback rounds to expect?
* Who has authority to approve logic changes in the future?
