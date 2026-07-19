# Multi-Source ETL with Databricks and Delta Lake
A production-style ETL pipeline that ingests, transforms, and stores data from multiple sources into a Delta Lake.

In modern data-driven organizations, data is spread across multiple platforms.  
This project demonstrates how to unify that data into a consistent Delta Lake format to enable analytics, improve data quality, and support downstream AI/BI use cases.

---

## Features
- Data ingestion from S3, PostgreSQL, and REST API
- Transformation with PySpark (joins, filtering, aggregation)
- Data quality checks (null handling, schema enforcement)
- Partitioned and versioned Delta Lake storage
- End-to-end reproducibility

---

## Tech Stack
- Databricks
- PySpark
- Delta Lake
- SQL
- AWS S3
- PostgreSQL

---

## Installation

# Install dependencies
pip install -r requirements.txt

# Run transformation
python src/transform.py

---

## Lessons Learned
- Learned how to implement schema evolution in Delta Lake
- Optimized PySpark jobs with broadcast joins for small lookup tables
- Automated Delta table version rollback for disaster recovery
