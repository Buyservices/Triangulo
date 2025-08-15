from defusedxml import ElementTree as ET

def parse_string_xml(xml: str) -> tuple[bool, str]:
    """
    Resposta típica: <string xmlns="...">mensagem</string>
    Sucesso heurístico: não conter 'erro'/'falha' em minúsculas.
    """
    try:
        root = ET.fromstring(xml)
        text = (root.text or "").strip()
        if not text:
            return False, "Resposta vazia."
        ok = not any(t in text.lower() for t in ("erro", "error", "falha"))
        return ok, text
    except Exception as e:
        return False, f"Falha ao parsear resposta: {e}"
