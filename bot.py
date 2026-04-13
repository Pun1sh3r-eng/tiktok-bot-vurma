#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import random
import time
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

# Renkleri başlat
init()

class TikTokBot:
    def __init__(self):
        self.proxy_list = []
        self.user_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36"
        ]
        self.session = requests.Session()
        self.success_count = 0
        self.fail_count = 0
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
    def show_banner(self):
        banner = f"""
{Fore.CYAN}╔════════════════════════════════════════════╗
║                                                  ║
║           {Fore.YELLOW}TIKTOT OTO BİTME SİSTEMİ{Fore.CYAN}           ║
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
    
    def send_request(self, url, data=None, headers=None):
        proxy = random.choice(self.proxy_list)
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        
        user_agent = random.choice(self.user_agents)
        default_headers = {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        
        if headers:
            default_headers.update(headers)
            
        try:
            if data:
                response = self.session.post(url, data=data, headers=default_headers, proxies=proxies, timeout=10)
            else:
                response = self.session.get(url, headers=default_headers, proxies=proxies, timeout=10)
                
            return response
        except Exception as e:
            return None
    
    def extract_user_id(self, username):
        try:
            url = f"https://www.tiktok.com/@{username}"
            response = self.send_request(url)
            
            if response and response.status_code == 200:
                # Basit bir ID çıkarma yöntemi - 2026'da güncellenmesi gerekebilir
                import re
                pattern = r'"userId":"(\d+)"'
                match = re.search(pattern, response.text)
                if match:
                    return match.group(1)
        except:
            pass
        return None
    
    def send_followers(self, user_id, count):
        url = "https://api.tiktok.com/web/user/follow/"
        headers = {
            "Referer": f"https://www.tiktok.com/",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        data = {
            "user_id": user_id,
            "count": count,
            "type": 1
        }
        
        success = 0
        for i in range(count):
            response = self.send_request(url, data=data, headers=headers)
            if response and response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("status", 0) == 0:
                        success += 1
                        self.success_count += 1
                        print(f"{Fore.GREEN}[+] Takipçi gönderildi: {success}/{count}{Style.RESET_ALL}")
                    else:
                        self.fail_count += 1
                except:
                    self.fail_count += 1
            else:
                self.fail_count += 1
                
            # Hız sabitleyici - her istek arası rastgele bekleme
            time.sleep(random.uniform(1.5, 3.5))
            
        return success
    
    def send_likes(self, video_id, count):
        url = "https://api.tiktok.com/web/like/action/"
        headers = {
            "Referer": f"https://www.tiktok.com/",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        data = {
            "video_id": video_id,
            "type": 1
        }
        
        success = 0
        for i in range(count):
            response = self.send_request(url, data=data, headers=headers)
            if response and response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("status", 0) == 0:
                        success += 1
                        self.success_count += 1
                        print(f"{Fore.GREEN}[+] Beğeni gönderildi: {success}/{count}{Style.RESET_ALL}")
                    else:
                        self.fail_count += 1
                except:
                    self.fail_count += 1
            else:
                self.fail_count += 1
                
            # Hız sabitleyici
            time.sleep(random.uniform(1.0, 2.5))
