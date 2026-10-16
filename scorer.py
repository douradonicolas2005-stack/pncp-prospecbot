from typing import Optional
from config import CONFIG
from utils import normalizar_minusculo

def calcular_score_oportunidade(valor_contrato: Optional[float], capital_social: Optional[float], municipio_sede: Optional[str], possui_socio_admin_pf: bool=False) -> int:
    score=0
    if valor_contrato is not None and valor_contrato>CONFIG.score.valor_alto_threshold: score+=CONFIG.score.pontos_valor_alto
    if capital_social is not None and capital_social>CONFIG.score.capital_social_threshold: score+=CONFIG.score.pontos_capital_alto
    if municipio_sede:
        mun=normalizar_minusculo(municipio_sede)
        for bonus in CONFIG.score.municipios_bonus:
            if normalizar_minusculo(bonus)==mun: score+=CONFIG.score.pontos_municipio_bonus; break
    if possui_socio_admin_pf: score+=CONFIG.score.pontos_socio_admin_pf
    sf=score+CONFIG.score.score_min
    if sf>CONFIG.score.score_max: sf=CONFIG.score.score_max
    if sf<CONFIG.score.score_min: sf=CONFIG.score.score_min
    return int(sf)
