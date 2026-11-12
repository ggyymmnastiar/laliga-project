# Prefect Orchestration — LaLiga Data Pipeline

## Table of Contents

- [1. Overview](#1-overview)
- [2. Orchestration Architecture](#2-orchestration-architecture)
  - [2.1 Flow and Task Hierarchy](#21-flow-and-task-hierarchy)
  - [2.2 Execution Flow](#22-execution-flow)
- [3. Prefect Features Used](#3-prefect-features-used)
  - [3.1 Task (`@task`)](#31-task-task)
  - [3.2 Flow (`@flow`)](#32-flow-flow)
  - [3.3 Retries](#33-retries)
  - [3.4 Tags](#34-tags)
  - [3.5 Logging (`get_run_logger`)](#35-logging-get_run_logger)
  - [3.6 Runtime Context (`prefect.runtime`)](#36-runtime-context-prefectruntime)
  - [3.7 States (Error Propagation)](#37-states-error-propagation)
  - [3.8 Deployment (`.serve()`)](#38-deployment-serve)
- [4. Comparison: With vs Without Orchestrator](#4-comparison-with-vs-without-orchestrator)
- [5. Sample Pipeline Output](#5-sample-pipeline-output)
- [6. Related Files](#6-related-files)

---

## 1. Overview

The LaLiga Data Engineering pipeline is orchestrated using **Prefect 3.x** as a workflow orchestrator. Prefect replaces the plain Python pipeline execution (`main.py`) by adding observability, automatic retries, structured logging, and deployment capabilities — without modifying any of the existing business logic functions.

**Entry point:** `main_prefect.py`

```bash
python main_prefect.py              # Run the pipeline once
python main_prefect.py --deploy     # Run as a scheduled deployment
```

---

## 2. Orchestration Architecture

### 2.1 Flow and Task Hierarchy

```
laliga-master-pipeline (Flow)
├── bronze-pipeline (Sub-Flow)
│   └── bronze-ingestion (Task)
│         → calls ingest_teams()
│
├── silver-pipeline (Sub-Flow)
│   ├── silver-transform (Task)
│   │     → calls run_transform_teams()
│   └── load-silver-to-db (Task)          [retries=2]
│         → calls load_silver_teams()
│
└── gold-pipeline (Sub-Flow)
    └── load-gold-to-db (Task)            [retries=2]
          → calls load_gold_teams()
```

### 2.2 Execution Flow

```
datasets/JSON
    │
    ▼
┌─────────────────────────────────┐
│  bronze-pipeline (Sub-Flow)     │
│  ┌───────────────────────────┐  │
│  │ bronze-ingestion (Task)   │  │
│  │ tags: [bronze, ingestion] │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  silver-pipeline (Sub-Flow)     │
│  ┌───────────────────────────┐  │
│  │ silver-transform (Task)   │  │
│  │ tags: [silver, transform] │  │
│  └─────────────┬─────────────┘  │
│                │ wait_for        │
│  ┌─────────────▼─────────────┐  │
│  │ load-silver-to-db (Task)  │  │
│  │ tags: [silver, database]  │  │
│  │ retries: 2 (delay: 10s)   │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  gold-pipeline (Sub-Flow)       │
│  ┌───────────────────────────┐  │
│  │ load-gold-to-db (Task)    │  │
│  │ tags: [gold, database]    │  │
│  │ retries: 2 (delay: 10s)   │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
    │
    ▼
Pipeline Summary + Runtime Metadata
```

---

## 3. Prefect Features Used

### 3.1 Task (`@task`)

Each pipeline step is wrapped as a Prefect Task — the smallest atomic unit of work that is independently tracked by Prefect.

| Task Name | Function Called | Tags | Retries |
|-----------|----------------|------|:-------:|
| `bronze-ingestion` | `ingest_teams()` | `bronze`, `ingestion` | 0 |
| `silver-transform` | `run_transform_teams()` | `silver`, `transform` | 0 |
| `load-silver-to-db` | `load_silver_teams()` | `silver`, `database` | 2 |
| `load-gold-to-db` | `load_gold_teams()` | `gold`, `database` | 2 |

**Design principle:** Tasks only wrap existing functions from `src/`. No business logic resides within the task itself — tasks are solely responsible for calling the function, capturing the logger, and returning a status.

```python
@task(
    name="bronze-ingestion",
    tags=["bronze", "ingestion"],
    retries=0,
    log_prints=True,
)
def task_bronze_ingestion() -> str:
    logger = get_run_logger()
    from src.bronze.ingestion_teams import ingest_teams
    ingest_teams()           # ← existing function, unchanged
    return "bronze_done"
```

### 3.2 Flow (`@flow`)

Flows orchestrate the execution order of tasks. There are 4 flows in this pipeline:

| Flow Name | Type | Tasks Executed |
|-----------|------|----------------|
| `bronze-pipeline` | Sub-flow | `bronze-ingestion` |
| `silver-pipeline` | Sub-flow | `silver-transform` → `load-silver-to-db` |
| `gold-pipeline` | Sub-flow | `load-gold-to-db` |
| `laliga-master-pipeline` | Master flow | Calls all three sub-flows sequentially |

**Sub-flow pattern:** Each Medallion layer (Bronze, Silver, Gold) is encapsulated as an independent sub-flow. The master flow calls sub-flows sequentially and handles error propagation.

```python
@flow(name="silver-pipeline", log_prints=True)
def silver_flow() -> str:
    transform_result = task_silver_transform()
    load_result = task_load_silver(wait_for=[transform_result])
    return load_result
```

### 3.3 Retries

Automatic retries are applied to tasks involving database connections, as PostgreSQL connections may fail due to timeouts or connection pool exhaustion.

| Task | retries | retry_delay_seconds | Reason |
|------|:-------:|:-------------------:|--------|
| `bronze-ingestion` | 0 | — | Local file operation, rarely fails |
| `silver-transform` | 0 | — | Local file operation, rarely fails |
| `load-silver-to-db` | 2 | 10 | PostgreSQL connection may timeout |
| `load-gold-to-db` | 2 | 10 | PostgreSQL connection may timeout |

**Retry flow:**
```
Task fails → wait 10s → retry #1 → (if fails) wait 10s → retry #2 → (if fails) FAILED
```

### 3.4 Tags

Tags are used to categorize tasks by layer and operation type, enabling easy filtering in the Prefect UI.

| Tag | Tasks Using This Tag |
|-----|----------------------|
| `bronze` | `bronze-ingestion` |
| `silver` | `silver-transform`, `load-silver-to-db` |
| `gold` | `load-gold-to-db` |
| `ingestion` | `bronze-ingestion` |
| `transform` | `silver-transform` |
| `database` | `load-silver-to-db`, `load-gold-to-db` |

### 3.5 Logging (`get_run_logger`)

Prefect provides a built-in logger that integrates with the Prefect UI. All logs from tasks and flows are automatically recorded with metadata (timestamp, task/flow run name, log level).

```python
from prefect import get_run_logger

@task(name="bronze-ingestion")
def task_bronze_ingestion() -> str:
    logger = get_run_logger()     # Prefect-integrated logger
    logger.info("✅ Bronze Ingestion complete")
    return "bronze_done"
```

**Log output format:**
```
19:22:48.810 | INFO | Task run 'bronze-ingestion-93e' - ✅ Bronze Ingestion complete
```

Each log entry automatically includes:
- **Timestamp** — execution time
- **Log level** — INFO, WARNING, ERROR
- **Run context** — name of the task/flow run that produced the log

### 3.6 Runtime Context (`prefect.runtime`)

Runtime context provides metadata about the currently executing run, used for auditability and traceability.

```python
from prefect.runtime import flow_run

run_id   = flow_run.get_id()       # Unique UUID per execution
run_name = flow_run.get_name()     # Auto-generated name ("active-ladybug")
```

| Property | Example Output | Purpose |
|----------|---------------|---------|
| `flow_run.get_id()` | `06af5af9-4c0a-7467-8000-fe0a4d0da18e` | Unique identifier for Prefect UI lookup |
| `flow_run.get_name()` | `active-ladybug` | Human-readable name for log readability |

Runtime context is displayed at the start and end of the pipeline summary:
```
  Flow Run ID   : 06af5af9-4c0a-7467-8000-fe0a4d0da18e
  Flow Run Name : active-ladybug
```

### 3.7 States (Error Propagation)

In Prefect 3.x, state management occurs automatically through exception propagation. If a sub-flow fails (raises an exception), the parent flow catches and logs the error before re-raising it, causing Prefect to mark the flow run as `Failed`.

```python
@flow(name="laliga-master-pipeline")
def master_pipeline() -> None:
    try:
        bronze_flow()
    except Exception as e:
        logger.error("❌ Bronze Pipeline FAILED — pipeline halted: %s", e)
        raise                    # Prefect automatically sets state → Failed
```

**State lifecycle:**
```
PENDING → RUNNING → COMPLETED ✅
                  ↘ FAILED ❌ → (if retries configured) RETRYING → COMPLETED / FAILED
```

### 3.8 Deployment (`.serve()`)

Deployment enables the pipeline to run on a schedule without manual execution.

```python
if __name__ == "__main__":
    if "--deploy" in sys.argv:
        master_pipeline.serve(
            name="laliga-daily-pipeline",
            tags=["production", "laliga"],
            parameters={},
        )
```

**How to run as a deployment:**
```bash
python main_prefect.py --deploy
```

Available deployment features:
- **Scheduling** — Add `cron="0 6 * * *"` to `.serve()` to run the pipeline daily at 06:00
- **Tags** — Group deployments for filtering (`production`, `laliga`)
- **Parameters** — Override default parameters at runtime

---

## 4. Comparison: With vs Without Orchestrator

| Aspect | `main.py` (Without Prefect) | `main_prefect.py` (With Prefect) |
|--------|---------------------------|--------------------------------|
| Observability | Manual logging via `logging` | Integrated Prefect UI logging |
| Retry | None | Automatic (2x for database tasks) |
| State tracking | None | Automatic (Pending → Running → Completed/Failed) |
| Run metadata | None | Flow Run ID, Name, timestamps |
| Error handling | Plain exceptions | Exception + state propagation + structured logging |
| Scheduling | Manual (`cron` + script) | Built-in via `.serve()` |
| Dependency management | Implicit (code order) | Explicit (`wait_for`, sub-flow sequence) |
| Monitoring | Read log files | Prefect UI (dashboard, timeline, log viewer) |

---

## 5. Sample Pipeline Output

```
19:22:46.141 | INFO | Flow run 'active-ladybug' -
19:22:46.148 | INFO | Flow run 'active-ladybug' - ╔══════════════════════════════════════════════════════════════╗
19:22:46.149 | INFO | Flow run 'active-ladybug' - ║  LALIGA DATA PIPELINE — START                                ║
19:22:46.149 | INFO | Flow run 'active-ladybug' - ╚══════════════════════════════════════════════════════════════╝
19:22:46.150 | INFO | Flow run 'active-ladybug' -   Flow Run ID   : 06af5af9-4c0a-7467-8000-fe0a4d0da18e
19:22:46.150 | INFO | Flow run 'active-ladybug' -   Flow Run Name : active-ladybug

19:22:48.356 | INFO | Flow run 'blazing-dugong'   - 🟤 Bronze Pipeline started
19:22:49.236 | INFO | Task run 'bronze-ingestion-93e' - ✅ Bronze Ingestion complete
19:22:49.238 | INFO | Task run 'bronze-ingestion-93e' - Finished in state Completed()
19:22:49.655 | INFO | Flow run 'blazing-dugong'   - Finished in state Completed()

19:22:51.832 | INFO | Flow run 'observant-collie' - ⚪ Silver Pipeline started
19:22:52.312 | INFO | Task run 'silver-transform-ea9'  - ✅ Silver Transform complete
19:22:53.042 | INFO | Task run 'load-silver-to-db-038' - ✅ Load Silver complete
19:22:53.502 | INFO | Flow run 'observant-collie' - Finished in state Completed()

19:22:55.818 | INFO | Flow run 'yellow-chimpanzee' - 🟡 Gold Pipeline started
19:22:56.476 | INFO | Task run 'load-gold-to-db-a50' - ✅ Load Gold complete
19:22:56.875 | INFO | Flow run 'yellow-chimpanzee' - Finished in state Completed()

19:22:56.877 | INFO | Flow run 'active-ladybug' - ╔══════════════════════════════════════════════════════════════╗
19:22:56.878 | INFO | Flow run 'active-ladybug' - ║  PIPELINE SUMMARY                                            ║
19:22:56.881 | INFO | Flow run 'active-ladybug' - ╠══════════════════════════════════════════════════════════════╣
19:22:56.882 | INFO | Flow run 'active-ladybug' - ║  Step 1  Bronze Ingestion                    3.51s  ✅  ║
19:22:56.883 | INFO | Flow run 'active-ladybug' - ║  Step 2  Silver (Transform + Load)           3.85s  ✅  ║
19:22:56.884 | INFO | Flow run 'active-ladybug' - ║  Step 3  Gold (OBT + Export)                 3.37s  ✅  ║
19:22:56.885 | INFO | Flow run 'active-ladybug' - ╠══════════════════════════════════════════════════════════════╣
19:22:56.886 | INFO | Flow run 'active-ladybug' - ║  TOTAL                              10.74s       ║
19:22:56.886 | INFO | Flow run 'active-ladybug' - ╚══════════════════════════════════════════════════════════════╝
19:22:56.888 | INFO | Flow run 'active-ladybug' - ✅ Pipeline completed in 10.74s
19:22:57.196 | INFO | Flow run 'active-ladybug' - Finished in state Completed()
```

---

## 6. Related Files

| File | Description |
|------|-------------|
| `main_prefect.py` | Pipeline entry point with Prefect orchestration |
| `main.py` | Original pipeline entry point (without Prefect) |
| `src/bronze/ingestion_teams.py` | `ingest_teams()` function — called by task |
| `src/silver/transform_teams.py` | `run_transform_teams()` function — called by task |
| `src/db/load_silver.py` | `load_silver_teams()` function — called by task |
| `src/db/load_gold.py` | `load_gold_teams()` function — called by task |
| `config/config.py` | Path, file list, and database connection configuration |
| `requirements.txt` | Dependencies including `prefect` |
