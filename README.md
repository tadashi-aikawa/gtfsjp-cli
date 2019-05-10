# gtfscli

CLI for [GTFS-JP]

[GTFS-JP]: https://www.gtfs.jp/developpers-guide/format-reference.html

One of usage.

```
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
```


## For developer

### Requirements

* pipenv

### Commands

#### Create and activate env

```
$ pipenv install -d
$ pipenv shell
```
