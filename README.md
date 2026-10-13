# Python Essentials for Data Engineers

**A hands-on Python data engineering project: APIs → S3 → CSV → DuckDB**

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-Analytics-FFF000?logo=duckdb&logoColor=black)](https://duckdb.org/)
[![uv](https://img.shields.io/badge/Package_Manager-uv-DE5FE9)](https://docs.astral.sh/uv/)
[![Status](https://img.shields.io/badge/Status-In_Progress-orange)](https://github.com/Daniel059/python-de-essentials)

---

## Overview

This repository documents my hands-on journey into **Python for data engineering**, covering the foundations of building a data pipeline from extraction to transformation, storage, data quality, testing, and orchestration.

The project integrates data from REST and GraphQL APIs, a public Amazon S3 bucket, and locally generated CSV files. Python handles extraction and pipeline logic, while DuckDB provides a SQL engine for transforming and analysing the data.

Rather than building everything in a single notebook, I am developing a modular Python project with reproducible commands, deliberately imperfect sample data, and incremental Git commits that document the implementation process.

## Architecture

```text
     PokeAPI         NOAA weather        Local CSVs
 (REST/GraphQL)       (public S3)    (orders, customers)
        │                  │                  │
        └──────────────────┬──────────────────┘
                           ▼
                ┌─────────────────────┐
                │  Python extraction  │
                │  requests · boto3   │
                └──────────┬──────────┘
                           ▼
                ┌─────────────────────┐
                │   DuckDB SQL        │
                │   joins · buckets   │
                └──────────┬──────────┘
                           ▼
                ┌─────────────────────┐
                │   DuckDB database   │
                └──────────┬──────────┘
                           ▼
                ┌─────────────────────┐
                │   Quality checks    │
                └─────────────────────┘
```

*The diagram illustrates the intended pipeline architecture; implementation progress is tracked in the roadmap below.*

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Pipeline logic and data extraction |
| Requests | REST API calls and HTTP error handling |
| boto3 | Accessing data stored in Amazon S3 |
| DuckDB | SQL-based data transformation and analytics |
| CSV | Source data and intermediate datasets |
| GraphQL | Querying API data with reusable variables |
| uv | Dependency management and reproducible environments |
| pytest | Automated testing of transformation logic |

## What This Project Covers

- **Data extraction:** Retrieve data from REST and GraphQL APIs, public S3 objects, and local CSV files.
- **Data transformation:** Join customer and order datasets, calculate customer ages, and derive age groups using DuckDB SQL.
- **Data quality:** Seeded dirty data for the validation checks being built.
- **Error handling:** Use HTTP timeouts and `raise_for_status()` to surface request failures.
- **Reproducibility:** Manage dependencies with `uv` and track implementation through Git.
- **Testing and orchestration:** Build toward automated transformation tests and a defined pipeline execution sequence.

## How This Implementation Differs from the Original Tutorial

This project is inspired by Joseph Machado's *Python Essentials for Data Engineers* tutorial. It follows the same broad learning progression while adapting selected implementation choices to my own learning objectives.

| Original approach | My implementation |
|---|---|
| Single Jupyter notebook | Modular Python scripts |
| Author's pre-built sample data | Self-generated data featuring Kenyan customers, KES prices, M-Pesa payments, and deliberately seeded duplicates and missing values |
| Spark-style API simulated using `sqlframe` | DuckDB SQL for analytical transformations |
| Approximate age calculation based on year differences | Age calculation designed to account for whether a birthday has occurred |
| Weather records handled as plain lists | `csv.DictReader` for named-column access |
| Hard-coded GraphQL query | GraphQL query variables for reusable limits |
| Basic HTTP requests | Timeouts and explicit HTTP error handling |

The implementation is my own adaptation of the learning material, rather than a direct copy of the original repository.

## Project Structure

```text
python-de-essentials/
├── data/
│   ├── customers.csv
│   └── orders.csv
├── src/
│   ├── extract.py
│   ├── generate_data.py
│   └── transform.py
├── tests/
├── pyproject.toml
├── uv.lock
└── README.md
```

| File or directory | Responsibility |
|---|---|
| `data/` | Generated customer and order datasets |
| `src/extract.py` | API, S3, and CSV extraction |
| `src/generate_data.py` | Custom sample-data generation, including intentionally dirty records |
| `src/transform.py` | DuckDB SQL transformations, joins, age calculations, and age groups |
| `tests/` | Automated tests for transformation logic |
| `pyproject.toml` | Project metadata and dependency configuration |
| `uv.lock` | Pinned dependency versions |

## Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Daniel059/python-de-essentials.git
cd python-de-essentials
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Generate sample data

```bash
uv run python -m src.generate_data
```

### 4. Extract source data

```bash
uv run python -m src.extract
```

### 5. Run transformations

```bash
uv run python -m src.transform
```

## Development Roadmap

- [x] Project setup, Git, and GitHub repository
- [x] Extract data from REST APIs, GraphQL, public S3, and local CSV files
- [x] Transform order data using DuckDB SQL
- [x] Join datasets and derive customer age groups
- [ ] Transform weather data, including types, units, and quality flags
- [ ] Persist transformed tables to a DuckDB database file
- [ ] Add data-quality checks for duplicates, nulls, and invalid ranges
- [ ] Implement pytest unit tests for transformation logic
- [ ] Document execution dependencies and orchestration
- [ ] Add automated pipeline execution and scheduling

## Key Learnings

**Python is the orchestration layer.** It connects data sources, coordinates processing, and manages pipeline logic, while DuckDB performs SQL-based analytical operations.

**Understand the source before extracting at scale.** API documentation, pagination, query parameters, and GraphQL variables can reduce unnecessary requests and improve extraction efficiency.

**Make failures visible.** Timeouts and HTTP status checks help prevent failed requests from silently propagating through a pipeline.

**Explore data before transforming it.** Data types, units, missing values, and quality flags must be understood before applying business logic.

**Preserve records when investigating data quality.** Left joins expose unmatched keys as `NULL`, making missing relationships easier to identify and investigate.

**Build for reproducibility.** Modular code, dependency management, and incremental commits make a project easier to understand, maintain, and extend.

## Acknowledgements

This project was inspired by Joseph Machado's tutorial:

- [Python Essentials for Data Engineers — Start Data Engineering](https://www.startdataengineering.com/post/python-for-de/)
- [Original tutorial repository — python_essentials_for_data_engineers](https://github.com/josephmachado/python_essentials_for_data_engineers)

The tutorial provided the learning path: Extract → Transform → Load → Quality → Test → Orchestrate. This repository adapts that path through a modular implementation, custom sample data, and DuckDB-based transformations.

## Author

**Daniel Nzioki Musyoka**  
Data Management & Analytics Intern

[GitHub](https://github.com/Daniel059) · [LinkedIn](https://www.linkedin.com/in/daniel-nzioki-musyoka/) · [Portfolio](https://daniel-nzioki-musyoka-data-and-ai-pro.netlify.app/)

---

*Built as a hands-on learning project focused on Python, SQL, and practical data engineering fundamentals.*