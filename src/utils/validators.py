"""
Utils — Data Quality Validators
================================
Fungsi-fungsi validasi reusable untuk memastikan kualitas data
sebelum dimuat ke PostgreSQL.

Filosofi:
  - TIDAK mengubah data (kecuali strip whitespace pada nama club)
  - RAISE ValueError jika validasi kritis gagal (pipeline berhenti)
  - LOG WARNING jika ada anomali non-fatal
  - Reusable untuk teams maupun players
"""

import logging
from typing import Any

import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Konstanta
# ---------------------------------------------------------------------------

LALIGA_CLUBS = {
    "Alaves", "Athletic Bilbao", "Atlético Madrid", "Barcelona",
    "Celta Vigo", "Elche", "Espanyol", "Getafe",
    "Girona", "Levante", "Mallorca", "Osasuna",
    "Rayo Vallecano", "Real Betis", "Real Madrid", "Real Oviedo",
    "Real Sociedad", "Sevilla", "Valencia", "Villarreal",
}

# Range wajar per pola nama kolom (min, max).
# Digunakan oleh validate_ranges() sebagai heuristik.
DEFAULT_RANGES = {
    "played":       (1, 50),
    "goals":        (0, 250),
    "xg":           (0, 250),
    "shots":        (0, 1500),
    "sot":          (0, 500),
    "tackles":      (0, 2000),
    "interceptions": (0, 1500),
    "possession_won": (0, 4000),
    "blocks":       (0, 1000),
    "clearances":   (0, 3000),
    "passes_total": (0, 30000),
    "crosses_total": (0, 2000),
    "pressed_seqs": (0, 2000),
    "ppda":         (0, 50),
    "through_balls": (0, 500),
    "touches_in_box": (0, 3000),
    "fast_breaks_total": (0, 300),
    "offsides":     (0, 500),
    "fouls":        (0, 1000),
    "yellows":      (0, 200),
    "reds":         (0, 50),
}


# ---------------------------------------------------------------------------
# 1. Empty File Check
# ---------------------------------------------------------------------------

def validate_not_empty(df: pd.DataFrame, name: str) -> None:
    """Pastikan DataFrame tidak kosong (> 0 rows).

    Raises:
        ValueError: Jika DataFrame kosong.
    """
    if df.empty:
        raise ValueError(
            f"[DQ FAIL] {name}: DataFrame kosong (0 rows). "
            f"File sumber mungkin corrupt atau tidak terbaca."
        )
    logger.info("  ✓ Not empty: %d rows", len(df))


# ---------------------------------------------------------------------------
# 2. CSV Integrity / Schema Check
# ---------------------------------------------------------------------------

def validate_schema(
    df: pd.DataFrame,
    name: str,
    expected_columns: list[str],
) -> None:
    """Pastikan kolom DataFrame sesuai dengan yang diharapkan.

    Raises:
        ValueError: Jika ada kolom yang hilang atau kolom tak dikenal.
    """
    actual = set(df.columns)
    expected = set(expected_columns)

    missing = expected - actual
    extra = actual - expected

    if missing:
        raise ValueError(
            f"[DQ FAIL] {name}: Kolom hilang → {sorted(missing)}. "
            f"Kolom yang ada: {sorted(actual)}"
        )
    if extra:
        raise ValueError(
            f"[DQ FAIL] {name}: Kolom tak dikenal → {sorted(extra)}. "
            f"Kolom yang diharapkan: {sorted(expected)}"
        )
    logger.info("  ✓ Schema: %d kolom sesuai", len(expected_columns))


# ---------------------------------------------------------------------------
# 3. Missing Value Check
# ---------------------------------------------------------------------------

def validate_no_missing(df: pd.DataFrame, name: str) -> None:
    """Pastikan tidak ada NULL/NaN di seluruh kolom.

    Raises:
        ValueError: Jika ditemukan missing values.
    """
    missing = df.isnull().sum()
    cols_with_missing = missing[missing > 0]

    if not cols_with_missing.empty:
        detail = ", ".join(
            f"{col}={count}" for col, count in cols_with_missing.items()
        )
        raise ValueError(
            f"[DQ FAIL] {name}: Ditemukan missing values → {detail}"
        )
    logger.info("  ✓ No missing values")


# ---------------------------------------------------------------------------
# 4. Whitespace Validation (satu-satunya yang memodifikasi data)
# ---------------------------------------------------------------------------

def validate_strip_whitespace(
    df: pd.DataFrame,
    name: str,
    column: str = "club",
) -> pd.DataFrame:
    """Strip spasi di awal/akhir kolom string (default: club).

    Returns:
        DataFrame dengan kolom yang sudah di-strip.
    """
    if column not in df.columns:
        return df

    df = df.copy()
    original = df[column].tolist()
    df[column] = df[column].str.strip()
    stripped = df[column].tolist()

    changed = [
        f"'{o}' → '{s}'"
        for o, s in zip(original, stripped)
        if o != s
    ]
    if changed:
        logger.warning(
            "  ⚠ %s: Whitespace ditemukan dan dihapus pada kolom '%s': %s",
            name, column, ", ".join(changed),
        )
    else:
        logger.info("  ✓ No whitespace issues pada kolom '%s'", column)

    return df


# ---------------------------------------------------------------------------
# 5. Duplicate Club Check
# ---------------------------------------------------------------------------

def validate_no_duplicates(
    df: pd.DataFrame,
    name: str,
    column: str = "club",
) -> None:
    """Pastikan tidak ada nilai duplikat pada kolom tertentu.

    Raises:
        ValueError: Jika ditemukan duplikat.
    """
    if column not in df.columns:
        return

    dupes = df[df[column].duplicated(keep=False)]
    if not dupes.empty:
        dupe_values = sorted(dupes[column].unique())
        raise ValueError(
            f"[DQ FAIL] {name}: Duplikat pada kolom '{column}' → {dupe_values}"
        )
    logger.info("  ✓ No duplicates pada kolom '%s'", column)


# ---------------------------------------------------------------------------
# 6. Expected Number of Rows
# ---------------------------------------------------------------------------

def validate_expected_rows(
    df: pd.DataFrame,
    name: str,
    expected: int = 20,
) -> None:
    """Pastikan jumlah baris sesuai yang diharapkan.

    Raises:
        ValueError: Jika jumlah baris tidak sesuai.
    """
    actual = len(df)
    if actual != expected:
        raise ValueError(
            f"[DQ FAIL] {name}: Jumlah baris = {actual}, "
            f"diharapkan = {expected}. "
            f"Apakah ada klub yang hilang atau ditambahkan?"
        )
    logger.info("  ✓ Row count: %d (sesuai)", actual)


# ---------------------------------------------------------------------------
# 7. Club Name Validation
# ---------------------------------------------------------------------------

def validate_club_names(
    df: pd.DataFrame,
    name: str,
    valid_clubs: set[str] | None = None,
    column: str = "club",
) -> None:
    """Pastikan semua nama club ada di daftar resmi.

    Warning (non-fatal) jika ada nama yang tidak dikenal.
    """
    if column not in df.columns:
        return

    if valid_clubs is None:
        valid_clubs = LALIGA_CLUBS

    actual_clubs = set(df[column].unique())
    unknown = actual_clubs - valid_clubs
    missing = valid_clubs - actual_clubs

    if unknown:
        logger.warning(
            "  ⚠ %s: Nama club tidak dikenal → %s. "
            "Mungkin ada perubahan nama klub atau typo.",
            name, sorted(unknown),
        )
    if missing:
        logger.warning(
            "  ⚠ %s: Club yang diharapkan tapi tidak ada → %s",
            name, sorted(missing),
        )
    if not unknown and not missing:
        logger.info("  ✓ Club names: semua 20 klub valid")


# ---------------------------------------------------------------------------
# 8. Data Type Validation
# ---------------------------------------------------------------------------

def validate_numeric_columns(
    df: pd.DataFrame,
    name: str,
    columns: list[str] | None = None,
) -> None:
    """Pastikan kolom-kolom numerik memang bertipe numerik.

    Args:
        columns: List kolom yang harus numerik.
                 Jika None, otomatis semua kolom kecuali 'club'.

    Raises:
        ValueError: Jika ada kolom yang seharusnya numerik tapi bukan.
    """
    if columns is None:
        columns = [c for c in df.columns if c != "club"]

    non_numeric = []
    for col in columns:
        if col not in df.columns:
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            non_numeric.append(f"{col} (dtype={df[col].dtype})")

    if non_numeric:
        raise ValueError(
            f"[DQ FAIL] {name}: Kolom berikut seharusnya numerik → "
            f"{', '.join(non_numeric)}"
        )
    logger.info("  ✓ Numeric types: %d kolom valid", len(columns))


# ---------------------------------------------------------------------------
# 9. Percentage Validation
# ---------------------------------------------------------------------------

def validate_percentages(
    df: pd.DataFrame,
    name: str,
    columns: list[str],
) -> None:
    """Pastikan kolom persentase berada di rentang 0–100.

    Raises:
        ValueError: Jika ada nilai di luar rentang 0–100.
    """
    if not columns:
        logger.info("  ✓ Percentage: tidak ada kolom pct untuk dicek")
        return

    violations = []
    for col in columns:
        if col not in df.columns:
            continue
        out_of_range = df[(df[col] < 0) | (df[col] > 100)]
        if not out_of_range.empty:
            bad_values = out_of_range[[col, "club"]].to_dict("records") \
                if "club" in df.columns \
                else out_of_range[[col]].to_dict("records")
            violations.append(f"{col}: {bad_values}")

    if violations:
        raise ValueError(
            f"[DQ FAIL] {name}: Nilai persentase di luar 0-100 → "
            f"{'; '.join(violations)}"
        )
    logger.info("  ✓ Percentages: %d kolom dalam rentang 0-100", len(columns))


# ---------------------------------------------------------------------------
# 10. Range Validation
# ---------------------------------------------------------------------------

def validate_ranges(
    df: pd.DataFrame,
    name: str,
    range_specs: dict[str, tuple[float, float]] | None = None,
) -> None:
    """Cek apakah nilai numerik berada di rentang yang wajar.

    Warning (non-fatal) — hanya logging, tidak raise error.

    Args:
        range_specs: Dict mapping nama_kolom → (min, max).
                     Jika None, gunakan DEFAULT_RANGES sebagai heuristik.
    """
    if range_specs is None:
        # Auto-match kolom dengan DEFAULT_RANGES berdasarkan nama
        range_specs = {}
        for col in df.columns:
            if col == "club":
                continue
            # Exact match
            if col in DEFAULT_RANGES:
                range_specs[col] = DEFAULT_RANGES[col]

    if not range_specs:
        logger.info("  ✓ Range: tidak ada range spec untuk dicek")
        return

    warnings_found = False
    for col, (low, high) in range_specs.items():
        if col not in df.columns:
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            continue

        out = df[(df[col] < low) | (df[col] > high)]
        if not out.empty:
            warnings_found = True
            if "club" in df.columns:
                details = [
                    f"{row['club']}={row[col]}"
                    for _, row in out.iterrows()
                ]
            else:
                details = [str(v) for v in out[col].tolist()]
            logger.warning(
                "  ⚠ %s: Kolom '%s' di luar rentang wajar (%s–%s) → %s",
                name, col, low, high, ", ".join(details),
            )

    if not warnings_found:
        logger.info("  ✓ Range: %d kolom dalam rentang wajar", len(range_specs))


# ---------------------------------------------------------------------------
# 11. Consistency Validation
# ---------------------------------------------------------------------------

def validate_consistency(
    df: pd.DataFrame,
    name: str,
    column: str = "played",
    expected_value: Any = 38,
) -> None:
    """Pastikan satu kolom memiliki nilai yang sama untuk semua baris.

    Raises:
        ValueError: Jika ada baris dengan nilai berbeda.
    """
    if column not in df.columns:
        logger.info("  ✓ Consistency: kolom '%s' tidak ada, skip", column)
        return

    unique_values = df[column].unique()
    if len(unique_values) != 1 or unique_values[0] != expected_value:
        raise ValueError(
            f"[DQ FAIL] {name}: Kolom '{column}' tidak konsisten. "
            f"Diharapkan semua = {expected_value}, "
            f"ditemukan = {sorted(unique_values)}"
        )
    logger.info("  ✓ Consistency: '%s' = %s untuk semua baris", column, expected_value)


# ---------------------------------------------------------------------------
# WRAPPER — Jalankan semua validasi sekaligus
# ---------------------------------------------------------------------------

def run_all_validations(
    df: pd.DataFrame,
    name: str,
    *,
    expected_columns: list[str],
    pct_columns: list[str] | None = None,
    expected_rows: int = 20,
    played_value: int | None = 38,
    valid_clubs: set[str] | None = None,
    range_specs: dict[str, tuple[float, float]] | None = None,
) -> pd.DataFrame:
    """Jalankan seluruh validasi DQ secara berurutan.

    Args:
        df: DataFrame yang akan divalidasi (setelah cleaning).
        name: Nama tabel/file untuk logging.
        expected_columns: Daftar kolom yang diharapkan.
        pct_columns: Kolom persentase (harus 0–100).
        expected_rows: Jumlah baris yang diharapkan (default: 20).
        played_value: Nilai yang diharapkan untuk kolom 'played'.
                      None jika tabel tidak punya kolom 'played'.
        valid_clubs: Set nama club yang valid. None = LALIGA_CLUBS.
        range_specs: Dict range per kolom. None = auto-detect.

    Returns:
        DataFrame yang sudah divalidasi (dengan whitespace di-strip).
    """
    logger.info("── DQ Validation: %s ──", name)

    # 1. Empty check (paling fundamental)
    validate_not_empty(df, name)

    # 2. Schema check (pastikan kolom lengkap sebelum cek lainnya)
    validate_schema(df, name, expected_columns)

    # 3. Missing values
    validate_no_missing(df, name)

    # 4. Whitespace strip (satu-satunya modifikasi)
    df = validate_strip_whitespace(df, name)

    # 5. Duplicate check (setelah whitespace di-strip)
    validate_no_duplicates(df, name)

    # 6. Row count
    validate_expected_rows(df, name, expected_rows)

    # 7. Club name validation
    validate_club_names(df, name, valid_clubs)

    # 8. Numeric type check
    validate_numeric_columns(df, name)

    # 9. Percentage range
    validate_percentages(df, name, pct_columns or [])

    # 10. Range sanity check
    validate_ranges(df, name, range_specs)

    # 11. Consistency (played = 38)
    if played_value is not None:
        validate_consistency(df, name, "played", played_value)

    logger.info("── DQ Validation: %s — PASSED ✅ ──\n", name)
    return df
