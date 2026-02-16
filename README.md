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
