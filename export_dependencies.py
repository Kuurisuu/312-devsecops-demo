import sys
import sysconfig
import tarfile
from pathlib import Path

packages = Path(sysconfig.get_path("purelib"))
metadata_files = sorted(packages.glob("*.dist-info/METADATA"))

if not metadata_files:
    raise RuntimeError("No se encontraron metadatos de paquetes instalados")

with tarfile.open(fileobj=sys.stdout.buffer, mode="w|") as archive:
    for metadata in metadata_files:
        archive.add(
            metadata,
            arcname=f"{metadata.parent.name}/METADATA"
        )