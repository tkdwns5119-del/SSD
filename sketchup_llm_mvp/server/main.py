from __future__ import annotations

import re
from typing import Literal, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="SketchUp LLM Bridge MVP")


class ParseRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)


class CreateBoxAction(BaseModel):
    action: Literal["create_box"]
    width_mm: float = Field(..., gt=1, le=100000)
    depth_mm: float = Field(..., gt=1, le=100000)
    height_mm: float = Field(..., gt=1, le=100000)


class MoveSelectionAction(BaseModel):
    action: Literal["move_selection"]
    dx_mm: float = Field(..., ge=-100000, le=100000)
    dy_mm: float = Field(..., ge=-100000, le=100000)
    dz_mm: float = Field(..., ge=-100000, le=100000)


Action = Union[CreateBoxAction, MoveSelectionAction]


class ParseResponse(BaseModel):
    command: Action


def _to_mm(number: float, unit: str) -> float:
    unit = unit.lower()
    if unit in ("mm", "밀리", "밀리미터"):
        return number
    if unit in ("cm", "센티", "센티미터"):
        return number * 10
    if unit in ("m", "미터"):
        return number * 1000
    raise ValueError(f"unsupported unit: {unit}")


def _extract_size(text: str, key: str) -> float | None:
    # 예: 가로 4m / width 4000mm
    patterns = [
        rf"{key}\s*([0-9]+(?:\.[0-9]+)?)\s*(mm|cm|m|밀리미터|센티미터|미터)",
    ]
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            return _to_mm(float(m.group(1)), m.group(2))
    return None


def _extract_move(text: str, axis: str) -> float:
    m = re.search(
        rf"{axis}\s*([+-]?[0-9]+(?:\.[0-9]+)?)\s*(mm|cm|m|밀리미터|센티미터|미터)",
        text,
        flags=re.IGNORECASE,
    )
    if not m:
        return 0.0
    return _to_mm(float(m.group(1)), m.group(2))


@app.post("/parse", response_model=ParseResponse)
def parse_command(req: ParseRequest) -> ParseResponse:
    text = req.text.strip().lower()

    if "박스" in text or "box" in text:
        width = _extract_size(text, "가로|width|w")
        depth = _extract_size(text, "세로|깊이|depth|d")
        height = _extract_size(text, "높이|height|h")

        if width is None or depth is None or height is None:
            raise HTTPException(status_code=400, detail="박스 생성에는 가로/세로/높이가 필요합니다.")

        return ParseResponse(
            command=CreateBoxAction(
                action="create_box",
                width_mm=width,
                depth_mm=depth,
                height_mm=height,
            )
        )

    if "이동" in text or "move" in text:
        dx = _extract_move(text, "x")
        dy = _extract_move(text, "y")
        dz = _extract_move(text, "z")
        return ParseResponse(
            command=MoveSelectionAction(
                action="move_selection",
                dx_mm=dx,
                dy_mm=dy,
                dz_mm=dz,
            )
        )

    raise HTTPException(status_code=400, detail="지원하지 않는 명령입니다. (create_box, move_selection)")
