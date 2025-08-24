# python-freelance-starter

CSV整形・PDF→表変換・価格監視など、中小業務の自動化に役立つミニツール集。  
LancersやCrowdWorksなどで即提案できるサンプルコードをまとめています。

---

## 含まれるツール

### 1. csv-cleaner
- CSV/ExcelをYAMLルールに基づいて一括整形  
- 欠損補完・重複削除・型変換・日付整形・列並び替え対応  
- CLI実行で再利用可能  
```bash
python csv_cleaner.py --input sample_input.csv --output cleaned.csv --config config.sample.yaml --report report.json
