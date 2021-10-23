# 関東ウナギ釣り掲示板記事抽出

[釣り掲示板](http://hazebbs.com/f/index.html)から、関東ウナギ釣りに関する記事を抽出して、CSVに変換します。


[KH Coder](https://khcoder.net/)のテキスト分析の入力データとして使用します。

## インストール

```
cd unasearch
pip install --editable .  
```

## 使用方法

```
unasearch > hazebbs.csv
```

## KH Coder 設定

KH Coder 起動して以下の設定をしてください。

メニュー : プロジェクト --> 新規を選択し、新規プロジェクト画面から以下を設定します。

* 分析対象ファイル : CSV ファイルを指定
* 分析対象 : content 列


メニュー : 前処理 --> 語の取捨選択を選択し、使用しない語リストに以下を追加します。


```
ウナギ
うなぎ
```
