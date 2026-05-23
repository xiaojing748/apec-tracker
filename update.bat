@echo off
chcp 65001 >nul
cd /d "C:\Users\Lenovo\apec-tracker"

echo.
echo   ========================================
echo     APEC 2026 网络安全动态追踪
echo   ========================================
echo.
echo   [1/2] 从 GitHub 拉取最新数据...

"C:\Program Files\Git\bin\git.exe" pull origin master 2>nul
if errorlevel 1 (
    echo         网络不通，使用本地已有数据
) else (
    echo         数据已更新
)

echo   [2/2] 生成看板页面...
"C:\Users\Lenovo\AppData\Local\Programs\Python\Python312\python.exe" build_html.py 2>nul
if errorlevel 1 (
    echo         生成失败，请检查环境
    pause
    exit /b 1
)
echo         完成

echo.
echo   正在浏览器中打开看板...
start "" "C:\Users\Lenovo\apec-tracker\APEC动态看板.html"

exit
