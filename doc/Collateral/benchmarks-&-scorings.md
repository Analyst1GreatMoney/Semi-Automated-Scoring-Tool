## **Benchmarks and Scorings**

### **1. Location/Neightbourhood Risk**

### **1.1 Property Address**

### **1.1.1 Suburb socio-economic level**: 
The indices for the suburb socio-economic level are: 
* **IRSD**: Index of Relative Socio-economic Disadvantage
* **IRSAD**: Index of Relative Advantage and Disadvantage

---

#### **1.1.1.1 IRSD Benchmarks**:

**IRSD focuses only on disadvantage.**
It ranks suburbs based on the **concentration of socio-economic stress**, including:
* Low household income
* High unemployment
* Lower education attainment
* Higher welfare dependence
* Higher proportion of low-skill occupations
* Housing stress and rental dependence

A **lower IRSD decile = higher socio-economic disadvantage.**

---

From a lender’s perspective, high socio-economic disadvantage is associated with:

**1. Higher default sensitivity**

   Residents in disadvantaged areas are more exposed to:
   * Income shocks
   * Employment instability
     
**2. Higher downside price volatility**
   * Property values fall faster in downturns
   * Recovery is slower after market stress
     
**3. Weaker liquidation outcomes**
   * Narrower buyer pool
   * Longer selling periods
   * Larger forced-sale discounts
     
---

| IRSD Decile | Interpretation              | Score (V1.0) |
| ----------- | --------------------------- | ------------ |
| 1           | Most disadvantaged          | 10           |
| 2           | Very disadvantaged          | 20           |
| 3           | Disadvantaged               | 30           |
| 4           | Below average               | 40           |
| 5           | Average                     | 50           |
| 6           | Slightly above average      | 60           |
| 7           | Above average               | 70           |
| 8           | Good socio-economic profile | 80           |
| 9           | Very good                   | 90           |
| 10          | Most advantaged             | 100          |

This table is stored in the [`irsd_scoring.py`](./data/irsd_scoring.py) file.

---

#### **1.1.1.2 IRSAD Benchmarks**:

**IRSAD captures both advantage and disadvantage.**
In addition to disadvantage factors, it includes:
* High household income
* Higher education levels
* Professional employment
* Dual-income households
* Higher owner-occupier rates

A **higher IRSAD decile = stronger overall socio-economic profile.**

---

High IRSAD suburbs typically show:
1. Stronger price stability
   * Lower volatility across cycles
   * Better capital preservation
2. Higher market liquidity
   * Deeper buyer demand
   * Faster resale under enforcement
3. Better long-term value retention
   * More resistant to macroeconomic shocks

---

| IRSAD Decile | Interpretation        | Score |
| ------------ | --------------------- | ----- |
| 1            | Most disadvantaged    | 10    |
| 2            | Very disadvantaged    | 20    |
| 3            | Disadvantaged         | 30    |
| 4            | Below average         | 40    |
| 5            | Average               | 50    |
| 6            | Slightly advantaged   | 60    |
| 7            | Moderately advantaged | 70    |
| 8            | Advantaged            | 80    |
| 9            | Very advantaged       | 90    |
| 10           | Most advantaged       | 100   |

This table is stored in the [`irsad_scoring.py`](./data/irsad_scoring.py) file.

---
### **1.1.2 Suburb Crime Level**: 

In residential collateral risk assessment, property value is influenced not only by the physical characteristics of the dwelling, but also by the stability, livability, and long-term sustainability of the surrounding neighbourhood.

Suburb crime level is therefore included as a quantifiable proxy to reflect the following factors:

* **Residential safety and livability**
  Areas with higher crime rates tend to be less attractive to owner-occupiers and tenants, which can negatively affect housing demand.

* **Market demand and liquidity**
  Persistently high crime levels may suppress buyer demand, resulting in reduced market liquidity and longer disposal times

* **Price resilience**
  During market downturns, properties located in higher-crime suburbs are generally more susceptible to price declines and tend to recover more slowly

> [!IMPORTANT]
> Due to file size constraints, raw suburb-level crime datasets are not stored in this repository.
> 
> Data can be obtained directly from [the official source](https://bocsar.nsw.gov.au/statistics-dashboards/open-datasets/criminal-offences-data.html)
> 
> A trimmed dataset is stored in () file
>
> The Crime rate only refers within the current 12 months.
> 
> Below are the python codes for trimming the dataset:
> ```python
> 

#### **Benchmark Table (Version 1.0)**:
| Crime Rank Range | Interpretation      | Risk Level     | Scoring (1–100) | Notes                   |
| ---------------- | ------------------- | -------------- | --------------- | ----------------------- |
| **1–20**         | Very low crime      | Very Low Risk  | Same as rank    | Safe, stable suburb     |
| **21–40**        | Lower than average  | Low Risk       | Same as rank    | Minor crime exposure    |
| **41–60**        | Average crime       | Medium Risk    | Same as rank    | Neutral baseline        |
| **61–80**        | Higher than average | High Risk      | Same as rank    | Noticeable crime issues |
| **81–100**       | Very high crime     | Very High Risk | Same as rank    | Severe crime concerns   |

---

### **1.2 Zoning**

#### **1.2.1 Residential Zoning Benmchmarks** 

| Code | Zoning Name | Description | Benchmark Score |
|------|-------------|-------------|-----------------|
| R1 | General Residential | Broad range of residential densities and housing types, including multi-dwelling and residential flat buildings, with supporting community and neighbourhood services. | 65 |
| R2 | Low Density Residential | Primarily low-density detached housing with limited redevelopment intensity; the most stable and restrictive urban residential zone. | 80 |
| R3 | Medium Density Residential | Medium-density residential accommodation allowing housing diversity and moderate redevelopment potential. | 55 |
| R4 | High Density Residential | High-density residential development such as apartments, with higher supply elasticity and greater market cycle sensitivity. | 30 |
| R5 | Large Lot Residential | Residential housing in a rural or semi-rural setting, often adjacent to urban areas, with lower density but reduced market liquidity. | 50 |

> [!IMPORTANT]
> Benchmark scores reflect the relative suitability of each residential zoning category for residential collateral purposes.
>  
> Higher scores indicate greater zoning stability, residential focus, and long-term market predictability.
> 
---

#### **1.2.2 Non-Residential Zoning Benchmark**

| Code | Zoning Name | Zoning Category | Description | Benchmark Score |
|------|------------|----------------|-------------|-----------------|
| RU1 | Primary Production | Rural | Commercial primary industry production including agriculture, aquaculture, forestry, mining and extractive industries. | 10 |
| RU2 | Rural Landscape | Rural | Rural land for primary production compatible with conserved ecological or scenic landscape qualities. | 15 |
| RU3 | Forestry | Rural | Land protected for long-term forestry use, including State forests. | 5 |
| RU4 | Primary Production Small Lots | Rural | Commercial primary production on smaller rural holdings, including emerging agricultural uses. | 20 |
| RU5 | Village | Rural | Mixed-use rural village centres providing residential, retail, business and community services. | 60 |
| RU6 | Transition | Rural | Transitional land between intensive rural uses and more sensitive or urbanised areas. | 25 |
| B1 | Neighbourhood Centre | Business | Small-scale centres providing daily convenience retail, business and community uses, with shop-top housing permitted. | 40 |
| B2 | Local Centre | Business | Centres providing a broad range of commercial, civic, cultural and residential uses servicing a wider catchment. | 35 |
| B3 | Commercial Core | Business | Major centres with intensive retail, office, entertainment and community uses linked to major transport routes. | 15 |
| B4 | Mixed Use | Business | Areas encouraging a wide range of commercial, residential, tourist and community uses. | 30 |
| B5 | Business Development | Business | Business and bulky goods retail uses requiring large floor areas, supporting employment generation. | 10 |
| B6 | Enterprise Corridor | Business | Commercial and industrial development along major transport corridors. | 10 |
| B7 | Business Park | Business | Office and light industrial uses, including high technology industries with specialised economic functions. | 5 |
| B8 | Metropolitan Centre | Business | Global strategic centres (Sydney and North Sydney CBDs) with intensive commercial and mixed uses. | 20 |
| IN1 | General Industrial | Industrial | Wide range of industrial and warehouse uses with compatible activities. | 5 |
| IN2 | Light Industrial | Industrial | Light industrial, warehouse and service industries with limited amenity impact. | 10 |
| IN3 | Heavy Industrial | Industrial | Heavy industrial uses requiring separation due to health or environmental risks. | 0 |
| IN4 | Working Waterfront | Industrial | Industrial and maritime uses requiring direct waterfront access. | 0 |
| SP1 | Special Activities | Special Purpose | Sites with unique characteristics unsuitable for standard zoning categories. | 5 |
| SP2 | Infrastructure | Special Purpose | Land for permanent public or strategic infrastructure such as hospitals, utilities, transport and defence facilities. | 0 |
| SP3 | Tourist | Special Purpose | Areas focused on tourism-related development and visitor accommodation. | 20 |
| RE1 | Public Recreation | Recreation | Public open space and recreational areas including parks and community facilities. | 5 |
| RE2 | Private Recreation | Recreation | Privately owned or managed recreational facilities such as golf courses and racecourses. | 15 |
| E1 | National Parks and Nature Reserves | Environment | Protected national parks and conservation reserves. | 0 |
| E2 | Environmental Conservation | Environment | Land protected for high ecological, scientific, cultural or aesthetic values. | 5 |
| E3 | Environmental Management | Environment | Land with environmental or hazard constraints requiring special management. | 15 |
| E4 | Environmental Living | Environment | Low-impact residential development within environmentally sensitive or scenic areas. | 45 |
| W1 | Natural Waterways | Waterway | Protected natural waterways with high ecological and scenic significance. | 0 |
| W2 | Recreational Waterways | Waterway | Waterways supporting recreation, boating and fishing-related activities. | 5 |
| W3 | Working Waterways | Waterway | Waterways used for commercial shipping, ports and maritime industries. | 0 |

> [!IMPORTANT]
> Non-residential zoning benchmark scores reflect the relative suitability of each zoning category for residential collateral purposes.
> 
> Higher scores indicate greater residential compatibility, market acceptance, and long-term value predictability.

