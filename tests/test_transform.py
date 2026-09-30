import pandas as pd

from src.transform import transform_placements


def make_raw():
    """A tiny raw table with the messy patterns we know exist."""
    return pd.DataFrame({
        "_id": [1, 2],
        "DATA_AS_AT": ["2018-08-05", "2018-08-05"],
        "JOB_PLACEMENT_ID": ["100", "101"],
        "JOB_PLACEMENT_DATE": ["2016-10-17", "not a date"],
        "STATE": ["QLD   ", "VIC"],
        "ALLOWANCE_DESC": ["UKN", "Newstart Allowance"],
        "DENOMINATOR_4WK": ["NULL", "1"],
        "DENOMINATOR_12WK": ["1", "1"],
        "DENOMINATOR_26WK": ["1", "1"],
        "NUMERATOR_4WK": ["1", "NULL"],
        "NUMERATOR_12WK": ["1", "1"],
        "NUMERATOR_26WK": ["1", "1"],
    })


def test_whitespace_is_stripped():
    clean = transform_placements(make_raw())
    assert clean["state"].iloc[0] == "QLD"


def test_placeholders_become_missing():
    clean = transform_placements(make_raw())
    assert clean["allowance_desc"].isna().iloc[0]
    assert clean["denominator_4wk"].isna().iloc[0]


def test_types_are_converted():
    clean = transform_placements(make_raw())
    assert pd.api.types.is_datetime64_any_dtype(clean["job_placement_date"])
    assert str(clean["denominator_12wk"].dtype) == "Int64"


def test_invalid_date_becomes_missing():
    clean = transform_placements(make_raw())
    assert clean["job_placement_date"].isna().iloc[1]


def test_internal_id_column_is_dropped():
    clean = transform_placements(make_raw())
    assert "_id" not in clean.columns


def test_raw_data_is_not_modified():
    raw = make_raw()
    transform_placements(raw)
    assert raw["STATE"].iloc[0] == "QLD   "