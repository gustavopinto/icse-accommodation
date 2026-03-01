"""
Armazenamento dos pedidos de acomodação em um único arquivo JSON (oculto).
Fonte única da verdade — sem banco de dados para acomodações.
"""
import json
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path


# Arquivo oculto (nome começa com .) dentro de instance/
STORAGE_FILENAME = ".accommodation_data.json"


def _storage_path(app):
    """Caminho do arquivo de dados (oculto)."""
    path = Path(app.instance_path) / STORAGE_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


@dataclass
class AccommodationRecord:
    """Registro de um pedido para uso no template (com .strftime nas datas)."""
    name: str
    email: str
    institution: str
    check_in: date
    check_out: date
    gender: str
    roommate_gender_pref: str
    smoker: bool
    accepts_smoker: bool
    notes: str | None
    social_media: str | None
    website: str | None
    created_at: str


def _dict_to_record(d: dict) -> AccommodationRecord:
    """Converte um dict (do JSON) em AccommodationRecord."""
    return AccommodationRecord(
        name=d["name"],
        email=d["email"],
        institution=d["institution"],
        check_in=date.fromisoformat(d["check_in"]) if isinstance(d["check_in"], str) else d["check_in"],
        check_out=date.fromisoformat(d["check_out"]) if isinstance(d["check_out"], str) else d["check_out"],
        gender=d["gender"],
        roommate_gender_pref=d["roommate_gender_pref"],
        smoker=d.get("smoker", False),
        accepts_smoker=d.get("accepts_smoker", False),
        notes=d.get("notes"),
        social_media=d.get("social_media"),
        website=d.get("website"),
        created_at=d.get("created_at", ""),
    )


def load_all(app) -> list[AccommodationRecord]:
    """Carrega todos os pedidos do arquivo (mais recentes primeiro)."""
    path = _storage_path(app)
    if not path.exists():
        return []
    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
    records = [_dict_to_record(d) for d in raw]
    records.sort(key=lambda r: r.created_at, reverse=True)
    return records


def save_new(
    app,
    *,
    name: str,
    email: str,
    institution: str,
    check_in: date,
    check_out: date,
    gender: str,
    roommate_gender_pref: str,
    smoker: bool = False,
    social_media: str | None = None,
    website: str | None = None,
    notes: str | None = None,
) -> None:
    """Adiciona um novo pedido ao arquivo (única gravação)."""
    path = _storage_path(app)
    now = datetime.now(timezone.utc).isoformat()
    data = {
        "name": name,
        "email": email,
        "institution": institution,
        "check_in": check_in.isoformat(),
        "check_out": check_out.isoformat(),
        "gender": gender,
        "roommate_gender_pref": roommate_gender_pref,
        "smoker": smoker,
        "accepts_smoker": False,
        "notes": notes,
        "social_media": social_media,
        "website": website,
        "created_at": now,
    }

    existing = []
    if path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, OSError):
            existing = []

    existing.append(data)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
