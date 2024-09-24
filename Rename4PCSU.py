import tkinter as tk
from tkinter import ttk
import subprocess
import os

def launch_app(app_name):
    """アプリケーションを起動する関数"""
    exe_dir = os.path.dirname(os.path.abspath(__file__))  # exeのディレクトリを取得
    source_dir = os.path.join(exe_dir, "source")  # sourceフォルダのパスを取得
    
    if app_name == "ファイル名生成":
        subprocess.run(["python", os.path.join(source_dir, "gen.py")])  # gen.pyを実行
    elif app_name == "バージョン更新":
        subprocess.run(["python", os.path.join(source_dir, "upd.py")])  # upd.pyを実行
    elif app_name == "配布データ化":
        subprocess.run(["python", os.path.join(source_dir, "del.py")])  # del.pyを実行
    else:
        print("Invalid app name")

def main():
    """メインアプリケーションのUIを作成"""
    root = tk.Tk()
    root.title("Rename4PCSU")

    # ウィンドウのサイズを設定 (幅 x 高さ)
    root.geometry("400x150")  # ウィンドウのサイズを400x150に設定

    # アプリケーション選択用のUI要素
    ttk.Label(root, text="ボタンを選んでね^^").pack(pady=10)

    button_options = {
        "ファイル名生成": (30, 2),
        "バージョン更新": (30, 2),
        "配布データ化": (30, 2)
    }

    for text, (width, padding) in button_options.items():
        ttk.Button(root, text=text, command=lambda app=text: launch_app(app), width=width).pack(pady=5, padx=5, fill=tk.X, ipadx=padding)

    root.mainloop()

if __name__ == "__main__":
    main()
