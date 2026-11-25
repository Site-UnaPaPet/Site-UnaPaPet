"Rotas /posts (publica) e /admin/posts"
from fastapi import APIRouter, Depends, HTTPException, status
from src.backend.database.operations.manage import ManageOperations
from src.backend.depends import auth_depends, get_ops
from src.backend.schema.posts import PostCreate, PostUpdate, PostResponse


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=list[PostResponse])
async def list_posts(ops: ManageOperations = Depends(get_ops)):

    return await ops.list_posts()


@router.get("/{id}", response_model=PostResponse)
async def get_post(id: int, ops: ManageOperations = Depends(get_ops)):

    post = await ops.get_post(id)

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return post


admin_router = APIRouter(
    prefix="/admin/posts",
    tags=["admin posts"],
    dependencies=[Depends(auth_depends.require_admin)],
)


@admin_router.get("", response_model=list[PostResponse])
async def admin_list_posts(ops: ManageOperations = Depends(get_ops)):

    return await ops.list_posts()


@admin_router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_post(body: PostCreate, ops: ManageOperations = Depends(get_ops)):

    return await ops.create_post(**body.model_dump())


@admin_router.get("/{id}", response_model=PostResponse)
async def admin_get_post(id: int, ops: ManageOperations = Depends(get_ops)):

    item = await ops.get_post(id)

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return item


@admin_router.put("/{id}", response_model=PostResponse)
async def admin_update_post(id: int, body: PostUpdate, ops: ManageOperations = Depends(get_ops)):

    item = await ops.update_post(id, **body.model_dump(exclude_unset=True))

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return item


@admin_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_post(id: int, ops: ManageOperations = Depends(get_ops)):

    if not await ops.delete_post(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
