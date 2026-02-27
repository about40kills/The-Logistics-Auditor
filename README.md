# Veridi Logistics: Last Mile Logistics Auditor

## A) Executive Summary
This internal audit of Veridi Logistics' last-mile delivery operations analyzed regional and category-specific delays using order data. We found that 2.9% of all orders are delivered late (1-5 days), while 4.2% are considered "Super Late" (over 5 days). The data reveals a strong negative correlation between delivery delays and customer review scores, underscoring the critical need to optimize fulfillment networks to preserve customer sentiment.

## B) Project Links
| Deliverable | Link / Location |
| :--- | :--- |
| **Data Analysis Notebook** | `veridi_logistics_audit.ipynb` |
| **Interactive Dashboard** | `app.py` (Run locally) |
| **Presentation Deck** | `[Link Placeholder]` |
| **Demo Video** | `[Link Placeholder]` |

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

## D) Repository Structure
```text
The-Logistics-Auditor/
│
├── veridi_logistics_audit.ipynb    # Main data analysis & cleaning notebook
├── app.py                          # Streamlit interactive dashboard
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore file for data and cache
├── README.md                       # This documentation file
│
└── [Dataset CSVs]                  # *Ignored by git, must be downloaded locally*
    ├── olist_orders_dataset.csv
    ├── olist_order_reviews_dataset.csv
    ├── ...
```

## E) How to Run Locally

### Prerequisites
1. Ensure you have Python 3.9+ installed.
2. Download the [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) from Kaggle.
3. Extract the contents into the root directory of this repository (the `.gitignore` will ensure they are not committed). You need at least:
    * `olist_orders_dataset.csv`
    * `olist_order_reviews_dataset.csv`
    * `olist_customers_dataset.csv`
    * `olist_products_dataset.csv`
    * `olist_order_items_dataset.csv`
    * `product_category_name_translation.csv`

### Installation & Execution
1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Run the Notebook (Data Pipeline):**
    Open `veridi_logistics_audit.ipynb` in Jupyter Notebook, JupyterLab, or VS Code and Run All Cells.
    *This will merge the datasets, perform the analysis, generate PNG charts, and output the required `veridi_master_clean.csv` file.*

3. **Run the Dashboard:**
    Once the clean CSV is generated, launch the Streamlit app:
    ```bash
    streamlit run app.py
    ```
    The dashboard will open automatically in your browser at `http://localhost:8501`.
