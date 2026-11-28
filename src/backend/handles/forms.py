"Rotas /forms (publica) e /admin/forms"
from fastapi import APIRouter, Depends, HTTPException, status
from src.backend.database.operations.manage import ManageOperations
from src.backend.depends import auth_depends, get_ops
from src.backend.schema.forms import FormCreate, FormUpdate, FormResponse


router = APIRouter(prefix="/forms", tags=["forms"])


#só os formulários ativos, já ordenados por position
@router.get("", response_model=list[FormResponse])
async def list_forms(ops: ManageOperations = Depends(get_ops)):

    return [form for form in await ops.list_forms() if form.active]


admin_router = APIRouter(
    prefix="/admin/forms",
    tags=["admin forms"],
    dependencies=[Depends(auth_depends.require_admin)],
)


@admin_router.get("", response_model=list[FormResponse])
async def admin_list_forms(ops: ManageOperations = Depends(get_ops)):

    return await ops.list_forms()


@admin_router.post("", response_model=FormResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_form(body: FormCreate, ops: ManageOperations = Depends(get_ops)):

    return await ops.create_form(**body.model_dump())


@admin_router.get("/{id}", response_model=FormResponse)
async def admin_get_form(id: int, ops: ManageOperations = Depends(get_ops)):

    item = await ops.get_form(id)

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Form not found")

    return item


@admin_router.put("/{id}", response_model=FormResponse)
async def admin_update_form(id: int, body: FormUpdate, ops: ManageOperations = Depends(get_ops)):

    item = await ops.update_form(id, **body.model_dump(exclude_unset=True))

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Form not found")

    return item


@admin_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_form(id: int, ops: ManageOperations = Depends(get_ops)):

    if not await ops.delete_form(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Form not found")
