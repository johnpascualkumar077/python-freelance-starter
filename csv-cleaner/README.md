# csv-cleaner

ファイル整形を自動化するCLI。欠損補完・重複排除・型変換・日付整形・空白除去・列並び替えをYAMLで定義。

## 使い方

```bash
# インストール
pip install -r requirements.txt

# 実行例
python csv_cleaner.py   --input sample_input.csv   --output cleaned.csv   --config config.sample.yaml   --report report.json
```

- `--input`: CSV/Excel(.xlsx)対応
- `--output`: CSV出力。`--to-excel`指定でExcel出力
- `--config`: ルールをYAMLで指定
- `--report`: 実行レポート(JSON)。件数や補完数など

## ルール(YAML)の例

```yaml
read:
  encoding: utf-8
  header: 0
cleaning:
  strip_whitespace: true
  drop_duplicates: true
  drop_na_rows_if_all_na: true
  fillna:
    price: 0
    note: ""
  dtype:
    id: int64
    price: float64
  parse_dates:
    - order_date
  date_format: "%Y-%m-%d"
  columns_order:
    - id
    - name
    - order_date
    - price
    - note
output:
  to_excel: false
```

## 入出力サンプル

- 入力: `sample_input.csv`
- 出力: `sample_output_expected.csv`

## ライセンス

MIT
