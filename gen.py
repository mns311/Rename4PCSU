import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def get_user_input():
    year = entry_year.get()
    course_type = selected_course_type.get()
    if course_type == "その他":
        course_type = entry_other_course_type.get()
    course_name = entry_course_number.get()
    category = selected_category.get()
    if category == "その他":
        category = entry_other_category.get()
    version = entry_version.get()
    return year, f'{course_type}{course_name}', category, version

def convert_number_to_suffix(event):
    try:
        num = int(entry_course_number.get())
        
        # 11, 12, 13は例外的に "th"
        if 10 <= num % 100 <= 13:
            suffix = f'{num}th'
        else:
            # 1の位に応じて suffix を変える
            last_digit = num % 10
            if last_digit == 1:
                suffix = f'{num}st'
            elif last_digit == 2:
                suffix = f'{num}nd'
            elif last_digit == 3:
                suffix = f'{num}rd'
            else:
                suffix = f'{num}th'
        
        # エントリーをクリアして結果を挿入
        entry_course_number.delete(0, tk.END)
        entry_course_number.insert(0, suffix)
        
    except ValueError:
        pass

def sanitize_filename(filename):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename

def generate_new_filename(year, course_name, category, version, old_filename):
    name, ext = os.path.splitext(old_filename)
    if category == "PP":
        new_name = f'{year}-{course_name}{category}{version}{ext}'
    else:
        new_name = f'{year}-{course_name}{category}（{name}）{version}{ext}'
    return sanitize_filename(new_name)

def show_file_list_window(filepaths):
    file_list_window = tk.Toplevel(root)
    file_list_window.title("ファイルリスト")

    ttk.Label(file_list_window, text="変更前").grid(row=0, column=0, padx=10, pady=5, sticky="ew")
    ttk.Label(file_list_window, text="変更後").grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    old_new_filenames = []

    for i, filepath in enumerate(filepaths):
        old_filename = os.path.basename(filepath)
        old_new_filenames.append((old_filename, None))
        
        year, course_name, category, version = get_user_input()
        new_filename = generate_new_filename(year, course_name, category, version, old_filename)
        old_new_filenames[i] = (old_filename, new_filename)
        
        ttk.Label(file_list_window, text=old_filename).grid(row=i+1, column=0, padx=10, pady=5, sticky="ew")
        ttk.Label(file_list_window, text=new_filename).grid(row=i+1, column=1, padx=10, pady=5, sticky="ew")

    def apply_changes():
        for old_filename, new_filename in old_new_filenames:
            try:
                dir_path = os.path.dirname(filepaths[0])
                old_filepath = os.path.join(dir_path, old_filename)
                new_filepath = os.path.join(dir_path, new_filename)
                os.rename(old_filepath, new_filepath)
            except Exception as e:
                messagebox.showerror("エラー", f"ファイル名の変更に失敗しました: {e}")
                return
        
        messagebox.showinfo("成功", "ファイル名を生成したよ！どういたしまして^^")
        file_list_window.destroy()

    def cancel_changes():
        file_list_window.destroy()
        rename_files()

    # Cancel and Apply buttons
    ttk.Button(file_list_window, text="キャンセル", command=cancel_changes).grid(row=len(filepaths)+1, column=0, pady=10, sticky="ew")
    ttk.Button(file_list_window, text="変更", command=apply_changes).grid(row=len(filepaths)+1, column=1, pady=10, sticky="ew")

def rename_files():
    filepaths = filedialog.askopenfilenames()
    if not filepaths:
        return
    
    year, course_name, category, version = get_user_input()
    if not all([year, course_name, category, version]):
        messagebox.showerror("入力エラー", "すべてのフィールドに入力してください")
        return

    show_file_list_window(filepaths)

def toggle_other_category_entry():
    if selected_category.get() == "その他":
        entry_other_category.grid(row=3, column=3, padx=5, pady=5, sticky="ew")
    else:
        entry_other_category.grid_remove()

def toggle_other_course_type_entry():
    if selected_course_type.get() == "その他":
        entry_other_course_type.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    else:
        entry_other_course_type.grid_remove()

def update_version():
    selected_version = selected_version_type.get()
    version_dict = {
        "1. アウトライン": "v1.0.0",
        "2. モギモギ": "v2.0.0",
        "3. 模擬": "v3.0.0",
        "4. 納入": "v4.0.0",
        "5. 最終確認": "v5.0.0",
        "6. 講座用データ": "v6.0.0",
        "7. 振り返り": "v7.0.0",
        "8. その他": "v.."
    }
    entry_version.delete(0, tk.END)
    entry_version.insert(0, version_dict[selected_version])


# GUIのセットアップ
root = tk.Tk()
root.title("ファイル名生成")


# Setting style for ttk widgets
style = ttk.Style()
style.configure('TButton')
style.configure('TLabel')
style.configure('TRadiobutton')
style.configure('TEntry')

root.bind('<Configure>')

# Labels and Entries
ttk.Label(root, text="年度").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_year = ttk.Entry(root)
entry_year.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

ttk.Label(root, text="講座名").grid(row=1, column=0, padx=5, pady=5, sticky="e")

frame_course = ttk.Frame(root)
frame_course.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
frame_course.grid_propagate(False)

selected_course_type = tk.StringVar(value="Std")

ttk.Radiobutton(frame_course, text="Std", variable=selected_course_type, value="Std", command=toggle_other_course_type_entry).pack(side=tk.LEFT)
ttk.Radiobutton(frame_course, text="Adv", variable=selected_course_type, value="Adv", command=toggle_other_course_type_entry).pack(side=tk.LEFT)
ttk.Radiobutton(frame_course, text="その他", variable=selected_course_type, value="その他", command=toggle_other_course_type_entry).pack(side=tk.LEFT)
entry_other_course_type = ttk.Entry(root, width=10)
entry_other_course_type.grid(row=1, column=2, padx=5, pady=5, sticky="w")
entry_other_course_type.grid_remove()

ttk.Label(root, text="第").grid(row=2, column=0, padx=5, pady=5, sticky="e")
ttk.Label(root, text="講").grid(row=2, column=2, padx=0, pady=0, sticky="w")
entry_course_number = ttk.Entry(root)
entry_course_number.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
entry_course_number.bind("<FocusOut>", convert_number_to_suffix)

ttk.Label(root, text="種類").grid(row=3, column=0, padx=5, pady=5, sticky="e")

frame_category = ttk.Frame(root)
frame_category.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
frame_category.grid_propagate(False)

selected_category = tk.StringVar(value="PP")

ttk.Radiobutton(frame_category, text="PP", variable=selected_category, value="PP", command=toggle_other_category_entry).pack(side=tk.LEFT)
ttk.Radiobutton(frame_category, text="ExD", variable=selected_category, value="ExD", command=toggle_other_category_entry).pack(side=tk.LEFT)
ttk.Radiobutton(frame_category, text="InD", variable=selected_category, value="InD", command=toggle_other_category_entry).pack(side=tk.LEFT)
ttk.Radiobutton(frame_category, text="その他", variable=selected_category, value="その他", command=toggle_other_category_entry).pack(side=tk.LEFT)

entry_other_category = ttk.Entry(root, width=10)
entry_other_category.grid(row=3, column=3, padx=5, pady=5, sticky="ew")
entry_other_category.grid_remove()

ttk.Label(root, text="バージョンタイプ").grid(row=4, column=0, padx=5, pady=5, sticky="e")

frame_version = ttk.Frame(root)
frame_version.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

version_options = [
    "1. アウトライン", "2. モギモギ", "3. 模擬",
    "4. 納入", "5. 最終確認", "6. 講座用データ", "7. 振り返り", "8. その他"
]

selected_version_type = tk.StringVar(value="")
for i, version in enumerate(version_options):
    ttk.Radiobutton(frame_version, text=version, variable=selected_version_type, value=version, command=update_version).grid(row=i // 4, column=i % 4, padx=5, pady=5, sticky="ew")

ttk.Label(root, text="バージョン").grid(row=5, column=0, padx=5, pady=5, sticky="e")
entry_version = ttk.Entry(root)
entry_version.insert(0, "v0.0.0")
entry_version.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

ttk.Button(root, text="ファイル名生成", command=rename_files).grid(row=6, column=0, columnspan=3, pady=10, sticky="ew")

root.mainloop()

