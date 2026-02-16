# Open Brewery Data Lake Pipeline

[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-enabled-blue)](https://www.docker.com/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()

## Table of Contents
1. [Objective](#objective)
2. [Architecture & Flow](#architecture--flow)
3. [Technology Stack](#technology-stack)
4. [Service Access](#service-access)
5. [Setup Instructions](#setup-instructions)
6. [Data Lake Layers](#data-lake-layers)
    - [Bronze](#bronze)
    - [Silver](#silver)
    - [Gold](#gold)
7. [Monitoring & Data Quality](#monitoring--data-quality)
8. [Design Choices & Trade-offs](#design-choices--trade-offs)
9. [License](#license)

---

## Objective
This project demonstrates how to **ingest data from the Open Brewery DB API, transform it, and persist it into a data lake** following the **medallion architecture**: Bronze, Silver, and Gold.  

The pipeline includes **data quality checks, metadata tracking, automated orchestration, retries, and a web UI for monitoring**.

---

## Architecture & Flow

```text
Open Brewery API
       │
       ▼
  Bronze Pipe (Parquet + data quality)
       │ triggers next pipe via Mage API
       ▼
  Silver Pipe (Spark + Delta + metadata)
       │ triggers next pipes via Mage API
       ▼
  Gold Pipes 1, 2, 3 (Spark + Delta aggregates)
```

**Key Points:**

- **Bronze Pipe**: stores raw API data in Parquet and performs **data quality checks** to ensure records exist.  
- **Silver Pipe**: transforms Bronze data using **Spark + Delta**, partitions by location, and generates **metadata**: file path, ingestion time, and Bronze info.  
- **Gold Pipes**: generate analytical aggregations using **Spark + Delta**.  
- **Pipeline orchestration**: each pipe triggers the next via Mage API, ensuring modular execution.  
- **Automatic retries**: Mage automatically retries each block **3–4 times** in case of failures.  
- **Automatic execution**: starting `docker-compose` runs the Bronze Pipe, triggering the full pipeline.  
- **Mage Web UI**: monitor logs, pipeline status, and execution progress.  

**Design rationale for separate pipelines and multiple blocks:**

- Pipelines for Bronze, Silver, and Gold are **separated** to improve **understanding, maintainability, and modularity**.  
- Bronze pipeline uses **multiple blocks** to clearly separate the logic and expectations of each step, making it easier to maintain and debug.  

---

## Technology Stack

- **Language**: Python 3.10 + PySpark  
- **Orchestration**: Mage (web UI + Mage API for pipe triggering)  
- **Data Storage**: Delta Lake (on S3-compatible storage, SeaweedFS)  
- **Containerization**: Docker  
- **Monitoring**: Mage Web UI + logging + retries

---

## Service Access

| Service          | URL                       | Notes                                      |
|-----------------|---------------------------|--------------------------------------------|
| Mage Web UI      | http://localhost:6789/    | user: `admin@admin.com`, pass: `admin`    |
| Object Store UI  | http://localhost:8888/    | browse buckets for Bronze/Silver/Gold     |
| Spark UI         | http://localhost:8080/    | monitor Spark jobs and performance        |

---

## Setup Instructions

```bash
git clone https://github.com/yourusername/open-brewery-datalake.git
cd open-brewery-datalake
docker-compose up --build
```

**Notes:**

- **SeaweedFS** runs an initialization script to create buckets: `bronze`, `silver`, `gold`, and `mage`.  
- **Mage** starts a **SQLite database** to persist pipeline information.  
- **Bronze Pipe executes automatically**, triggering Silver → Golds.  
- **Dynamic API URL handling**: Mage’s internal API URL changes on each initialization because it includes a dynamic ID stored in SQLite. This is resolved dynamically at runtime.  
- **Retries**: Mage automatically retries each block **3–4 times** if errors occur.  

---

## Data Lake Layers

### Bronze
- Stores raw API data in **Parquet**.  
- Performs **data quality checks** to ensure records exist.  
- Uses **multiple blocks** to separate ingestion and validation steps.  

### Silver
- Reads Bronze Parquet.  
- Transforms and partitions using **Spark + Delta**.  
- Generates **metadata**: file path, ingestion timestamp, and reference to Bronze data.  

### Gold
- Aggregates brewery counts per type and location.  
- Stored as **Delta tables** for analytics.  

---

## Monitoring & Data Quality

- **Bronze**: ensures records exist and schema is valid.  
- **Silver**: generates metadata for traceability.  
- **Mage Web UI**: visual interface to check logs, pipeline progress, retries, and errors.  

---

## Design Choices & Trade-offs

- **Parquet in Bronze**: simple ingestion, works natively with pandas.  
- **Spark + Delta in Silver/Gold**: scalable transformations and aggregations.  
- **Separate pipelines**: improves **maintainability, modularity, and clarity**.  
- **Multiple blocks in Bronze**: separates ingestion and validation steps for easier debugging and monitoring.  
- **Mage API orchestration**: pipes trigger each other automatically.  
- **Automatic retries**: 3–4 attempts per block for reliability.  
- **Object Store bucket for Mage**: avoids storing Mage files locally.  
- **Mage Web UI**: easy monitoring and debugging.  

---

## License
MIT License
