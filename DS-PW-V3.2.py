import subprocess
import tkinter as tk
from tkinter import ttk
import pyperclip  # 用于访问剪贴板内容
import webbrowser

# 创建 Tkinter 根窗口
root = tk.Tk()
# 设置窗口标题
root.title("DS Password Assistant")

# 定义样式
root.style = ttk.Style()
root.style.configure('.', font=('微软雅黑', 10))
root.style.configure('TEntry', background='black', foreground='red', font=('微软雅黑', 10, 'bold'))
root.style.map('Accent.TButton', background=[('pressed', '#97d7b6'), ('active', '#a3d7b9')], foreground=[('pressed', '#000000'), ('active', '#000000')])

# 打开网站的函数
def open_website():
    webbrowser.open("https://pvwa.lilly.com/PasswordVault/v10/logon/saml")

# 转义密码中的特殊字符
def escape_special_characters(password):
    special_characters = "#!^+{}%"
    escaped_password = ""
    for char in password:
        if char in special_characters:
            if char == "%":
                escaped_password += "`" + char
            else:
                escaped_password += "{" + char + "}"
        else:
            escaped_password += char
    return escaped_password

# 更新密码按钮的回调函数
def update_password():
    # 从剪贴板获取新密码
    new_password = r"{}".format(new_password_entry.get().strip())
    # 转义密码中的特殊字符
    new_password = escape_special_characters(new_password)
    # 获取脚本文件路径
    script_path = "C:/Users/Public/DS-PW.ahk"
    # 更新脚本中的密码内容
    with open(script_path, 'r') as file:
        content = file.read()
        # 假设密码所在行以 "password = " 开头，并且密码直接位于等号后面
        start_index = content.find("password = ") + len("password = ")
        end_index = content.find("\n", start_index)
        new_content = content[:start_index] + new_password + content[end_index:]
    # 使用写入模式重新打开文件并写入新内容
    with open(script_path, 'w') as file:
        file.write(new_content)
    # 启动 AutoHotkey 脚本
    start_autohotkey_script(script_path)
    status_label.config(text="Password updated successfully and AutoHotkey script restarted.")


# 启动 AutoHotkey 脚本的函数
def start_autohotkey_script(script_path):
    try:
        # 使用 subprocess 模块启动 AutoHotkey 脚本
        subprocess.Popen(['autohotkey', script_path])
    except FileNotFoundError:
        # 如果找不到 AutoHotkey，则更新状态标签文本为错误消息
        status_label.config(text="AutoHotkey is not installed or not in the system path.")

# 创建标签显示 "New Password:"
new_password_label = tk.Label(root, text="Please Enter DS Password:")
new_password_label.pack()

# 创建文本框用于输入新密码
new_password_entry = ttk.Entry(root, width=66)
new_password_entry.pack()

# 创建更新密码按钮并绑定 update_password 函数作为回调
update_button = ttk.Button(root, text="Update Password", command=update_password, style='Accent.TButton')
update_button.pack()

# 创建用于显示状态信息的标签
status_label = tk.Label(root, text="")
status_label.pack()

# 创建打开网站按钮并绑定 open_website 函数作为回调
website_button = ttk.Button(root, text="Get Password", command=open_website, style='Accent.TButton')
website_button.pack()

# 进入 Tkinter 事件循环
root.mainloop()