from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
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
