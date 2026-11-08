# 自动同步图片（可选）

我这边推 `workflow` 目录被 GitHub 挡住了（403 Resource not accessible by personal access token，
token 缺 `workflow` scope），所以这个文件先躺在 docs 里。

想开自动同步，两件事：

1. 把本文件拷到 `.github/workflows/sync-images.yml`（网页上 Add file 也行）；
2. 只搬 `license: open` 的条目 —— 斗图啦那些 `net` 的图不搬，版权不替别人背书。

```yaml
name: sync-images

on:
  workflow_dispatch:
  schedule:
    - cron: "0 3 * * 1"
  push:
    paths: ["stickers.json", "tools/sticker.py", ".github/workflows/sync-images.yml"]

permissions:
  contents: write

concurrency:
  group: sync-images
  cancel-in-progress: true

jobs:
  fetch:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python tools/sticker.py fetch-all --license open -o images
      - continue-on-error: true
        run: python tools/sticker.py check
      - run: |
          git config user.name "tsundere-bot"
          git config user.email "bot@users.noreply.github.com"
          git add images
          if git diff --cached --quiet; then echo "没有变化"; exit 0; fi
          git commit -m "chore: sync open-license images"
          git push
```

不想用 Actions 就本地跑，一条命令的事：

```bash
python tools/sticker.py fetch-all --license open -o images
```
