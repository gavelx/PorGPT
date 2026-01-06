from app.fiscal.regimes.simples import impostos_simples
from app.fiscal.regimes.normal import impostos_normal

REGIMES = {
    "SIMPLES": impostos_simples,
    "NORMAL": impostos_normal
}

