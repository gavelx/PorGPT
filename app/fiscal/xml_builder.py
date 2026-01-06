from lxml import etree
from app.fiscal.regimes.simples import impostos_simples
from app.fiscal.regimes.normal import impostos_normal


NS = "http://www.portalfiscal.inf.br/nfe"

def gerar_xml_nfe(dados):
    nfe = etree.Element("NFe", nsmap={None: NS})
    inf = etree.SubElement(
        nfe,
        "infNFe",
        Id=dados["id"],
        versao="4.00"
    )

    _ide(inf, dados)
    _emit(inf, dados["emitente"])
    _dest(inf, dados["destinatario"])
    _det(inf, dados)
    _total(inf, dados)
    _pag(inf, dados)

    return etree.tostring(
        nfe,
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8"
    )


def _ide(inf, dados):
    ide = etree.SubElement(inf, "ide")
    etree.SubElement(ide, "cUF").text = dados["cUF"]
    etree.SubElement(ide, "natOp").text = dados["natOp"]
    etree.SubElement(ide, "mod").text = "55"
    etree.SubElement(ide, "serie").text = str(dados["serie"])
    etree.SubElement(ide, "nNF").text = str(dados["numero"])
    etree.SubElement(ide, "tpNF").text = "1"
    etree.SubElement(ide, "idDest").text = "1"
    etree.SubElement(ide, "cMunFG").text = dados["cMunFG"]
    etree.SubElement(ide, "tpImp").text = "1"
    etree.SubElement(ide, "tpEmis").text = "1"
    etree.SubElement(ide, "tpAmb").text = dados["tpAmb"]
    etree.SubElement(ide, "finNFe").text = "1"
    etree.SubElement(ide, "indFinal").text = "1"
    etree.SubElement(ide, "indPres").text = "1"
    etree.SubElement(ide, "procEmi").text = "0"
    etree.SubElement(ide, "verProc").text = "PorGPT 1.0"


def _emit(inf, emit):
    emitente = etree.SubElement(inf, "emit")
    etree.SubElement(emitente, "CNPJ").text = emit["cnpj"]
    etree.SubElement(emitente, "xNome").text = emit["razao_social"]
    etree.SubElement(emitente, "xFant").text = emit["fantasia"]

    ender = etree.SubElement(emitente, "enderEmit")
    etree.SubElement(ender, "xLgr").text = emit["logradouro"]
    etree.SubElement(ender, "nro").text = emit["numero"]
    etree.SubElement(ender, "xMun").text = emit["municipio"]
    etree.SubElement(ender, "UF").text = emit["uf"]
    etree.SubElement(ender, "CEP").text = emit["cep"]
    etree.SubElement(ender, "cMun").text = emit["cMun"]

    etree.SubElement(emitente, "IE").text = emit["ie"]
    etree.SubElement(emitente, "CRT").text = emit["crt"]


def _dest(inf, dest):
    destinatario = etree.SubElement(inf, "dest")
    etree.SubElement(destinatario, "CPF").text = dest["cpf"]
    etree.SubElement(destinatario, "xNome").text = dest["nome"]

    ender = etree.SubElement(destinatario, "enderDest")
    etree.SubElement(ender, "xLgr").text = dest["logradouro"]
    etree.SubElement(ender, "nro").text = dest["numero"]
    etree.SubElement(ender, "xMun").text = dest["municipio"]
    etree.SubElement(ender, "UF").text = dest["uf"]
    etree.SubElement(ender, "CEP").text = dest["cep"]
    etree.SubElement(ender, "cMun").text = dest["cMun"]

    etree.SubElement(destinatario, "indIEDest").text = "9"


def _det(inf, dados):
    total_prod = 0

    for i, item in enumerate(dados["itens"], start=1):
        det = etree.SubElement(inf, "det", nItem=str(i))

        prod = etree.SubElement(det, "prod")
        etree.SubElement(prod, "cProd").text = item["codigo"]
        etree.SubElement(prod, "xProd").text = item["descricao"]
        etree.SubElement(prod, "NCM").text = item["ncm"]
        etree.SubElement(prod, "CFOP").text = item["cfop"]
        etree.SubElement(prod, "uCom").text = "UN"
        etree.SubElement(prod, "qCom").text = "1"
        etree.SubElement(prod, "vUnCom").text = str(item["valor"])
        etree.SubElement(prod, "vProd").text = str(item["valor"])

        total_prod += float(item["valor"])

        imposto = etree.SubElement(det, "imposto")

        if dados["regime"] == "SIMPLES":
            impostos_simples(imposto)
        else:
            impostos_normal(imposto)

    dados["vProd"] = total_prod


def _total(inf, dados):
    total = etree.SubElement(inf, "total")
    icms_tot = etree.SubElement(total, "ICMSTot")

    etree.SubElement(icms_tot, "vBC").text = "0.00"
    etree.SubElement(icms_tot, "vICMS").text = "0.00"
    etree.SubElement(icms_tot, "vProd").text = f"{dados['vProd']:.2f}"
    etree.SubElement(icms_tot, "vNF").text = f"{dados['vProd']:.2f}"


def _pag(inf, dados):
    pag = etree.SubElement(inf, "pag")
    det_pag = etree.SubElement(pag, "detPag")
    etree.SubElement(det_pag, "tPag").text = "01"
    etree.SubElement(det_pag, "vPag").text = f"{dados['vProd']:.2f}"
