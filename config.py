# -*- coding: utf-8 -*-
"""
Configuration and constants for CS2 Skin Arbitrage Application
"""

# API and Web Scraping Settings
REQUESTS_TIMEOUT = 30
REQUESTS_RETRY_COUNT = 3
REQUESTS_RETRY_DELAY = 2
REQUEST_DELAY_MIN = 1
REQUEST_DELAY_MAX = 3

# Third-party sites and commission rates (%)
SITE_COMMISSIONS = {
    "skinport": 12,
    "csfloat": 2,
    "skinbaron": 15,
    "dmarket": 5,
    "buff163": 5,
    "steam": 15,
}

# Steam Market settings
STEAM_COMMISSION_RATE = 15
MIN_DAILY_VOLUME = 10

# Price ranges
MIN_PRICE = 0.01
MAX_PRICE = 10000.00

# Reliability (Star) range
MIN_RATING = 1.0
MAX_RATING = 5.0

# Product types
PRODUCT_TYPES = [
    "Case",
    "Capsule",
    "Knife",
    "Gloves",
    "Rifle",
    "Pistol",
    "Other"
]

# API Endpoints
API_ENDPOINTS = {
    "skinport": "https://api.skinport.com/v1/items",
    "csfloat": "https://api.csfloat.com/v1/me/inventory",
    "dmarket": "https://api.dmarket.com/v1/marketplace/items",
    "skinbaron": "https://api.skinbaron.de/api/v2/Marketplace/GetItems",
    "buff163": "https://buff.163.com/api/market/goods",
}

# User-Agent (For bot protection)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
]

# Data caching duration (seconds)
CACHE_DURATION = 3600  # 1 hour

# Currency
CURRENCY = "USD"

# Language
LANGUAGE = "en"

# Debug mode
DEBUG = False
