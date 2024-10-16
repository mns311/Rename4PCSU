#version_Mk4(2024/10/16)
import os
import re
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

def extract_version_from_filename(filename):
    match = re.search(r'v\d+\.\d+\.\d+', filename)
    if match:
        return match.group(0)
    return ""

def select_files():
    file_paths = filedialog.askopenfilenames()  # ファイルを複数選択
    if file_paths:
        entry_files.delete(0, tk.END)
        entry_files.insert(0, ', '.join(file_paths))
        first_version = extract_version_from_filename(os.path.basename(file_paths[0]))
        entry_current_version.delete(0, tk.END)
        entry_current_version.insert(0, first_version)

def select_folder():
    folder_path = filedialog.askdirectory()  # フォルダを選択
    if folder_path:
        entry_folder.delete(0, tk.END)
        entry_folder.insert(0, folder_path)

        # 選択されたフォルダ内のファイルから最初のバージョンを抽出
        files = []
        file_paths = []
        
        for root_dir, dirs, file_list in os.walk(folder_path):
            for file in file_list:
                if extract_version_from_filename(file):  # バージョンを持つファイルのみをリストに追加
                    full_path = os.path.join(root_dir, file)  # フルパスを取得
                    files.append(file)
                    file_paths.append(full_path)
                    
        if files:
            first_version = extract_version_from_filename(files[0])
            entry_current_version.delete(0, tk.END)
            entry_current_version.insert(0, first_version)
            entry_files.delete(0, tk.END)
            entry_files.insert(0, ', '.join(file_paths))
        else:
            messagebox.showwarning("警告", "フォルダ内にバージョン付きファイルが見つかりませんでした。")





def update_version():
    selected_version = selected_version_type.get()
    version_dict = {
    "1. モギモギ": "v1.0.0",
    "2. 模擬": "v2.0.0",
    "3. 納入": "v3.0.0",
    "4. 最終確認": "v4.0.0",
    "5. 講座用データ": "v5.0.0",
    "6. 振り返り": "v6.0.0",
    "7. その他": "v.."
    }

    entry_new_version.delete(0, tk.END)
    entry_new_version.insert(0, version_dict[selected_version])

def show_file_list_window(filepaths):
    file_list_window = tk.Toplevel(root)
    file_list_window.title("ファイルリスト")

    # ヘッダーラベル
    ttk.Label(file_list_window, text="変更前のファイル名").grid(row=0, column=0, padx=10, pady=5, sticky="ew")
    ttk.Label(file_list_window, text="変更後のファイル名").grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    old_new_filenames = []  # 変更前と変更後のフルファイルパスを格納するリスト
    new_version = entry_new_version.get()  # ユーザーが指定した新しいバージョンを取得

    # ファイル名を取得し、新しいファイル名を生成
    for i, filepath in enumerate(filepaths):
        old_filename = os.path.basename(filepath)  # ファイルパスからファイル名のみを取得
        dir_name = os.path.dirname(filepath)  # 親ディレクトリを取得

        # 新しいファイル名を生成 (バージョン番号を置換)
        if new_version:  # 新しいバージョンが指定されている場合
            new_filename = re.sub(r'v\d+\.\d+\.\d+', new_version, old_filename)  # 正規表現でバージョン部分を置換
        else:
            new_filename = old_filename  # バージョンが指定されていない場合、変更なし

        # フルパスを生成してリストに保存
        old_new_filenames.append((filepath, os.path.join(dir_name, new_filename)))

        # 変更前のファイル名と変更後のファイル名をウィンドウに表示
        ttk.Label(file_list_window, text=old_filename).grid(row=i+1, column=0, padx=10, pady=5, sticky="ew")
        ttk.Label(file_list_window, text=new_filename).grid(row=i+1, column=1, padx=10, pady=5, sticky="ew")

    def apply_changes():
        """ファイル名変更を実行する処理"""
        for old_filepath, new_filepath in old_new_filenames:
            try:
                # すでにフルパスが保存されているので、そのままリネーム
                if old_filepath != new_filepath:  # 同じ名前でない場合のみリネーム
                    os.rename(old_filepath, new_filepath)
            except Exception as e:
                messagebox.showerror("エラー", f"ファイル名の変更に失敗しました: {e}")
                return

        messagebox.showinfo("成功", "ファイルのバージョンを更新したよ！どういたしまして^^")
        file_list_window.destroy()

    def cancel_changes():
        """キャンセルボタンの処理"""
        file_list_window.destroy()

    # キャンセルと変更ボタンを追加
    ttk.Button(file_list_window, text="キャンセル", command=cancel_changes).grid(row=len(filepaths)+1, column=0, pady=10, sticky="ew")
    ttk.Button(file_list_window, text="変更", command=apply_changes).grid(row=len(filepaths)+1, column=1, pady=10, sticky="ew")


def update_versions():
    file_paths = entry_files.get().split(', ')
    if not file_paths:
        messagebox.showerror("エラー", "ファイルが選択されていません。")
        return

    # ファイルリストウィンドウを開いて、変更前後のファイル名を表示
    show_file_list_window(file_paths)


# GUIのセットアップ
root = tk.Tk()
root.title("バージョンタイプ更新")

# Setting style for ttk widgets
style = ttk.Style()
style.configure('TButton')  
style.configure('TLabel')
style.configure('TEntry')
style.configure('TRadiobutton')

root.bind('<Configure>')

# ファイルとフォルダ選択を1行に配置
frame_select = ttk.Frame(root)
frame_select.grid(row=0, column=0, padx=5, pady=5, sticky="ew", columnspan=3)

# ファイル選択ボタンとエントリー
ttk.Label(frame_select, text="ファイルを選択").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_files = ttk.Entry(frame_select, width=30)
entry_files.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
ttk.Button(frame_select, text="ファイルを選択", command=select_files).grid(row=0, column=2, padx=5, pady=5, sticky="ew")

# フォルダ選択ボタンとエントリー
ttk.Label(frame_select, text="フォルダを選択").grid(row=0, column=3, padx=5, pady=5, sticky="e")
entry_folder = ttk.Entry(frame_select, width=30)
entry_folder.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
ttk.Button(frame_select, text="フォルダを選択", command=select_folder).grid(row=0, column=5, padx=5, pady=5, sticky="ew")

# 現在のバージョンラベルとエントリー
ttk.Label(root, text="現在のバージョン").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_current_version = ttk.Entry(root)
entry_current_version.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# バージョンタイプラベルとエントリー
ttk.Label(root, text="バージョンタイプ").grid(row=2, column=0, padx=5, pady=5, sticky="e")

frame_version = ttk.Frame(root)
frame_version.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

version_options = [
"1. モギモギ", "2. 模擬",
"3. 納入", "4. 最終確認", "5. 講座用データ", "6. 振り返り", "7. その他"
]
selected_version_type = tk.StringVar(value="")
for i, version in enumerate(version_options):
    ttk.Radiobutton(frame_version, text=version, variable=selected_version_type, value=version, command=update_version).grid(row=i // 4, column=i % 4, padx=5, pady=5, sticky="ew")

# 変更後のバージョンラベルとエントリー
ttk.Label(root, text="変更後のバージョン").grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_new_version = ttk.Entry(root)
entry_new_version.insert(0, "v0.0.0")
entry_new_version.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

# バージョンを更新するボタン
ttk.Button(root, text="バージョンを更新", command=update_versions).grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")

root.mainloop()


