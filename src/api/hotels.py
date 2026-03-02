from email.policy import default

from fastapi import Query, APIRouter, Body, Path

from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])






@router.get("", summary="Получение всех отелей")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(default=None, description="Местоположение"),
        title: str | None = Query(default=None, description="Название отеля"),

):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.get("/{hotel_id}", summary="Получение одного отеля по id")
async def get_hotel(hotel_id: int = Path(description="Айдишник")):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)




@router.post("", summary="Создание отеля")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Пермь",
          "value": {
        "title": "Отель Урал",
        "location": "г.Пермь, ул.Ленина 48г",
    }},
    "2": {"summary": "Екатеринбург",
          "value":{
        "title": "Отель Hyatt",
        "location": "г.Екатеринубург, ул.Бориса Ельцина 6",
    }},
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Полное обновление данных об отеле")
async def update_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()

    return {"status": "OK"}



@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
async def partially_update_hotel(hotel_id: int, hotel_data: HotelPATCH):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, is_patch = True, id=hotel_id)
        await session.commit()

    return {"status": "OK"}




@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}