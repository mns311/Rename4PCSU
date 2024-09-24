# Rename4PCSU
PCSU内の命名規則に沿ってファイル名を一括編集します．<br>
※フォルダを選択すると変更をサブフォルダまで反映できます．


## How to use
1. "Rename4PCSU.py", "source" をダウンロード
2. "Rename4PCSU.py" を実行
3. 使用したいアプリケーションを選択
    * ファイル名生成<br>
       1. ボタンや入力フィールドを記入
       2. 「ファイル名生成」をクリックしてファイルの選択<br>
     * バージョン更新<br>
       1. 変更したいファイル，またはフォルダを選択
       2. バージョン情報を自由に変更<br>
    ※③を選択→メジャー　➃を変更→マイナー，ビルド
    * ファイル名生成<br>
       1. 変更したいファイル，またはフォルダを選択
    

## Config
### ファイル名生成：gen.py
PCSU内のファイルの命名則を生成<br>
例：25年度スタンダード講座第１講モギモギ用データ<br>
PP.pptx→25-Std1stPPv2.0.0.pptx
第１回課題.pdf→ 25-Std1stExD（第１回課題）v2.0.0.pdf
### バージョン更新：upd.py
ファイルのバージョンを更新<br>
例：モギモギ→模擬<br>
25-Std1stExD（第１回課題）v2.0.0.pdf → 25-Std1stExD（第１回課題）v3.0.0.pdf
### 配布データ化：del.py
PCSU内のファイルの命名則を削除<br>
例：講座用データ→配布データ<br>
25-Std1stExD（第１回課題）v6.0.0.pdf → 第１回課題.pdf<br>



