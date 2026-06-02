# ETL Mini-Pipeline — NYC Taxi (PySpark + Delta Lake + Databricks)

End-to-end pipeline ETL na danych NYC Taxi. Pobiera publiczny dataset, przetwarza go z użyciem PySparka w architekturze medallion (bronze → silver → gold), zapisuje jako Delta Table i generuje raport agregacyjny.

## Stack

- **Python 3.11+**
- **PySpark 3.5** — przetwarzanie danych
- **Delta Lake 3.2** — format storage z ACID, time travel, schema evolution
- **Databricks Community Edition** — finalny deploy jako zaplanowany job
- **Jupyter** — wizualizacja wyników

## Architektura medallion

```
API NYC TLC → BRONZE (raw)  → SILVER (cleaned)  → GOLD (aggregated reports)
                Delta Table     Delta Table         Delta Table
```

| Warstwa | Zawartość |
|---------|-----------|
| **Bronze** | Surowy snapshot danych z API, 1:1 jako Delta Table |
| **Silver** | Wyczyszczone, otypowane, zwalidowane (data quality checks) |
| **Gold** | Zagregowane metryki gotowe pod raport / dashboard |

## Co pokazuje ten projekt

- PySpark — DataFrame API, transformacje, agregacje
- Delta Lake — Delta Tables, schema enforcement, ACID
- Data quality — walidacje w PySparku (custom assertions)
- Architektura medallion (bronze/silver/gold)
- Databricks jobs — deploy + scheduling

## Uruchomienie lokalne

```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
python run_pipeline.py
```

## Struktura projektu

```
.
├── data/                  # Delta Tables (lokalnie, gitignored)
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── notebooks/             # Jupyter notebooks z analizą i wizualizacją
├── src/                   # Kod pipeline'u
│   ├── config.py          # Konfiguracja Sparka + Delta
│   ├── bronze.py          # Ingestion z API
│   ├── silver.py          # Czyszczenie + walidacja
│   └── gold.py            # Agregacje
├── databricks/            # Wersje notebooków pod Databricks + job config
├── run_pipeline.py        # Punkt wejścia uruchamiający bronze→silver→gold
├── requirements.txt
└── README.md
```

## Status

🚧 W trakcie budowy — projekt portfolio.
