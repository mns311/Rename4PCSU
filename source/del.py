import os
import re
import tkinter as tk
from tkinter import filedialog, ttk, messagebox


def extract_info_from_filename(filename):
    # "ExD" の後の括弧内の部分と拡張子を抽出
    match = re.search(r'ExD[（(](.+?)[）)]v[\d.]+(\.\w+)$', filename)
    if match:
        name, ext = match.groups()
        return name, ext
    return None, None




def update_button_state():
    # ファイルまたはフォルダが選択されている場合にボタンを有効化
    if entry_files.get() or entry_folder.get():
        btn_rename_files.config(state=tk.NORMAL)
    else:
        btn_rename_files.config(state=tk.DISABLED)

def select_files():
    file_paths = filedialog.askopenfilenames()  # ファイルを複数選択
    if file_paths:
        entry_files.delete(0, tk.END)
        entry_files.insert(0, ', '.join(file_paths))
        update_button_state()

def select_folder():
    folder_path = filedialog.askdirectory()  # フォルダを選択
    if folder_path:
        entry_folder.delete(0, tk.END)
        entry_folder.insert(0, folder_path)
        update_button_state()



def rename_files():
    folder_path = entry_folder.get()
    files = entry_files.get().split(', ')

    if not folder_path and not files:
        messagebox.showerror("エラー", "ファイルまたはフォルダが選択されていません")
        return

    changes = []

    # フォルダが選択されている場合
    if folder_path:
        for root_dir, dirs, file_list in os.walk(folder_path):
            for file in file_list:
                name, ext = extract_info_from_filename(file)
                if name and ext:
                    new_name = f"{name}{ext}"
                    old_path = os.path.join(root_dir, file)
                    new_path = os.path.join(root_dir, new_name)
                    if old_path != new_path:  # 重複リネームを防ぐため、ファイル名が異なる場合のみ実行
                        changes.append((old_path, new_path))

    # 個別にファイルが選択されている場合
    for file_path in files:
        if file_path:
            file_name = os.path.basename(file_path)
            name, ext = extract_info_from_filename(file_name)
            if name and ext:
                new_name = f"{name}{ext}"
                old_path = file_path
                new_path = os.path.join(os.path.dirname(file_path), new_name)
                if old_path != new_path:  # 重複リネームを防ぐため、ファイル名が異なる場合のみ実行
                    changes.append((old_path, new_path))

    if changes:
        show_confirmation_dialog(changes)
    else:
        messagebox.showinfo("情報", "リネームするファイルがありません。")




def show_confirmation_dialog(changes):
    # 変更内容を表示する新しいウィンドウを作成
    confirmation_window = tk.Toplevel(root)
    confirmation_window.title("変更内容の確認")

    ttk.Label(confirmation_window, text="以下の変更を実行しますか？").grid(row=0, column=0, columnspan=2, padx=5, pady=5)

    ttk.Label(confirmation_window, text="変更前のファイル名").grid(row=1, column=0, padx=5, pady=5)
    ttk.Label(confirmation_window, text="変更後のファイル名").grid(row=1, column=1, padx=5, pady=5)

    for i, (old_name, new_name) in enumerate(changes):
        # フルパスからファイル名のみを抽出
        old_filename = os.path.basename(old_name)
        new_filename = os.path.basename(new_name)
        ttk.Label(confirmation_window, text=old_filename).grid(row=i+2, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(confirmation_window, text=new_filename).grid(row=i+2, column=1, padx=5, pady=5, sticky="w")

    # 実行とキャンセルのボタンを入れ替える
    ttk.Button(confirmation_window, text="キャンセル", command=lambda: reset_fields(confirmation_window)).grid(row=len(changes)+2, column=0, padx=5, pady=5)
    ttk.Button(confirmation_window, text="実行", command=lambda: execute_changes(changes, confirmation_window)).grid(row=len(changes)+2, column=1, padx=5, pady=5)

def reset_fields(confirmation_window):
    # 入力フィールドをリセットし、確認ウィンドウを閉じる
    entry_files.delete(0, tk.END)
    entry_folder.delete(0, tk.END)
    update_button_state()  # ボタンの状態をリセット
    confirmation_window.destroy()

def execute_changes(changes, confirmation_window):
    # 変更を実行
    for old_name, new_name in changes:
        old_path = os.path.join(entry_folder.get(), old_name)
        new_path = os.path.join(entry_folder.get(), new_name)
        try:
            os.rename(old_path, new_path)
        except Exception as e:
            messagebox.showerror("エラー", f"ファイル {old_name} のリネーム中にエラーが発生しました: {e}")
            return

    confirmation_window.destroy()
    reset_fields(confirmation_window)  # 入力フィールドをリセット
    messagebox.showinfo("完了", "ファイルを配布データ化したよ！どういたしまして^^")


# GUIのセットアップ
root = tk.Tk()
root.title("配布データ化")

style = ttk.Style()
style.configure('TButton')
style.configure('TLabel')
style.configure('TEntry')
style.configure('TRadiobutton')

root.bind('<Configure>')

frame_select = ttk.Frame(root)
frame_select.grid(row=0, column=0, padx=5, pady=5, sticky="ew", columnspan=3)

ttk.Label(frame_select, text="ファイルを選択").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_files = ttk.Entry(frame_select, width=30)
entry_files.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
ttk.Button(frame_select, text="ファイルを選択", command=select_files).grid(row=0, column=2, padx=5, pady=5, sticky="ew")

ttk.Label(frame_select, text="フォルダを選択").grid(row=0, column=3, padx=5, pady=5, sticky="e")
entry_folder = ttk.Entry(frame_select, width=30)
entry_folder.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
ttk.Button(frame_select, text="フォルダを選択", command=select_folder).grid(row=0, column=5, padx=5, pady=5, sticky="ew")

# ファイル名をリネームするボタン
btn_rename_files = ttk.Button(root, text="配布データ化", command=rename_files, state=tk.DISABLED)
btn_rename_files.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")

root.mainloop()




