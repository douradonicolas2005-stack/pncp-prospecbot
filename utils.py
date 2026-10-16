import asyncio
import json
import logging
import os
import re
from datetime import datetime, date, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiofiles
from tenacity import retry, stop_after_attempt, wait_exponential, wait_random, retry_if_exception_type, before_sleep_log
from rich.logging import RichHandler
from config import CONFIG

def setup_logger(name: str = "pncp_bot") -> logging.Logger:
    log_dir = Path(CONFIG.storage.logs_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if logger.handlers:
        logger.handlers.clear()
    rich_handler = RichHandler(rich_tracebacks=True, show_time=True, show_level=True)
    rich_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(rich_handler)
    log_file = log_dir / f"pncp_bot_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    return logger

logger = setup_logger()

def limpar_cnpj(cnpj: Optional[str]) -> Optional[str]:
    if not cnpj: return None
    c = re.sub(r"\D", "", str(cnpj).strip())
    return c if len(c) == 14 else None

def formatar_cnpj(cnpj: Optional[str]) -> Optional[str]:
    c = limpar_cnpj(cnpj)
    if not c: return None
    return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:14]}"

def parse_valor_monetario(valor: Any) -> Optional[float]:
    if valor is None or valor == "": return None
    try:
        if isinstance(valor, (int,float)) and not isinstance(valor,bool): 
            v=float(valor); return round(v,2) if v>=0 else 0
        if isinstance(valor, Decimal): 
            v=float(valor); return round(v,2) if v>=0 else 0
        s=str(valor).strip().replace("R$","").replace(" ","").replace("\u00A0","")
        if "," in s and "." in s: s=s.replace(".","").replace(",",".")
        elif "," in s and "." not in s: s=s.replace(",",".")
        s_clean=re.sub(r"[^0-9\.\-]","",s)
        if s_clean in ("","-","."): return None
        v=float(s_clean); return round(v,2) if v>=0 else 0
    except Exception: return None

def normalizar_texto(texto: Optional[str]) -> Optional[str]:
    if not texto: return None
    t=str(texto).strip(); t=re.sub(r"\s+"," ",t); return t or None

def normalizar_minusculo(texto: Optional[str]) -> Optional[str]:
    if not texto: return None
    return normalizar_texto(str(texto).lower())

def data_hoje(): return date.today()
def calcular_data_inicial(dias:int=CONFIG.pncp.janela_dias): return data_hoje()-timedelta(days=dias)
def calcular_data_final(): return data_hoje()

def criar_diretorios():
    Path(CONFIG.storage.data_dir).mkdir(parents=True, exist_ok=True)
    Path(CONFIG.storage.logs_dir).mkdir(parents=True, exist_ok=True)
