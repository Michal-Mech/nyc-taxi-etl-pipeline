import os
from pathlib import Path
# PySpark needs JAVA_HOME to locate the JVM. Resolution order:
#   1) Respect JAVA_HOME from the shell / OS environment (preferred).
#   2) Fall back to DEFAULT_JAVA_HOME below — adjust to your local JDK path
#      if you don't have JAVA_HOME set system-wide.
# Must be set BEFORE importing pyspark.
DEFAULT_JAVA_HOME = r"C:\Program Files\Java\jdk-17"  # change me on a fresh clone

if not os.environ.get("JAVA_HOME"):
    os.environ["JAVA_HOME"] = DEFAULT_JAVA_HOME


# Set HADOOP_HOME (Windows only — needs winutils.exe + hadoop.dll)
# Spark internally uses Hadoop libraries, which on Windows require winutils.
# Download winutils for matching Hadoop version (Spark 3.5 → Hadoop 3.3.x) from:
#   https://github.com/cdarlint/winutils
DEFAULT_HADOOP_HOME = r"C:\hadoop"  # must contain bin/winutils.exe and bin/hadoop.dll

if not os.environ.get("HADOOP_HOME"):
    os.environ["HADOOP_HOME"] = DEFAULT_HADOOP_HOME
    os.environ["PATH"] = os.environ["HADOOP_HOME"] + r"\bin;" + os.environ["PATH"]

# Data layer paths
# Path(__file__) = path to this file (config.py)
# .parent = src/ folder
# .parent.parent = project root
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
BRONZE_PATH = DATA_DIR / "bronze"
SILVER_PATH = DATA_DIR / "silver"
GOLD_PATH = DATA_DIR / "gold"


# SparkSession factory with Delta Lake enabled
def get_spark(app_name: str = "ETL-Pipeline"):
    from pyspark.sql import SparkSession
    from delta import configure_spark_with_delta_pip

    builder = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")  # run locally and use all available CPU cores
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.driver.memory", "2g")
        .config("spark.sql.shuffle.partitions", "4")
        
        # Windows fixes: avoid non-ASCII paths in temp dir + force localhost binding
        .config("spark.local.dir", r"D:\spark-tmp")
        .config("spark.driver.host", "localhost")
        .config("spark.driver.bindAddress", "127.0.0.1")

    )

    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    spark.sparkContext.setLogLevel("WARN")  # reduce console noise
    return spark