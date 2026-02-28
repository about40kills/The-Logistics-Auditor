# Veridi Logistics: Last Mile Logistics Auditor

## A) Executive Summary
This internal audit of Veridi Logistics' last-mile delivery operations analyzed regional and category-specific delays using order data. We found that 2.9% of all orders are delivered late (1-5 days), while 4.2% are considered "Super Late" (over 5 days). The data reveals a strong negative correlation between delivery delays and customer review scores, underscoring the critical need to optimize fulfillment networks to preserve customer sentiment.

## B) Project Links
| Deliverable | Link / Location |
| :--- | :--- |
| **Data Analysis Notebook** | `https://colab.research.google.com/drive/1N0qmbi_J6Hu9OzwfXg3NIinCzC0k6SjW?usp=sharing` |
| **Interactive Dashboard** | `app.py` (Run locally) |
| **Presentation Deck** | `https://docs.google.com/presentation/d/17Y0maQx-dBAJEhjn-_W_AB633wEBZ2KK/edit?usp=sharing&ouid=104160930435475761743&rtpof=true&sd=true` |` |

## C) Technical Explanation

### Data Cleaning Decisions
1. **Deduplicating Reviews:** The `olist_order_reviews_dataset` contained multiple reviews for single orders (due to customers updating ratings or separate item reviews). To prevent a 1-to-many relationship from inflating the master dataset row count, reviews were sorted by `review_creation_date` descending, and duplicates were dropped keeping only the most recent review per `order_id`.
2. **Datetime Parsing:** All temporal columns were explicitly cast to datetime objects. `days_difference` was calculated by extracting and comparing the `.date` components, effectively ignoring time-of-day variations (which add noise to a daily-level metric).
3. **Filtering Invalid Orders:** Canceled and unavailable orders, as well as orders missing actual delivery dates, were excluded from the delay analysis, as they represent fulfillment failures rather than measurable delivery delays.
4. **Category Translation:** Product categories were aggregated at the item level. To prevent row duplication when joining back to the master table (which is unique per order), the top 15 delayed categories analysis was grouped independently.

### Candidate's Choice Justification
**Monthly Trend Analysis (Dual-Axis Chart):**  
I elected to build a monthly trend visualization comparing the percentage of late orders against the average review score over time. 
*   **Business Value:** Logistics chains often suffer from seasonal bottlenecks (e.g., Black Friday, holidays). By mapping delay spikes to timeline events, leadership can proactively allocate overflow resources for peak months.
*   **Metric Relationship:** Charting the average review score on a secondary axis vividly illustrates the direct, lagging impact that operational failures have on customer satisfaction.