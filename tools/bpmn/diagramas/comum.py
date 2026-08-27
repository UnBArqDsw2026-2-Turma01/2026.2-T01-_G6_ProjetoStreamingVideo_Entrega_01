"""Atalhos compartilhados pelas especificações dos diagramas."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gerador import (  # noqa: E402
    DataFlow, Diagram, Flow, Lane, MsgFlow, Node, Note, Pool,
)

__all__ = ["DataFlow", "Diagram", "Flow", "Lane", "MsgFlow", "Node", "Note",
           "Pool", "N", "F", "T"]


def N(id_, kind, name="", lane=None, col=0, row=0, **kw) -> Node:
    return Node(id=id_, kind=kind, name=name, lane=lane, col=col, row=row, **kw)


def F(src, dst, name="", **kw) -> Flow:
    return Flow(src=src, dst=dst, name=name, **kw)


def T(id_, text, attach, lane, col, row) -> Note:
    return Note(id=id_, text=text, attach=attach, lane=lane, col=col, row=row)
