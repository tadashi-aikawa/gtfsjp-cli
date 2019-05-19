# gtfscli

**⚠ 本プロジェクトはお試し版であり、開発中です**

[GTFS-JP]に準拠したデータを操作するCLIです。

[GTFS-JP]: https://www.gtfs.jp/developpers-guide/format-reference.html

実行例

```
# データソース作成
$ python gtfscli\main.py init db <gtfs_dir_path>

# 停留所/標柱情報取得コマンドのヘルプ表示
$ python gtfscli\main.py get stop -h
Get data related to stops

Usage:
  gtfscli get stop --id <id> <dir>
  gtfscli get stop (-w <word> | --word <word>) <dir>
  gtfscli get stop (-h | --help)

Options:
  --id <id>                         Stop id
  -w, --word <word>                 Search word for stop name
  <dir>                             GTFS dir
  -h --help                         Show this screen.

# 東京駅に部分一致するものを取得
$ python gtfscli\main.py get stop -w 東京
...
```


## 開発者向け

### 動作要件

* pipenv

### コマンド

#### 仮想環境作成とActivate

```
$ pipenv install -d
$ pipenv shell
```

### アーキテクチャ

[![](https://cacoo.com/diagrams/FaXrS1rZ5c7SUxiF-4B5CE.png)](https://cacoo.com/diagrams/FaXrS1rZ5c7SUxiF/4B5CE)
