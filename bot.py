#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Renkleri başlat
init()

class TikTokBot:
    def __init__(self):
        self.proxy_list = []
        self.working_proxies = []
        self.user_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36"
        ]
        self.success_count = 0
        self.fail_count = 0
        self.lock = threading.Lock()
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
    def show_banner(self):
        banner = f"""
{Fore.CYAN}╔════════════════════════════════════════════╗
║                                                  ║
║           {Fore.YELLOW}TIKTOK OTO BİTME SİSTEMİ{Fore.CYAN}           ║
║                                                  ║
║     {Fore.GREEN}Doğal Proxy ile İzleyici/Takipçi/Beğeni{Fore.CYAN}     ║
║                                                  ║
║           {Fore.MAGENTA}2026 VERSİYON - TERMUX UYUMLU{Fore.CYAN}           ║
║                                                  ║
╚════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
        
    def load_proxies(self):
        try:
            # 2026'da çalışan doğal proxy kaynakları
            proxy_sources = [
                "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
                "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
                "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
            ]
            
            print(f"{Fore.YELLOW}[!] Proxy'ler yükleniyor...{Style.RESET_ALL}")
            
            for source in proxy_sources:
                try:
                    response = requests.get(source, timeout=10)
                    if response.status_code == 200:
                        proxies = response.text.strip().split('\n')
                        for proxy in proxies:
                            if ':' in proxy:
                                self.proxy_list.append(proxy.strip())
                except:
                    continue
                    
            print(f"{Fore.GREEN}[+] {len(self.proxy_list)} proxy başarıyla yüklendi!{Style.RESET_ALL}")
            return len(self.proxy_list) > 0
        except Exception as e:
            print(f"{Fore.RED}[!] Proxy'ler yüklenirken hata: {str(e)}{Style.RESET_ALL}")
            return False
    
    def test_proxy(self, proxy):
        try:
            test_url = "https://httpbin.org/ip"
            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
            response = requests.get(test_url, proxies=proxies, timeout=5)
            if response.status_code == 200:
                return True
        except:
            pass
        return False
    
    def filter_working_proxies(self):
        print(f"{Fore.YELLOW}[!] Çalışan proxy'ler filtreleniyor...{Style.RESET_ALL}")
        
        working_proxies = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            results = list(executor.map(self.test_proxy, self.proxy_list))
            
        for i, is_working in enumerate(results):
            if is_working:
                working_proxies.append(self.proxy_list[i])
                
        self.proxy_list = working_proxies
        print(f"{Fore.GREEN}[+] {len(self.proxy_list)} adet çalışan proxy bulundu!{Style.RESET_ALL}")
        return len(self.proxy_list) > 0
    
    def create_driver(self, proxy=None):
        options = uc.ChromeOptions()
        
        # Mobil görünüm için
        options.add_argument("--window-size=390,844")
        options.add_argument("--user-agent=" + random.choice(self.user_agents))
        
        # Proxy ayarları
        if proxy:
            ip, port = proxy.split(':')
            options.add_argument(f'--proxy-server=http://{ip}:{port}')
        
        # Termux uyumluluğu için
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")
        
        # Headless mod (Termux için gerekli)
        options.add_argument("--headless")
        
        try:
            driver = uc.Chrome(options=options)
            return driver
        except Exception as e:
            print(f"{Fore.RED}[!] Driver oluşturulamadı: {str(e)}{Style.RESET_ALL}")
            return None
    
    def follow_user(self, username, count):
        if not self.proxy_list:
            print(f"{Fore.RED}[!] Çalışan proxy bulunamadı!{Style.RESET_ALL}")
            return False
            
        print(f"{Fore.YELLOW}[!] @{username} kullanıcısına {count} takipçi gönderiliyor...{Style.RESET_ALL}")
        
        def worker_thread():
            if not self.proxy_list:
                return
                
            proxy = random.choice(self.proxy_list)
            driver = self.create_driver(proxy)
            
            if not driver:
                with self.lock:
                    self.fail_count += 1
                return
                
            try:
                driver.get(f"https://www.tiktok.com/@{username}")
                time.sleep(random.uniform(2, 4))
                
                # Takip et butonunu bul ve tıkla
                follow_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Follow')]"))
                )
                follow_button.click()
                
                with self.lock:
                    self.success_count += 1
                    print(f"{Fore.GREEN}[+] Takip edildi! Başarılı: {self.success_count}, Başarısız: {self.fail_count}{Style.RESET_ALL}")
                    
            except Exception as e:
                with self.lock:
                    self.fail_count += 1
                    print(f"{Fore.RED}[!] Takip edilemedi: {str(e)}{Style.RESET_ALL}")
            finally:
                try:
                    driver.quit()
                except:
                    pass
        
        # Çoklu thread ile işlem
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(worker_thread) for _ in range(count)]
            
            for future in futures:
                future.result()
                # Hız sabitleyici - her işlem arası rastgele bekleme
                time.sleep(random.uniform(3, 7))
        
        return True
    
    def like_video(self, video_url, count):
        if not self.proxy_list:
            print(f"{Fore.RED}[!] Çalışan proxy bulunamadı!{Style.RESET_ALL}")
            return False
            
        print(f"{Fore.YELLOW}[!] {count} beğeni gönderiliyor...{Style.RESET_ALL}")
        
        def worker_thread():
            if not self.proxy_list:
                return
                
            proxy = random.choice(self.proxy_list)
            driver
