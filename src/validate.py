VALID_STATES = {"NSW", "VIC", "QLD", "SA", "WA", "TAS", "NT", "ACT"}
REQUIRED_COLUMNS = ["job_placement_id", "job_placement_date", "state"]


def validate_placements(df):
    """Return (errors, warnings). Errors should stop the pipeline."""
    errors = []
    warnings = []

    if df.empty:
        errors.append("Table is empty")
        return errors, warnings

    # Key columns must always be filled in
    for col in REQUIRED_COLUMNS:
        missing = df[col].isna().sum()
        if missing:
            errors.append(f"{col}: {missing} missing values")

    # Each placement should appear once
    dupes = df["job_placement_id"].duplicated().sum()
    if dupes:
        errors.append(f"job_placement_id: {dupes} duplicates")

    # Only real Australian states and territories
    unexpected = set(df["state"].dropna().unique()) - VALID_STATES
    if unexpected:
        errors.append(f"Unexpected state values: {sorted(unexpected)}")

    # A placement can't happen after the snapshot was taken
    after_snapshot = (df["job_placement_date"] > df["data_as_at"]).sum()
    if after_snapshot:
        errors.append(f"{after_snapshot} placements dated after data_as_at")

    # Warning only: assumes numerator <= denominator (check the data dictionary)
    for weeks in ("4wk", "12wk", "26wk"):
        bad = (df[f"numerator_{weeks}"] > df[f"denominator_{weeks}"]).sum()
        if bad:
            warnings.append(f"numerator_{weeks} exceeds denominator in {bad} rows")

    return errors, warnings