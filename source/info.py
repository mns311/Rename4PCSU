import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

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
        pp_files = []
        exd_files = []
        ind_files = []
        other_files = []
        reflection_files = []  # 振り返りシート用リスト

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if 'PP' in file:
                    pp_files.append(file)
                elif 'ExD' in file:
                    exd_files.append(file)
                elif 'InD' in file:
                    ind_files.append(file)
                elif '振り返りシート' in file:  # 振り返りシートを判定
                    reflection_files.append(file)
                else:
                    other_files.append(file)

        display_classified_files(pp_files, exd_files, ind_files, reflection_files, other_files)
    except Exception as e:
        messagebox.showerror("エラー", f"フォルダのファイルの分類中にエラーが発生しました: {e}")

def extract_and_classify_selected_files(file_paths):
    try:
        pp_files = []
        exd_files = []
        ind_files = []
        other_files = []
        reflection_files = []  # 振り返りシート用リスト

        for file in file_paths:
            if 'PP' in file:
                pp_files.append(os.path.basename(file))
            elif 'ExD' in file:
                exd_files.append(os.path.basename(file))
            elif 'InD' in file:
                ind_files.append(os.path.basename(file))
            elif '振り返りシート' in file:  # 振り返りシートを判定
                reflection_files.append(os.path.basename(file))
            else:
                other_files.append(os.path.basename(file))

        display_classified_files(pp_files, exd_files, ind_files, reflection_files, other_files)
    except Exception as e:
        messagebox.showerror("エラー", f"選択されたファイルの分類中にエラーが発生しました: {e}")

def display_classified_files(pp_files, exd_files, ind_files, reflection_files, other_files):
    text_files.delete('1.0', tk.END)  # テキストボックスをクリア

    text_files.insert(tk.END, "ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー\n")
    # フォーマットに従ってファイルを出力
    if pp_files:
        text_files.insert(tk.END, "＜PP＞\n")
        for file in pp_files:
            text_files.insert(tk.END, f"・{file}\n")

    if exd_files:
        text_files.insert(tk.END, "＜配布データ＞\n")
        for file in exd_files:
            text_files.insert(tk.END, f"・{file}\n")

    if ind_files:
        text_files.insert(tk.END, "＜内部データ＞\n")
        for file in ind_files:
            text_files.insert(tk.END, f"・{file}\n")

    if reflection_files:
        text_files.insert(tk.END, "＜振り返りシート＞\n")  # 振り返りシートのセクション
        for file in reflection_files:
            text_files.insert(tk.END, f"・{file}\n")

    if other_files:
        text_files.insert(tk.END, "＜その他＞\n")
        for file in other_files:
            text_files.insert(tk.END, f"・{file}\n")

    text_files.insert(tk.END, "ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー\n")


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

# スクロールバー
scrollbar_y = ttk.Scrollbar(root, orient="vertical", command=text_files.yview)
scrollbar_y.grid(row=1, column=1, sticky="ns")
text_files.config(yscrollcommand=scrollbar_y.set)

scrollbar_x = ttk.Scrollbar(root, orient="horizontal", command=text_files.xview)
scrollbar_x.grid(row=2, column=0, sticky="ew")
text_files.config(xscrollcommand=scrollbar_x.set)

root.mainloop()
