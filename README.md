# FastAPI Template

これは、GoogleBook APIを使って書籍管理をするweb apiで、学習用のテンプレートプロジェクトです。

## 🛠️ 主要技術

- **Python 3.11**
- **FastAPI**
- **SQLAlchemy**
- **Alembic**
- **Poetry**
- **Pytest**
- **Docker / Dev Containers**

## 🚀 セットアップと実行

### 1. 前提条件

- [Docker](https://www.docker.com/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### 2. 環境構築

1.  このリポジトリをクローンします。
2.  VS Codeでプロジェクトフォルダを開きます。
3.  コマンドパレット (`Ctrl+Shift+P` or `Cmd+Shift+P`) を開き、`"Remote-Containers: Reopen in Container"` を選択します。

VS Codeがコンテナをビルドし、開発環境を自動的にセットアップします。

### 3. 開発サーバーの起動

コンテナ内のターミナルで以下のコマンドを実行すると、Uvicorn開発サーバーが起動します。

```bash
task dev
```

サーバーは `http://localhost:8000` で利用可能になります。

## ✅ テスト

テストスイート全体を実行するには、以下のコマンドを使用します。

```bash
task test
```

## DATABASE

### データベースマイグレーション

Alembicを使用してデータベースのスキーマを管理します。

- **マイグレーションの適用:**
  ```bash
  task db_upgrade
  ```
- **マイグレーションの生成:**
  モデルに変更を加えた後、新しいマイグレーションファイルを生成します。
  ```bash
  task db_revision "あなたのマイグレーションメッセージ"
  ```
- **マイグレーションのロールバック:**
  ```bash
  task db_downgrade
  ```

## 💅 コード品質

コードの品質を維持するためのコマンドが用意されています。

- **リンティング (Pylint):**
  ```bash
  task lint
  ```
- **インポートのフォーマット (isort):**
  ```bash
  task format_isort
  ```
- **コードのフォーマット (autopep8):**
  ```bash
  task format_autopep8
  ```

## 📁 フォルダ構造

```
/
├── .devcontainer/   # Dev Container設定
├── app/             # アプリケーションソースコード
│   ├── migration/   # Alembicマイグレーションファイル
│   ├── models/      # SQLAlchemyモデル
│   ├── routers/     # APIルーター
│   ├── schemas/     # Pydanticスキーマ
│   ├── services/    # ビジネスロジック
│   └── main.py      # FastAPIアプリケーションのエントリポイント
├── test/            # テストコード
├── pyproject.toml   # プロジェクト設定と依存関係 (Poetry)
└── README.md        # このファイル
```

## 📄 ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。