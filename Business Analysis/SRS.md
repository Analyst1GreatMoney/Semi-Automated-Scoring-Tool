## System Requirements Specification

### Executive Summary


---

### 1. Introduction

👉 让非技术 Stakeholder 5 分钟内明白：
* 这是一个什么系统
* 为什么要做
* 给谁用
* 解决什么业务痛点

---

#### 1.1 Purpose

**This subsection will:**

* Clarify how this document will be used to guide the design, development, and evaluation of the Credit Scoring Engine
* Define the scope of the document as a single source of requirements for both business and technical stakeholders
* Establish the document as a shared reference point to align business expectations with system behaviour
* Ensure that the content remains accessible and understandable to non-technical stakeholders, while still providing sufficient clarity for technical implementation

**Key focus:**

* How the document is used
* Who the document is for
* How it bridges business and technical perspectives

---

#### 1.2 Business background and Current State

**This subsection will:**

* Describe Great Money’s current lending business at a high level, including how credit decisions are made within the organisation
* Explain that credit analysis is conducted using the Five C’s credit framework, with assessments performed across multiple dimensions
* Outline how credit assessments are currently carried out as a predominantly manual, analyst-led process
* Describe the current reliance on:
  * Individual analyst judgement
  * Manual review of supporting documents (e.g. valuation reports, policy references)
  * Experience-based interpretation rather than system-supported analysis

* Summarise the operational characteristics of the current approach, such as:
  * Time-intensive assessment workflows
  * High dependence on analyst availability and expertise
  * Limited standardisation across individual assessments

**Key focus:**

* Current business model and operating process
* How credit analysis is performed today
* AS-IS state, without proposing solutions

---

#### 1.3 Project Objectives

**This subsection will:**

* Describe the organisation’s objective to introduce a system-supported credit analysis capability to complement the existing manual assessment process
* Clarify that the system is designed to support analyst decision-making, rather than fully automate credit decisions
* Explain the intent to partially delegate repeatable and standardised analysis tasks to the system in order to:
  * Reduce manual workload and operational costs
  * Improve consistency and transparency in assessments
  * Enhance scalability as assessment volumes increase

* Define the scope of the project as focusing on Collateral risk within the Five C’s credit framework, while acknowledging that other dimensions (Character, Capacity, Capital, and Conditions) remain outside the current project scope
* Articulate the target operating model in which:
  * The system performs structured risk assessment and scoring
  * Alerts and flags are generated at predefined risk points
  * Manual review is initiated selectively, based on system output and professional judgement

* Establish the objective of providing explainable and auditable outputs to support internal risk governance and compliance requirements

**Key focus:**

* Target-state credit analysis operating model (TO-BE)
* Clear definition of project scope and boundaries
* Role of the system versus human judgement

---

#### 1.4 Stakeholders 

**This subsection will:**

* Identify the primary and secondary stakeholders associated with the Credit Scoring Engine
* Clarify each stakeholder group’s role in the credit analysis process and their interaction with the system
* Establish clear boundaries of responsibility between business users, governance functions, and technical teams
* Support shared understanding of stakeholder expectations throughout system design, development, and use

**Identified Stakeholders**

*Credit Analysts*

* Primary users of the system
* Responsible for performing credit analysis and interpreting system outputs
* Use alerts and risk indicators to support professional judgement and decision-making

*Credit Managers*

* Secondary users with review and escalation responsibilities
* Responsible for overseeing high-risk or non-standard cases
* May perform or approve manual reviews and overrides in accordance with policy

*Risk and Compliance*

* Governance stakeholders responsible for ensuring alignment with credit policy and regulatory requirements
* Rely on system outputs to support consistency, transparency, and auditability of credit decisions
* Provide input into risk rules, thresholds, and control requirements

*IT / Development Team*

* Technical stakeholders responsible for system design, implementation, and maintenance
* Use this SRS as a reference to translate business requirements into technical solutions
* Ensure system behaviour aligns with defined functional and non-functional requirements

**Key focus:**

* Clear identification of stakeholder groups
* High-level role definition without operational detail
* Alignment of responsibilities across business and technical functions

---

### 2. System Overview

Provide a high-level view of the system, its boundaries, key components, and user interactions, to ensure a shared understanding between business and technical stakeholders before detailing functional requirements.

📌 是否画图：✅ 建议画 1 张图（非常加分）
📌 图类型：High-Level System Architecture / Context Diagram

**这张图的目的（不是为了好看)**

* 明确系统边界（system boundary）
* 区分 system 内 vs system 外
* 帮 non-technical stakeholder 快速理解：
> “人在哪里？系统在哪里？输入从哪来？输出到哪去？”

**图中应包含的元素（你列得是完全对的）**

* User
* Credit Scoring Engine
* External Inputs
  * Valuation Report
  * Credit Policy / Risk Rules

* Outputs
  * Risk Score
  * Alerts / Flags
  * Recommendation

---

#### 2.1 System Description

**This subsection will:**

* Describe the system as a semi-automated Credit Scoring Engine designed to support credit analysis
* Clarify that the system assists decision-making rather than making final credit decisions autonomously
* Summarise the system’s primary function as assessing risk and generating structured outputs for analyst review

---

##### 2.1.1 Inputs

**This subsection will outline:**

* Identify the high-level categories of information required by the Credit Scoring Engine to perform collateral-related risk assessment
* Clarify that input definitions are intentionally abstracted to support flexibility across different assessment contexts
* Establish that detailed field-level definitions and policy-specific checklists are outside the scope of this document

**Input Categories**

The system requires the following categories of information to support collateral assessment:

* **Collateral-related information**
  Information describing the asset offered as collateral, including characteristics relevant to valuation, marketability, and risk exposure.

* **Location-related information**
  Information describing the geographic and environmental context of the collateral, which may influence risk assessment outcomes.

* **Policy and risk rule information**
  Relevant credit policy guidelines, risk thresholds, and rule definitions used to inform system logic and risk interpretation.

* **Analyst-provided information**
  Supplementary inputs provided by analysts to support or contextualise the assessment, where required.

**Input Sources**

* Inputs to the system may be derived from multiple sources, including but not limited to:
  * Valuation reports and supporting documentation
  * Internal credit policy documents and risk guidelines
  * Analyst-entered or confirmed information

**Scope and Constraints**

* This section does not define detailed data fields, formats, or validation rules
* The system does not replace upstream eligibility checks or policy gates
* Detailed implementation of policy-specific rules and checklists is outside the scope of this document

**Key focus:**

* Clear definition of input categories and sources
* Explicit separation between system requirements and policy implementation
* Alignment with a collateral-focused project scope

---

##### 2.1.2 Outputs

**This subsection will outline:**

* The system outputs generated as part of the assessment, including:
  * Risk score
  * Alerts and flags
  * Risk-based recommendation

* That outputs are intended to:
  * Support analyst judgement
  * Highlight potential risk concerns
  * Inform further review or escalation where required

📌 重点：
输出是“支持决策”，不是“替代决策”

---

#### 2.2 User roles 

**This subsection will:**

* Identify the key user roles interacting with the system
* Describe each role’s responsibilities and level of interaction at a high level
* Clarify separation of duties between system execution and human decision-making

##### 2.2.1 Credit Analyst

* Primary user of the system
* Responsible for:
  * Entering or reviewing input information
  * Interpreting risk scores, alerts, and recommendations
  * Exercising professional judgement based on system outputs

##### 2.2.2 Manager (Review/Override)

* Secondary user with review and oversight responsibilities
* Responsible for:
  * Reviewing flagged or escalated cases
  * Approving or performing manual overrides where appropriate
  * Ensuring decisions align with credit policy and governance requirements

##### 2.2.3 System 

* Represents automated system behaviour
* Responsible for:
  * Processing inputs
  * Applying predefined risk rules and scoring logic
  * Generating outputs in a consistent and repeatable manner

---

#### 2.3 Eligibility Gates (Overview)

##### 2.3.1 Purpose of Eligibility Gates

**This subsection will:**

* Explain that eligibility gates are used to determine whether an application should proceed to detailed credit analysis
* Clarify that gates function as pre-assessment controls, not risk scoring mechanisms
* Establish gates as a cost- and efficiency-driven control to prevent ineligible cases from entering downstream analysis

---

##### 2.3.2 Position of Gates in the Credit Assessment Process

**This subsection will:**

* Describe where gates occur within the overall credit workflow
* Clarify that eligibility gates are applied before any Five C’s assessment begins
* Establish that passing a gate does not imply approval, but eligibility to proceed

---

##### 2.3.3 Gate Ownership and Policy Alignment

**This subsection will:**

* Clarify that eligibility gates are defined and governed by internal credit policy
* Establish that the system does not create or modify gate rules
* Define the system’s role as executing or supporting gate checks based on policy-defined criteria

---

##### 2.3.4 Gate Execution Model

**This subsection will:**

* Describe a hybrid execution approach, where:
  * Certain eligibility checks may be system-executed
  * Others may require manual confirmation or approval

* Clarify that gate outcomes may be:
  * Automatically determined
  * Externally confirmed prior to system use
  * Manually reviewed in exceptional cases

 ---

 ##### 2.3.5 Relationship Between Gates and Risk Assessment

**This subsection will:**

* Clearly separate eligibility gates from risk assessment activities
* Establish that:

Gates determine whether analysis occurs

Risk assessment determines how risky an eligible application is

Confirm that eligibility gates operate independently from Collateral or other Five C’s assessments

### 3. Functional Requirements

📌 是否画图：✅ 必须
📌 是否需要 Use Case：✅ 必须（至少 1–2 个）
📌 是否需要 Business Process Map：✅ 建议

---

#### 3.1 User Input & Data Capture

📌 图：Optional（表格即可）

用户输入哪些字段

哪些是必填 / 选填

哪些来自 valuation report

📌 用 表格，不是文字堆砌

---

#### 3.2 Risk Assessment modules

📌 图：❌ 不需要画，但要结构化

每个模块都要有：

Description

Inputs

Scoring logic（高层，不是代码）

Outputs

Risk flags

---

#### 3.3 Scoring logic

📌 图：Optional（流程图可加分）

单项评分 → 权重 → 总分

风险等级划分（Low / Medium / High）

推荐动作（Approve / Review / Decline）

---

#### 3.4 Alerts & flags


##### 3.4.1 Purpose of Alert & Flags

可以这样写（逻辑示意）：

Alerts & Flags 用于在风险评估过程中

标识潜在异常、政策偏离或高风险情形

提供 透明、可解释的风险提示

不直接改变评分结果


##### 3.4.2 Types of Alerts

这里你要体现的是：
👉 系统是“有层级、有逻辑”的，而不是乱报警

🔹 Risk Alerts（风险类）

高风险 zoning

不利 planning overlays

环境/土地限制

🔹 Policy Alerts（政策类）

超出 policy 推荐阈值

非标准使用场景

🔹 Data Quality Alerts（数据类）

缺失关键信息

模糊或不一致描述

##### 3.4.3 Alert Trigger Conditions

你不需要写代码，但要写清楚 触发“条件逻辑”：

If zoning classification ∈ High Risk category → trigger alert

If multiple moderate risks occur simultaneously → trigger alert

If valuation wording contains uncertainty → trigger alert

📌 用 If / When / Where 句式
📌 不要用“系统会判断”这种模糊话

##### 3.4.4 Alert Severity Levels

你可以设计 Severity Level，哪怕只有 3 级：

Informational

Warning

Critical

并说明：

不同等级对用户行为的影响建议

哪些通常会引导 Manual Review

📌 注意措辞：
👉 “recommend review” 而不是 “force review”

##### 3.4.5 Alert Presentation & Explanation

这部分你可以非常克制地写：

Alert message should be concise

Provide brief explanation

Reference underlying risk factor

📌 不写 UI 细节
📌 写 信息设计原则

##### 3.4.6 Relationship with Manual Review

你可以明确写：

Alerts & Flags do not automatically initiate manual review

They support user judgement

Manual Review remains a separate, discretionary process

📌 这句话本质上是在说：
👉 系统辅助人，而不是替代人

---

#### 3.5 Manual override

📌 图：❌ 文字 + 条件说明即可

必须写清楚：

谁可以 override

override 记录什么

是否保留原始系统评分

audit trail

---

### 4. Use Case Section

📌 是否画图：✅ 必须（Use Case Diagram）

这一章的目的

👉 从“用户角度”描述系统行为

---

### 5. Business Process Map

#### 5.1 End-to-end assessment flow

✅ End-to-End Business Process Flow

流程示例：

Receive application

Input property data

System calculates risk

Analyst reviews

(Optional) Manager override

Final decision

---

### 6. Non-Functional Requirements

#### 6.1 Explainability

#### 6.2 Auditability

#### 6.3 Performance

#### 6.4 Security (role-based access)

#### 6.5 Maintainability

---

### 7. Assumption & Constraints

📌 是否画图：❌ 不需要

数据来源可靠

非生产级系统

政策规则可能变化

---

### 8.Out of Scope

📌 是否画图：❌ 不需要

不做自动放贷

不接外部信用局

不做实时审批
