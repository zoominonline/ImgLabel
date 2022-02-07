一個協助用戶快速進行圖像分類標示的小工具.

第一次嘗試使用 github, 非典型使用方式.
相關說明暫時放置於 https://www.zoominonline.com/dev
未來補加程式文件, 單元測試後會持續更新.

簡易使用: 於 Python 3.9 
python -m venv c:\venv\ps6 #建立一個被命名為 ps6 的 Python 虛擬環境
c:/venv/ps6/Scripts/Activate.ps1 #啟動剛剛建立的 ps6 環境, 未來需要在此環境執行

#先確認PowerShell 新增行開頭是否有 (ps6) 的字眼, 如果沒有那必須把上述的動作再確認
pip install -U pip #更新 Python 套件安裝指令 pip, 很多套件要求較新的 pip 版本
pip install pyside6 Pillow #安裝 pyside6 以開發 Qt 6 GUI

假設要做標示的所有圖像檔都放置於 C:\YOUR IMAGES 目錄下

python main.py 'C:\YOUR IMAGES'
