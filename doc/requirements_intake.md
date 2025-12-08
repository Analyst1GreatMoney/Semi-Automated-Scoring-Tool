# **Five-C Scoring Tool -- Requirements Intake Template** 

*A structured requirement-gathering document for discussions with lending stakeholders.*

--- 

### **1. Project Overview**
**Purpose:**
To gather functinal and scoring logic requirements for building a semi-automated Five-C credit assessment tool. 

当然可以！我先给你一份**专业、简洁、银行咨询级别的 Requirement Intake Template（需求访谈模板）**，格式适合放进：

* GitHub repo（作为 `/docs/requirements_intake.md`）
* 需求会议（你带进去问问题）
* 与 senior lender 对齐 scoring 逻辑

我会写成 Markdown 版本，这样你可以直接复制到 GitHub。

---

# ✅ **Five-C Scoring Tool — Requirements Intake Template**

*A structured requirement-gathering document for discussions with lending stakeholders.*

---

## **1. Project Overview**

**Purpose:**
To gather functional and scoring logic requirements for building a semi-automated Five-C credit assessment tool.

**Stakeholders to Interview:**

* Senior Credit Analyst
* Senior Lender / Lending Manager
* Credit Policy Representative (if applicable)

---

## **2. Current Business Process**

**Questions:**

* How is the Five-C assessment currently performed?
* What inputs do credit assessors rely on for each C?
* Which parts are quantitative vs qualitative?
* Where are inconsistencies or pain points today?
* Which steps should remain manual (if any)?

**Notes:**

* Describe the full workflow from borrower application → assessment → decision → documentation.
* Identify steps that can be automated vs maintained as human judgement.

---

## **3. Required Inputs (Per C)**

### **Character**

* Borrower behaviour indicators used?
* Past repayment history / arrears?
* Qualitative behaviours considered? (E.g., communication, compliance)
* How is Character scored today?

### **Capacity**

* Required income components?
* Required liabilities?
* Which financial ratios are used? (e.g., DSR, NSR)
* Stress rate used? Who defines it?

### **Capital**

* Net asset calculation approach?
* Which asset types count?
* Are certain assets weighted differently?

### **Collateral**

* Required property information?
* LVR calculation rules?
* Valuation method used (desktop / full valuation)?
* Any loan-to-value thresholds (e.g., >80% needs extra conditions)?

### **Conditions**

* How is loan purpose assessed?
* Are industry risks or economic conditions incorporated?
* Is this qualitative only, or partially quantitative?

---

## **4. Required Outputs**

* Score for each individual C
* Weighted total score
* Risk band classification (e.g., “Low / Medium / High”)
* System recommendation (Approve / Refer / Decline)
* Supporting reasoning or notes

---

## **5. Scoring Rules and Logic**

### **Questions to Ask:**

* Is each C scored independently or interdependently?
* What are the scoring ranges? (e.g., 1–5, 1–10?)
* Weighting for each C in total score?
* Minimum score for approval?
* Which rules are strict (“hard declines”)?
* Which rules allow overrides and who can approve them?

### **Rulebook Information Required:**

* Definitions of each scoring band
* Examples of typical borrower profiles and expected scores
* Edge cases (e.g., inconsistent income, no credit file, special-purpose loans)

---

## **6. Validation Requirements**

* Which data points need validation?
  (e.g., income must be numeric, NSR > 1.0)
* Which missing data should block the assessment?
* Which fields are optional but recommended?

---

## **7. User Experience & Interface Requirements**

* Who are the primary users?
* What does a “simple and clean” UI mean for the team?
* Do they prefer:

  * one-page form?
  * step-by-step wizard?
  * collapsible sections per C?
* Output format needed:

  * on-screen only?
  * PDF report?
  * exportable summary?

---

## **8. Review and Approval Process**

* Who signs off on the scoring logic?
* Who reviews prototype scoring results?
* How many feedback rounds to expect?
* Who has authority to approve logic changes in the future?

---

## **9. Future Considerations (Optional)**

(Not required for Version 1, but good to align early.)

* Integration with CRM or loan application data
* Historical data import for machine-learning assisted scoring
* Audit log for decisions
* Version control of scoring logic

---

# 📌 Should This Template Be Stored in the GitHub Repo?

### **✔ Yes — but only in the `/docs` folder.**

Why?

* It shows professionalism
* It documents the logic behind your tool
* It helps future developers / reviewers understand how the scoring model was designed
* It’s a standard practice in real software projects

**Recommended structure:**

```
/project-root
│
├── streamlit_app/
│   └── main.py
│
├── docs/
│   ├── requirements_intake.md   ← 放这里
│   ├── scoring_logic.md         ← 之后使用
│   └── versioning_notes.md
│
└── README.md
```

不要放在根目录，因为根目录应该保持干净。

---

# 如果你愿意，我可以帮你进一步产出：

### ✔ **scoring_logic.md 模板（你之后要填的）**

### ✔ **First prototype UI 文案（展示 Version 1）**

### ✔ **GitHub README.md（专业、干净、银行级格式）**

只要告诉我：“帮我写 scoring_logic template / README / V1 UI wording”，我马上给你。
