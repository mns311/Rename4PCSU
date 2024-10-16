#Mk4(2024/10/16)
import os
import re
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

# バージョンと日本語の関連付け
version_mapping = {
    "1. モギモギ": "v1.0.0",
    "2. 模擬": "v2.0.0",
    "3. 納入": "v3.0.0",
    "4. 最終確認": "v4.0.0",
    "5. 講座": "v5.0.0",
    "6. 振り返り": "v6.0.0",
    "7. その他": "v.."
}

# バージョンから用途へのマッピング
usage_mapping = {
    "v1.0.0": "モギモギ",
    "v2.0.0": "模擬",
    "v3.0.0": "納入",
    "v4.0.0": "最終確認",
    "v5.0.0": "講座",
    "v6.0.0": "振り返り",
    "v..": "その他"
}

def select_folder():
    folder_path = filedialog.askdirectory()  # フォルダを選択
    if folder_path:
        entry_folder.delete(0, tk.END)
        entry_folder.insert(0, folder_path)
        extract_and_classify_files(folder_path)

def select_files():
    file_paths = filedialog.askopenfilenames()  # 複数ファイルを選択
    if file_paths:
        entry_files.delete(0, tk.END)  # テキストボックスをクリア
        entry_files.insert(0, ', '.join(file_paths))  # 選択されたファイルのパスを表示
        extract_and_classify_selected_files(file_paths)  # 選択されたファイルの分類を実行

def extract_and_classify_files(folder_path):
    try:
        file_list = []
        for root, dirs, files in os.walk(folder_path):
            file_list.extend(files)
        
        classified_files = extract_and_classify_files_common(file_list)
        display_classified_files(classified_files)
    except Exception as e:
        messagebox.showerror("エラー", f"フォルダのファイルの分類中にエラーが発生しました: {e}")

def classify_file(file_name):
    """ファイル名に基づいて分類を行う"""
    if 'PP' in file_name:
        return 'PP'
    elif 'ExD' in file_name:
        return '配布データ'
    elif 'InD' in file_name:
        return '内部データ'
    elif '振り返りシート' in file_name:
        return '振り返りシート'
    else:
        return 'その他'

def extract_and_classify_files_common(file_list):
    """共通の分類処理"""
    classified_files = {
        'PP': [],
        '配布データ': [],
        '内部データ': [],
        '振り返りシート': [],
        'その他': []
    }
    
    for file in file_list:
        category = classify_file(file)
        classified_files[category].append(file)
    
    return classified_files

def extract_and_classify_selected_files(file_paths):
    try:
        file_names = [os.path.basename(file) for file in file_paths]
        classified_files = extract_and_classify_files_common(file_names)
        display_classified_files(classified_files)
    except Exception as e:
        messagebox.showerror("エラー", f"選択されたファイルの分類中にエラーが発生しました: {e}")

def get_main_file(classified_files):
    """主要なファイルから情報を抽出する。PPが存在すればPPから、なければ他から。"""
    if classified_files['PP']():
        return classified_files['PP'][0]
    else:
        # 他のカテゴリから最初のファイルを取得
        for category in ['配布データ', '内部データ', '振り返りシート', 'その他']:
            if classified_files[category]:
                return classified_files[category][0]
    return None

def display_classified_files(classified_files):
    """分類されたファイルを表示"""
    text_files.delete('1.0', tk.END)  # テキストボックスをクリア
    
    # 最初のファイルを取得（PP、ExDなど、どの種類でも）
    first_file = next((file for files in classified_files.values() for file in files), None)

    if first_file:
        pattern = r'(?P<year>\d+)-(?P<course_type>[A-Za-z]+)(?P<course_number>\d+\w+)(?P<file_type>ExD|PP)(?:（[^）]+）)?v(?P<version>\d+\.\d+\.\d+)\.(?P<ext>.+)'
        match = re.match(pattern, first_file)

        if match:
            year = match.group('year')
            course_type = match.group('course_type')
            course_number = match.group('course_number')
            version = match.group('version')
            version_major = version.split('.')[0]  # メジャーバージョンを取得

            # メジャーバージョンに基づく日本語の取得
            version_japanese = next((jp.split('. ')[1] for jp in version_mapping if version_mapping[jp] == f"v{version_major}.0.0"), "その他")
            usage_japanese = version_japanese  # メジャーバージョンに基づく用途を使用

            # 出力項目の作成
            text_files.insert(tk.END, f"【データアップ報告 {year}-{course_type}{course_number}】\n")
            text_files.insert(tk.END, f"{year}-{course_type}{course_number}の{usage_japanese}用データをCANVASにアップロードしました。\n")
            text_files.insert(tk.END, f"《用途》{usage_japanese}\n")
            text_files.insert(tk.END, "《場所》\n")
            text_files.insert(tk.END, "ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー\n")
        else:
            text_files.insert(tk.END, "ファイル名の形式が正しくありません。\n")
    else:
        # すべてのファイルが存在しない場合の処理
        text_files.insert(tk.END, "ファイルが見つかりませんでした。\n")

    # 各カテゴリのファイルを表示
    for category, files in classified_files.items():
        if files:
            text_files.insert(tk.END, f"＜{category}＞\n")
            for file in files:
                text_files.insert(tk.END, f"・{file}\n")

    text_files.insert(tk.END, "ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー\n")

# クリップボードにコピーする関数
def copy_to_clipboard():
    try:
        root.clipboard_clear()  # クリップボードをクリア
        text_content = text_files.get('1.0', tk.END)  # テキストウィジェットの内容を取得
        root.clipboard_append(text_content)  # クリップボードにテキストをコピー
        messagebox.showinfo("成功", "ファイル名をクリップボードにコピーしたよ^^\nSlackでみんなに報告しよう!")
    except Exception as e:
        messagebox.showerror("エラー", f"クリップボードへのコピー中にエラーが発生しました: {e}")

# GUIのセットアップ
root = tk.Tk()
root.title("ファイル名取得")

frame_select = ttk.Frame(root)
frame_select.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

# ファイルを複数選択するボタンと入力フィールド
ttk.Label(frame_select, text="ファイルを選択").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_files = ttk.Entry(frame_select, width=30)
entry_files.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
ttk.Button(frame_select, text="ファイルを選択", command=select_files).grid(row=0, column=2, padx=5, pady=5, sticky="ew")

# フォルダを選択するボタンと入力フィールド
ttk.Label(frame_select, text="フォルダを選択").grid(row=0, column=3, padx=5, pady=5, sticky="e")
entry_folder = ttk.Entry(frame_select, width=30)
entry_folder.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
ttk.Button(frame_select, text="フォルダを選択", command=select_folder).grid(row=0, column=5, padx=5, pady=5, sticky="ew")

# ファイルリストを表示するTextウィジェット
text_files = tk.Text(root, width=80, height=20, wrap='none')  # コピー可能にするため、Textウィジェットを使用
text_files.grid(row=1, column=0, padx=5, pady=5)

# クリップボードにコピーするボタン
ttk.Button(root, text="クリップボードにコピー", command=copy_to_clipboard).grid(row=2, column=0, padx=5, pady=5, sticky="ew")

root.mainloop()
