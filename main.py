#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

Window.clearcolor = (0.09, 0.10, 0.15, 1)

class ScrcpyAgentApp(App):
    def build(self):
        self.running = False
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(text="⚡ Scrcpy Agent", font_size='22sp', bold=True, color=(0.54, 0.68, 0.96, 1)))
        
        layout.add_widget(Label(text="عنوان اللابتوب (IP):", size_hint=(1, 0.2)))
        self.ip_input = TextInput(text="192.168.1.100", multiline=False, size_hint=(1, 0.3))
        layout.add_widget(self.ip_input)
        
        self.status_lbl = Label(text="الحالة: متوقف ⏹", size_hint=(1, 0.2))
        layout.add_widget(self.status_lbl)
        
        self.btn = Button(text="بدء النفق في الخلفية ▶", background_color=(0.4, 0.8, 0.4, 1), size_hint=(1, 0.3))
        self.btn.bind(on_press=self.toggle)
        layout.add_widget(self.btn)
        
        return layout

    def toggle(self, instance):
        if not self.running:
            self.running = True
            self.btn.text = "إيقاف ⏹"
            self.btn.background_color = (0.9, 0.4, 0.4, 1)
            self.status_lbl.text = "متصل ويعمل في الخلفية ✔"
            threading.Thread(target=self.run_bridge, daemon=True).start()
        else:
            self.running = False
            self.btn.text = "بدء النفق في الخلفية ▶"
            self.btn.background_color = (0.4, 0.8, 0.4, 1)
            self.status_lbl.text = "الحالة: متوقف ⏹"

    def run_bridge(self):
        host = self.ip_input.text.strip()
        while self.running:
            try:
                s_laptop = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s_laptop.connect((host, 5001))
                s_phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s_phone.connect(("127.0.0.1", 5555))
                
                t1 = threading.Thread(target=self.pipe, args=(s_laptop, s_phone), daemon=True)
                t2 = threading.Thread(target=self.pipe, args=(s_phone, s_laptop), daemon=True)
                t1.start()
                t2.start()
                t1.join()
                t2.join()
            except Exception:
                time.sleep(5)

    def pipe(self, src, dst):
        try:
            while self.running:
                data = src.recv(8192)
                if not data: break
                dst.sendall(data)
        except Exception:
            pass
        finally:
            src.close()
            dst.close()

if __name__ == "__main__":
    ScrcpyAgentApp().run()
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
