from pydantic import BaseModel, Field
from typing import List, Dict, Set

class MunicipioConfig(BaseModel):
    nome: str
    ibge: str
    uf: str = "SP"

MUNICIPIOS_ALVO: List[MunicipioConfig] = [
    MunicipioConfig(nome="Jundiaí", ibge="3525904", uf="SP"),
    MunicipioConfig(nome="Campinas", ibge="3509502", uf="SP"),
    MunicipioConfig(nome="Várzea Paulista", ibge="3556503", uf="SP"),
    MunicipioConfig(nome="Itupeva", ibge="3524006", uf="SP"),
    MunicipioConfig(nome="Cabreúva", ibge="3508405", uf="SP"),
    MunicipioConfig(nome="Louveira", ibge="3527306", uf="SP"),
    MunicipioConfig(nome="Vinhedo", ibge="3556701", uf="SP"),
    MunicipioConfig(nome="Indaiatuba", ibge="3520509", uf="SP"),
]

IBGE_TO_NOME: Dict[str, str] = {m.ibge: m.nome for m in MUNICIPIOS_ALVO}
NOMES_ALVO_NORMALIZADOS: Set[str] = {m.nome.lower().strip() for m in MUNICIPIOS_ALVO}

class PNCPConfig(BaseModel):
    base_url: str = "https://pncp.gov.br/api/consulta/v1/contratos"
    janela_dias: int = 30
    status_validos: List[str] = Field(default_factory=lambda: ["Contratado", "Homologado"])
    page_size: int = 100
    timeout_segundos: int = 60
    delay_entre_reqs_seg: float = 0.5
    max_paginas: int = 500
    valor_minimo: float = 300000.00

class CNPJConfig(BaseModel):
    brasilapi_base: str = "https://brasilapi.com.br/api/cnpj/v1"
    minhareceita_base: str = "https://minhareceita.org/api/cnpj"
    timeout_segundos: int = 30
    delay_entre_reqs_seg: float = 1.0
    max_retries: int = 6
    max_cnpjs_por_exec: int = 0
    max_concorrencia: int = 2

class ScoreConfig(BaseModel):
    valor_alto_threshold: float = 2000000.00
    pontos_valor_alto: int = 2
    capital_social_threshold: float = 500000.00
    pontos_capital_alto: int = 1
    municipios_bonus: List[str] = Field(default_factory=lambda: ["Jundiaí", "Campinas"])
    pontos_municipio_bonus: int = 1
    qualificacoes_socio_admin: List[str] = Field(default_factory=lambda: [
        "socio-administrador","administrador","diretor","socio administrador","sócio-administrador","sócio administrador","diretor(a)","administrador(a)"
    ])
    pontos_socio_admin_pf: int = 1
    score_min: int = 1
    score_max: int = 5

class StorageConfig(BaseModel):
    data_dir: str = "data"
    logs_dir: str = "logs"
    csv_saida: str = "leads_pncp_jundiai.csv"
    sqlite_db: str = "leads_pncp_jundiai.db"
    checkpoint_file: str = "checkpoint.json"
    csv_encoding: str = "utf-8-sig"
    csv_sep: str = ","

class AppConfig(BaseModel):
    pncp: PNCPConfig = Field(default_factory=PNCPConfig)
    cnpj: CNPJConfig = Field(default_factory=CNPJConfig)
    score: ScoreConfig = Field(default_factory=ScoreConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)

CONFIG = AppConfig()
