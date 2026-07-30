# Business Answers

Candidate name: Taksha R Naik
Date:30/07/2026

\---

## Q1. Which warehouse has the highest stock discrepancy rate, and what's actually driving it?

**From my analysis, Pune has the highest stock discrepancy rate at 11.34%.**



**I also looked at the movement types to understand what was causing these discrepancies. I found that Adjustment movements had the highest discrepancy rate (11.11%). Since adjustments are usually manual corrections made to inventory records, this suggests that inventory counts or stock updates may not be accurate and employees are making manual corrections more often.**



**Although Pune has the highest discrepancy rate, the other warehouses are also between 8% and 11%, which indicates that this is not limited to one warehouse. It appears to be a broader inventory management issue across the company.**



**How I checked it:**



**Calculated the stock discrepancy rate for each warehouse.**

**Compared discrepancy rates across different movement types.**

**Identified which movement type contributed the most to stock discrepancies.**

\---

## Q2. Is there a relationship between unit cost and quantity across suppliers? Which supplier(s) deviate, and by how much?

**Answer:**



**For most suppliers, the unit cost stayed fairly consistent regardless of the quantity ordered. The average unit cost was around $1,026, and most suppliers followed a similar pricing pattern.**



**However, SUP\_09 stood out from the rest. This supplier had unit costs reaching nearly $22,000, and its average unit cost was $10,559, which is about 10 times higher than the overall supplier average.**



**This could indicate that SUP\_09 supplies premium products, has pricing issues, or may require further investigation to understand why the costs are significantly higher.**



**How I checked it:**



**Compared unit cost and quantity across all suppliers.**

**Calculated the average unit cost for each supplier.**

**Identified suppliers whose average costs were much higher than the overall average.**

\---

## Q3. Which SKU(s) show signs of frequent stockouts or inventory imbalance? What would you recommend?

**Answer:**



**The analysis showed that SKU\_0172 had the highest number of inventory imbalance issues and frequently resulted in negative stock levels.**



**After reviewing these records, I noticed two main problems:**



**In several cases, the system allowed stock to be dispatched even when the available inventory was lower than the requested quantity.**

**I also found records where the stock calculations did not match the expected values, suggesting that some inventory updates may not have been processed correctly.**



**Recommendation:**



**I would recommend adding a validation rule in the Warehouse Management System (WMS) that prevents transactions when the requested quantity is greater than the available stock. It would also be useful to review the inventory calculation process to make sure stock balances are updated correctly after each transaction.**



**How I checked it:**



**Identified SKUs with the highest number of negative stock records.**

**Reviewed stock before, quantity moved, and stock after values.**

**Compared expected stock calculations with the recorded values to identify inconsistencies.**

\---

## Q4. What data quality issues did you find, and how did you handle them?

**Answer:**



**Before starting the analysis, I checked the quality of the dataset and found a few issues.**



**I found 15 duplicate movement records, so I removed the duplicate entries while keeping the first occurrence.**

**The date column was stored as text, so I converted it into a datetime format for easier analysis.**

**There were 545 completed transactions where the stock\_after value was missing. Instead of filling these values, I kept them as missing because they may indicate that the inventory system failed to update the stock correctly.**

**I found 202 records with negative stock values. I did not remove these because they were important for identifying inventory problems. Instead, I created a flag to easily analyze these cases.**

\---

## Q5. If you could track exactly one metric weekly to catch inventory problems early, what would it be and why?Answer:

## 

If I could track only one metric each week, I would monitor the number of manual inventory adjustments for each warehouse.



A sudden increase in manual adjustments usually indicates that the physical inventory does not match the system records. Tracking this metric would help identify problems early, allowing the operations team to investigate and fix issues before they lead to larger inventory discrepancies or stock shortages.



\---

## Anything else you'd flag if this were a real dataset at FreightFox?



One thing I noticed is that stock discrepancies are present across all warehouses, not just in Pune. Although Pune has the highest discrepancy rate, the other warehouses also have relatively high values.



This suggests that the issue may be related to the overall inventory management process rather than a single location. I would recommend reviewing inventory procedures, warehouse operations, and system validations across all warehouses to reduce manual corrections and improve inventory accuracy.

