"""Redazione automatica CurioMondo.

Il pacchetto separa il monitoraggio leggero delle fonti dal lavoro editoriale
costoso: il watcher gira spesso ed è gratuito, il worker editoriale parte solo
quando esiste davvero un candidato nuovo e rilevante.
"""

__all__ = [
    "config",
    "filters",
    "normalize",
    "observability",
    "sources",
    "state",
    "watcher",
]
