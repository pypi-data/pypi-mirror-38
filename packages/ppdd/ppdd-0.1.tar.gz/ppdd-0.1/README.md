# Picture Placement by Dated Directory

実行すると指定されたフォルダの画像（JPGとPNG）からEXIFを取得し、日付ごとにフォルダ分けを行います。

## インストール

```bash
pip install ppdd
```

もしくは、

```bash
git clone https://github.com/Sakaki/ppdd.git
pip install ppdd
```

## 使い方

```bash
$ ppdd /many/images/dir
INFO:Move IMAGE1.JPG to /many/images/dir/2012_03_12
INFO:Move IMAGE2.JPG to /many/images/dir/2012_03_17
INFO:Move IMAGE3.JPG to /many/images/dir/2012_03_09
...
INFO:Processed 67 file(s)
```

パスに何も指定しないとカレントディレクトリが対象になります。

```bash
$ ppdd --help
Usage: ppdd [OPTIONS] [DIR_NAME]

Options:
  --suffix TEXT  Directory name suffix (ex: 20XX_XX_XX_suffix)
  --debug        Print debug information
  --help         Show this message and exit.
```
