#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pathlib import Path
import typer
import pandas as pd
import yaml
from typing import Optional

app = typer.Typer(help="CSV/ExcelをYAMLルールで一括整形するCLI")

def load_df(input_path: Path, encoding: str = "utf-8", header: int = 0) -> pd.DataFrame:
    if input_path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(input_path, header=header)
    return pd.read_csv(input_path, encoding=encoding, header=header)

def apply_cleaning(df: pd.DataFrame, cfg: dict) -> tuple[pd.DataFrame, dict]:
    changes = {"rows_in": len(df), "rows_out": None, "filled": {}, "dropped_duplicates": 0}
    cleaning = cfg.get("cleaning", {})
    # strip whitespace
    if cleaning.get("strip_whitespace", False):
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype(str).str.strip()
    # parse dates
    for c in cleaning.get("parse_dates", []):
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    # dtype
    for col, dt in cleaning.get("dtype", {}).items():
        if col in df.columns:
            try:
                if str(dt).startswith("int"):
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64").astype(dt)
                else:
                    df[col] = df[col].astype(dt)
            except Exception:
                pass
    # fillna
    for col, v in cleaning.get("fillna", {}).items():
        if col in df.columns:
            before_na = df[col].isna().sum()
            df[col] = df[col].fillna(v)
            after_na = df[col].isna().sum()
            changes["filled"][col] = int(before_na - after_na)
    # drop rows that are all NA
    if cleaning.get("drop_na_rows_if_all_na", False):
        df = df.dropna(how="all")
    # drop duplicates
    if cleaning.get("drop_duplicates", False):
        before = len(df)
        df = df.drop_duplicates()
        changes["dropped_duplicates"] = int(before - len(df))
    # date format
    fmt = cleaning.get("date_format")
    if fmt:
        for c in cleaning.get("parse_dates", []):
            if c in df.columns:
                df[c] = pd.to_datetime(df[c], errors="coerce").dt.strftime(fmt)
    # reorder columns
    order = cleaning.get("columns_order")
    if order:
        cols = [c for c in order if c in df.columns]
        rest = [c for c in df.columns if c not in cols]
        df = df[cols + rest]
    changes["rows_out"] = len(df)
    return df, changes

@app.command()
def run(
    input: Path = typer.Option(..., exists=True, help="入力CSV/Excelファイル"),
    output: Path = typer.Option(..., help="出力CSVまたはExcel"),
    config: Path = typer.Option(..., exists=True, help="YAMLルールファイル"),
    report: Optional[Path] = typer.Option(None, help="処理レポートJSON"),
):
    cfg = yaml.safe_load(config.read_text(encoding="utf-8"))
    read_cfg = cfg.get("read", {})
    df = load_df(input, encoding=read_cfg.get("encoding", "utf-8"), header=read_cfg.get("header", 0))
    cleaned, changes = apply_cleaning(df, cfg)
    out_excel = bool(cfg.get("output", {}).get("to_excel", False)) or output.suffix.lower() in [".xlsx", ".xls"]
    if out_excel:
        cleaned.to_excel(output, index=False)
    else:
        cleaned.to_csv(output, index=False, encoding="utf-8")
    if report:
        report.write_text(json.dumps(changes, ensure_ascii=False, indent=2), encoding="utf-8")
    typer.echo(f"Done. rows: {changes['rows_in']} -> {changes['rows_out']} | dup_dropped={changes['dropped_duplicates']}")

if __name__ == "__main__":
    app()
