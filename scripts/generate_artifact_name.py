#!/usr/bin/env python3
"""
generate_artifact_name.py
Generador canónico de nombres de artefactos con timestamp UTC y anti-colisión.

Uso:
  python3 generate_artifact_name.py html reporte_ventas
  python3 generate_artifact_name.py html reporte_ventas --output-dir ./outputs
  python3 generate_artifact_name.py html reporte_ventas --dry-run

Formato de salida: {slug}.{YYYYMMDDTHHMMSS}.{ext}
Ejemplo:          reporte-ventas.20260716T220606.html
"""
import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Tipos de artefacto soportados
VALID_TYPES = {"html", "json", "csv", "pdf", "txt", "md", "png", "jpg", "svg"}


def sanitize_base_name(name: str) -> str:
    """
    Convierte cualquier string en un slug válido para nombre de archivo.
    Ejemplo: "Reporte Ventas Julio" -> "reporte-ventas-julio"
    """
    slug = name.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)      # Eliminar caracteres especiales
    slug = re.sub(r"[\s_]+", "-", slug)       # Espacios y guiones bajos -> guion
    slug = re.sub(r"-+", "-", slug).strip("-")  # Guiones múltiples -> uno
    if not slug:
        raise ValueError(f"El nombre base no puede sanitizarse: {name!r}")
    return slug


def get_safe_timestamp() -> str:
    """
    Retorna timestamp UTC en formato ISO 8601 compacto: YYYYMMDDTHHMMSS.
    Usar UTC garantiza unicidad entre zonas horarias.
    """
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")


def generate_unique_name(base_name: str, artifact_type: str, output_dir: Path) -> tuple:
    """
    Genera un nombre de archivo único con timestamp.
    Si ya existe un archivo con ese nombre (colisión de segundo),
    agrega sufijo _v2, _v3, etc.

    Retorna: (nombre_del_archivo, path_completo)
    """
    slug = sanitize_base_name(base_name)
    timestamp = get_safe_timestamp()
    ext = f".{artifact_type.lstrip('.')}"
    candidate = f"{slug}.{timestamp}{ext}"
    path = output_dir / candidate
    version = 2
    while path.exists():
        candidate = f"{slug}.{timestamp}_v{version}{ext}"
        path = output_dir / candidate
        version += 1
    return candidate, path


def generate_meta_tags(base_name: str, artifact_name: str) -> str:
    """
    Genera los meta tags HTML anti-caché y de versión para incluir en el <head>.
    """
    now_utc = datetime.now(timezone.utc)
    created_iso = now_utc.isoformat()
    created_legible = now_utc.strftime("%d/%m/%Y %H:%M:%S UTC")
    return f"""  <!-- Anti-caché: fuerza al browser a no cachear este archivo -->
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <!-- Metadatos de versión del artefacto -->
  <meta name="generator" content="context-engineering-agents-playbook/1.0">
  <meta name="artifact-id" content="{artifact_name}">
  <meta name="created" content="{created_iso}">
  <!-- Título con fecha visible para identificar la versión -->
  <!-- Usar en <title>: {base_name} — {created_legible} -->"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "tipo",
        help=f"Tipo de artefacto. Opciones: {', '.join(sorted(VALID_TYPES))}"
    )
    parser.add_argument(
        "nombre_base",
        help="Nombre base del artefacto (se sanitiza automáticamente)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./outputs"),
        help="Directorio de salida (default: ./outputs)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostrar el nombre que se generaría sin crear el archivo"
    )
    parser.add_argument(
        "--meta-tags",
        action="store_true",
        help="Imprimir los meta tags HTML anti-caché para incluir en el <head>"
    )
    args = parser.parse_args()

    artifact_type = args.tipo.lower().strip().lstrip(".")
    if artifact_type not in VALID_TYPES:
        print(
            f"ERROR: tipo no soportado: {args.tipo!r}\n"
            f"Tipos válidos: {', '.join(sorted(VALID_TYPES))}",
            file=sys.stderr
        )
        return 1

    output_dir = args.output_dir.resolve()
    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    try:
        name, path = generate_unique_name(args.nombre_base, artifact_type, output_dir)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"[DRY-RUN] Nombre que se generaría: {name}")
        print(f"[DRY-RUN] Path completo: {path}")
    else:
        path.touch()
        print(f"✅ Artefacto creado: {path}")
        print(f"📎 Nombre: {name}")
        print(f"⚠️  Recordar: abrir ESTE archivo ({name}), no recargar versiones anteriores.")

    if args.meta_tags:
        print("\n--- META TAGS PARA EL <HEAD> ---")
        print(generate_meta_tags(args.nombre_base, name))
        print("--- FIN META TAGS ---")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
