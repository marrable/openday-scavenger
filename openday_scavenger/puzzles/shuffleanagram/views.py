from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

from openday_scavenger.api.puzzles.dependencies import get_puzzle_name
from openday_scavenger.api.visitors.dependencies import get_auth_visitor
from openday_scavenger.api.visitors.schemas import VisitorAuth

from .service import get_initial_word, shuffle_word

router = APIRouter()

templates = Jinja2Templates(directory=Path(__file__).resolve().parent / "templates")


@router.get("/static/{path:path}")
async def get_static_files(
    path: Path,
):
    """get_static_files Serve files from a local static folder"""
    # This route is required as the current version of FastAPI doesn't allow
    # the mounting of folders on APIRouter. This is an open issue:
    # https://github.com/fastapi/fastapi/discussions/9070
    parent_path = Path(__file__).resolve().parent / "static"
    file_path = parent_path / path

    # Make sure the requested path is a file and relative to this path
    if file_path.is_relative_to(parent_path) and file_path.is_file():
        return FileResponse(file_path)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Requested file does not exist"
        )


# function that returns a shuffled version of the word
@router.get("/shuffled")
async def get_shuffled_word(
    request: Request,
    initial_word: Annotated[str, Depends(get_initial_word)],
):
    """get_shuffled_word Send a scrambled version of the word to the client"""
    # create a shuffled version of the word
    word = await shuffle_word(initial_word)
    return templates.TemplateResponse(
        request=request,
        name="scrambled_word.html",
        context={
            "scrambled_word": word,
        },
    )


@router.get("/")
async def index(
    request: Request,
    visitor: Annotated[VisitorAuth, Depends(get_auth_visitor)],
    puzzle_name: Annotated[str, Depends(get_puzzle_name)],
    initial_word: Annotated[str, Depends(get_initial_word)],
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "puzzle": puzzle_name,
            "visitor": visitor.uid,
            "scrambled_word": initial_word,
        },
    )
