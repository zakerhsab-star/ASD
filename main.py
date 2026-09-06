#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrcpy Remote Reverse Tunnel Agent (Client)
Runs on the secondary device/phone to tunnel ADB connection directly back to the Laptop.
"""

import socket
import threading
import time

# ضع هنا الـ IP الخاص باللابتوب أو عنوان النفق الخاص بك
LAPTOP_IP = "192.168.1.100"
PORT = 5001  # رقم المنفذ المخصص لهذا الجهاز (مثال: 5001 للجهاز الأول، 5002 للثاني)
LOCAL_ADB = ("127.0.0.1", 5555)

def bridge_sockets(s1, s2):
    try:
        while True:
            data = s1.recv(8192)
            if not data:
                break
            s2.sendall(data)
    except Exception:
        pass
    finally:
        s1.close()
        s2.close()

def run_agent():
    print(f"[*] جاري الاتصال باللابتوب عبر النفق على {LAPTOP_IP}:{PORT}...")
    while True:
        try:
            s_laptop = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_laptop.connect((LAPTOP_IP, PORT))

            s_phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_phone.connect(LOCAL_ADB)

            print("[+] تم إنشاء النفق العكسي بنجاح! اللابتوب يتحكم الآن بجهازك.")

            t1 = threading.Thread(target=bridge_sockets, args=(s_laptop, s_phone), daemon=True)
            t2 = threading.Thread(target=bridge_sockets, args=(s_phone, s_laptop), daemon=True)
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        except Exception:
            print("[-] انقطع الاتصال أو تعذر الوصول للابتوب، جاري إعادة المحاولة خلال 5 ثوانٍ...")
            time.sleep(5)

if __name__ == "__main__":
    run_agent()
