import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys


def launch_app(app_name):
    """アプリケーションを起動する関数"""
    exe_dir = os.path.dirname(os.path.abspath(__file__))  # exeのディレクトリを取得
    if app_name == "ファイル名生成":
        subprocess.run([os.path.join(exe_dir, "gen.exe")])  # c.exeを実行
    elif app_name == "バージョン更新":
        subprocess.run([os.path.join(exe_dir, "upd.exe")])  # d.exeを実行
    elif app_name == "配布データ化":
        subprocess.run([os.path.join(exe_dir, "del.exe")])  # e.exeを実行
    else:
        print("Invalid app name")


def main():
    """メインアプリケーションのUIを作成"""
    root = tk.Tk()
    root.title("Re：ゼロから始める名前変更_Mk2")

    # ウィンドウのサイズを設定 (幅 x 高さ)
    root.geometry("400x150")  # ウィンドウのサイズを400x150に設定

    # アイコンの設定
    try:
        if getattr(sys, 'frozen', False):  # PyInstallerでバンドルされているかどうかをチェック
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(__file__)

        icon_path = os.path.join(application_path, 'favicon.ico')
        root.iconbitmap(icon_path)  # アイコンファイルを設定
    except Exception as e:
        print(f"アイコンが見つかりません: {e}")

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
