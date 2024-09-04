from typing import Annotated
from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse


from sqlalchemy.orm import Session

from openday_scavenger.api.db import get_db
from openday_scavenger.api.visitors.service import create as create_visitor
from openday_scavenger.api.puzzles.service import compare_answer
from openday_scavenger.api.puzzles.schemas import PuzzleCompare

router = APIRouter()

templates = Jinja2Templates(directory=Path(__file__).resolve().parent / "static")


@router.get("/")
async def render_root_page(request: Request):
    """ Render root index page """
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@router.get("/register/{visitor_uid}")
async def register_visitor(visitor_uid: str, db: Annotated["Session", Depends(get_db)]):
    _ = create_visitor(db, visitor_uid)
    return RedirectResponse("/")

@router.post("/submission")
async def submit_answer(puzzle_in: PuzzleCompare, db: Annotated["Session", Depends(get_db)]):

    if compare_answer(db, puzzle_in):
        return {"success": True}
    else:
        return {"success": False}
