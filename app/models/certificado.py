from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, ForeignKey
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
