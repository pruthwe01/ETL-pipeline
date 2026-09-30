import pandas as pd

DATE_COLUMNS = ["data_as_at", "job_placement_date"]
NUMBER_COLUMNS = [
    "denominator_4wk", "denominator_12wk", "denominator_26wk",
    "numerator_4wk", "numerator_12wk", "numerator_26wk",
]
PLACEHOLDERS = ["NULL", "UKN", ""]


def transform_placements(df):
    """Clean the raw job placement table and return a new DataFrame."""
    df = df.copy()  # never modify the raw data in place

    # 1. Consistent column names; drop the API's internal row id
    df.columns = df.columns.str.lower()
    df = df.drop(columns=["_id"])

    # 2. Strip whitespace from every text column
    for col in df.columns:
        df[col] = df[col].astype("string").str.strip()

    # 3. Placeholders -> real missing values
    df = df.replace(PLACEHOLDERS, pd.NA)

    # 4. Proper data types
    for col in DATE_COLUMNS:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    for col in NUMBER_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 5. Report duplicates rather than silently dropping them
    dupes = df["job_placement_id"].duplicated().sum()
    print(f"Duplicate job_placement_id values: {dupes}")

    return df