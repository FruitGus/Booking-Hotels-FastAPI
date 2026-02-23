
from fastapi import Query, APIRouter, Body

from sqlalchemy import insert

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])





hotels = [
    {"id": 1, "title": "Moscow", "name": "moscow_plaza"},
    {"id": 2, "title": "Krasnodar", "name": "krasnodar_star"},
    {"id": 3, "title": "Yekaterinburg", "name": "ekb_hyatt"},
    {"id": 4, "title": "Perm", "name": "perm_ural"},
    {"id": 5, "title": "Tagil", "name": "tagil_hotel"},
    {"id": 6, "title": "Tumen", "name": "tumen_hotel"},
    {"id": 7, "title": "Vladivostok", "name": "vladik_stars"},
    {"id": 8, "title": "Yaroslavl", "name": "yar_hotel"},
]


@router.get("", summary="Получение всех отелей")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)


    return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]




@router.post("", summary="Создание отеля")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Пермь", "value": {
        "title": "Отель Урал",
        "location": "г.Пермь, ул.Ленина 48г",
    }},
    "2": {"summary": "Екатеринбург", "value":{
        "title": "Отель Hyatt",
        "location": "г.Екатеринубург, ул.Бориса Ельцина 6",
    }},
})
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Полное обновление данных об отеле")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}



@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
def partially_update_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}




@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}