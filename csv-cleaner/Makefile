# 仮想環境のセットアップ
setup:
	python -m venv venv
	venv\Scripts\Activate.ps1 && pip install -r requirements.txt

# 仮想環境のアクティベート
activate:
	venv\Scripts\Activate.ps1

# 依存関係のインストール
install:
	pip install -r requirements.txt

# 仮想環境の削除
clean:
	rmdir /s /q venv

# サンプル実行
run:
	python csv_cleaner.py --input sample_input.csv --output cleaned.csv --config config.sample.yaml --report report.json

# ヘルプ
help:
	@echo "利用可能なコマンド:"
	@echo "  setup    - 仮想環境を作成し、依存関係をインストール"
	@echo "  activate - 仮想環境をアクティベート"
	@echo "  install  - 依存関係をインストール"
	@echo "  run      - サンプルCSVファイルで実行"
	@echo "  clean    - 仮想環境を削除"
	@echo "  help     - このヘルプを表示"
