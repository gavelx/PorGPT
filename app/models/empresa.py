from sqlalchemy import Column, Integer, String, Boolean
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
