# -*- coding: utf-8 -*-
"""豆包炫酷启动器：全屏 WebView2 播放启动动画，动画结束自动拉起豆包。
使用 pywebview（Edge WebView2 Runtime），无浏览器界面，全屏沉浸。"""
import os
import sys
import threading
import traceback

import webview

# 动态计算路径，解压到哪都能跑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANIM_HTML = os.path.join(BASE_DIR, 'preview', 'index.html')
ANIM_URL = 'file:///' + ANIM_HTML.replace('\\', '/')

# 豆包安装路径（如果不在默认位置，请改成你自己的路径）
DOUBAO_PATHS = [
    os.path.expandvars(r'%LOCALAPPDATA%\Doubao\Application\Doubao.exe'),
    os.path.join(os.environ.get('USERPROFILE', ''), r'AppData\Local\Doubao\Application\Doubao.exe'),
]

LOG_FILE = os.path.join(BASE_DIR, 'launcher.log')


def log(msg):
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')
    except Exception:
        pass


def find_doubao():
    """在常见路径里找豆包可执行文件。"""
    for p in DOUBAO_PATHS:
        if os.path.exists(p):
            return p
    return None


window = None
launched = False


def launch_doubao():
    """动画窗口关闭后拉起豆包（只执行一次）。"""
    global launched
    if launched:
        return
    launched = True
    try:
        exe = find_doubao()
        if exe:
            os.startfile(exe)
    except Exception:
        pass


class Api:
    """动画页通过 window.pywebview.api.finished() 通知动画已播完。"""

    def log(self, msg):
        log(str(msg))

    def finished(self):
        try:
            if window is not None:
                window.destroy()
        except Exception:
            pass


def boot():
    global window
    window = webview.create_window(
        '豆包炫酷启动',
        ANIM_URL,
        fullscreen=True,
        js_api=Api(),
        background_color='#000000',
        min_size=(800, 600),
    )
    window.events.closed += launch_doubao


def main():
    log('=== launcher start ===')
    # 兜底：即使窗口异常被关/无法创建，也保证豆包能开（延迟 180 秒保险）。
    t = threading.Timer(180.0, launch_doubao)
    t.daemon = True
    t.start()
    try:
        boot()
        webview.start(debug=False)
        log('=== webview start returned ===')
    except Exception:
        log('ERROR: ' + traceback.format_exc())
        launch_doubao()


if __name__ == '__main__':
    main()
