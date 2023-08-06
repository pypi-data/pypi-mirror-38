#XYLLibrary


    @echo off
    echo "确定要上传最新的包到pypi么?"
    pause
    D:
    cd D:\work\OlymLibrary
    python setup.py sdist
    echo "sdist 完成"
    pause
    twine register dist/*
    echo "上传 完成"
    pause
