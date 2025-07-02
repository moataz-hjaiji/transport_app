# from sqlalchemy.orm import Session
# from typing import Type, TypeVar,List,Any,Optional
# from sqlalchemy import update, delete
# from sqlalchemy.future import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from .repository import IBaseRepository

# ModelType = TypeVar('ModelType')

# class BaseRepository(IBaseRepository[ModelType]):
#     def __init__(self, session: AsyncSession, model: Type[ModelType]):
#         self.session = session
#         self.model = model
    
#     async def find(self, filter: dict = {}) -> List[ModelType]:
#         stmt = select(self.model).filter_by(**filter)
#         result = await self.session.execute(stmt)
#         return result.scalars().all()
    
#     async def find_with_pagination(self, filter: dict = {}, skip: int = 0, limit: int = 100) -> List[ModelType]:
#         stmt = select(self.model).filter_by(**filter).offset(skip).limit(limit)
#         result = await self.session.execute(stmt)  # This is correct
#         return result.scalars().all()  # No await needed here

    
#     async def update_many(self, filter: dict, update_obj: dict) -> int:
#         stmt = update(self.model).where(*[getattr(self.model, k) == v for k, v in filter.items()]).values(**update_obj)
#         result = await self.session.execute(stmt)
#         await self.session.commit()
#         return result.rowcount
    
#     async def update_by_id(self, id: Any, update_obj: dict) -> Optional[ModelType]:
#         stmt = select(self.model).where(self.model.id == id)
#         result = await self.session.execute(stmt)
#         instance = result.scalar_one_or_none()
#         if instance:
#             for key, value in update_obj.items():
#                 setattr(instance, key, value)
#             await self.session.commit()
#             await self.session.refresh(instance)
#         return instance
    
#     async def update(self, filter: dict, update_obj: dict) -> Optional[ModelType]:
#         stmt = select(self.model).filter_by(**filter)
#         result = await self.session.execute(stmt)
#         instance = result.scalar_one_or_none()
#         if instance:
#             for key, value in update_obj.items():
#                 setattr(instance, key, value)
#             await self.session.commit()
#             await self.session.refresh(instance)
#         return instance
    
#     async def delete_by_id(self, id: Any) -> bool:
#         stmt = delete(self.model).where(self.model.id == id)
#         result = await self.session.execute(stmt)
#         await self.session.commit()
#         return result.rowcount > 0
    
#     async def delete(self, filter: dict) -> bool:
#         stmt = delete(self.model).filter_by(**filter)
#         result = await self.session.execute(stmt)
#         await self.session.commit()
#         return result.rowcount > 0
    
#     async def delete_many(self, filter: dict) -> int:
#         stmt = delete(self.model).filter_by(**filter)
#         result = await self.session.execute(stmt)
#         await self.session.commit()
#         return result.rowcount