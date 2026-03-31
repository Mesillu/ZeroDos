#!/bin/bash

clear
echo "======================="
echo "      ZeroDos"
echo "======================="

sleep 1

echo "[*] Updating Termux..."
pkg update -y

echo "[*] Installing Python..."
pkg install python git -y

echo "[*] Upgrading pip..."
pip install --upgrade pip

echo "[*] Installing requirements (if any)..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

echo "[*] Running program..."
python zerodos.py
