import os
from pathlib import Path

BASE_DIR = Path(r"D:\Python\Projetos\PorGPT")

FILES = {
    "app/main.py": """from fastapi import FastAPI

app = FastAPI(
    title="PorGPT - Emissor de NF-e",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"status": "Emissor NF-e ativo"}
""",

    "app/config.py": """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://usuario:senha@localhost:5432/porgpt"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
""",

    "app/models/base.py": """from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
""",

    "app/models/empresa.py": """from sqlalchemy import Column, Integer, String, Boolean
from app.models.base import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    razao_social = Column(String(150), nullable=False)
    nome_fantasia = Column(String(150))
    cnpj = Column(String(14), unique=True, nullable=False)
    ie = Column(String(20))
    im = Column(String(20))
    uf = Column(String(2), nullable=False)
    municipio = Column(String(100), nullable=False)
    regime_tributario = Column(String(20), nullable=False)
    ambiente = Column(String(20), default="HOMOLOGACAO")
    ativo = Column(Boolean, default=True)
""",

    "app/models/certificado.py": """from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class Certificado(Base):
    __tablename__ = "certificados"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    arquivo_pfx = Column(LargeBinary, nullable=False)
    senha = Column(String(255), nullable=False)
    valido_ate = Column(DateTime, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    empresa = relationship("Empresa")
""",

    "app/models/nfe.py": """from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class NFe(Base):
    __tablename__ = "nfe"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    chave = Column(String(44), unique=True)
    numero = Column(Integer, nullable=False)
    serie = Column(Integer, nullable=False)
    status = Column(String(50), default="CRIADA")
    protocolo = Column(String(50))
    ambiente = Column(String(20))
    xml = Column(Text)
    xml_autorizado = Column(Text)
    criado_em = Column(DateTime, default=datetime.utcnow)
    autorizado_em = Column(DateTime)

    empresa = relationship("Empresa")
""",

    "app/models/__init__.py": """from app.models.empresa import Empresa
from app.models.certificado import Certificado
from app.models.nfe import NFe
""",

    "app/fiscal/xml_builder.py": """from lxml import etree

NS = "http://www.portalfiscal.inf.br/nfe"

def gerar_xml_nfe(dados):
    nfe = etree.Element("NFe", nsmap={None: NS})
    inf = etree.SubElement(nfe, "infNFe", Id=dados["id"], versao="4.00")

    ide = etree.SubElement(inf, "ide")
    etree.SubElement(ide, "cUF").text = dados["cUF"]
    etree.SubElement(ide, "natOp").text = dados["natOp"]
    etree.SubElement(ide, "mod").text = "55"

    return etree.tostring(
        nfe,
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8"
    )
""",

    "requirements.txt": """fastapi==0.95.2
uvicorn==0.22.0
sqlalchemy==1.4.49
psycopg2-binary==2.9.9
python-dotenv==1.0.0
lxml==4.9.3
signxml==3.2.1
cryptography==41.0.3
requests==2.31.0
pydantic==1.10.13
""",

    "README.md": """# PorGPT - Emissor de NF-e

Projeto emissor de NF-e em Python 3.8
Uso comercial | SaaS | Multiempresa | Multi-regime
"""
}

DIRS = [
    "app/api",
    "app/fiscal/regimes",
    "app/models",
    "app/schemas",
    "app/workers",
    "tests"
]

def create_project():
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    for d in DIRS:
        (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

    for file, content in FILES.items():
        path = BASE_DIR / file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    print("✅ Projeto PorGPT criado com sucesso!")

if __name__ == "__main__":
    create_project()
