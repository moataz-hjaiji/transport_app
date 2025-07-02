# from abc import ABC, abstractmethod
# from typing import TypeVar, Generic, Optional, List, Dict, Any

# T = TypeVar('T') 

# class IBaseRepository(ABC, Generic[T]):
#     @abstractmethod
#     def find(self, filter: Dict[str, Any] = {}) -> List[T]:
#         pass
    
#     @abstractmethod
#     def find_with_pagination(self, filter: Dict[str, Any] = {}, skip: int = 0, limit: int = 100) -> List[T]:
#         pass
    
#     @abstractmethod
#     def update_many(self, filter: Dict[str, Any], update_obj: Dict[str, Any]) -> int:
#         pass
    
#     @abstractmethod
#     def update_by_id(self, id: Any, update_obj: Dict[str, Any]) -> Optional[T]:
#         pass
    
#     @abstractmethod
#     def update(self, filter: Dict[str, Any], update_obj: Dict[str, Any]) -> Optional[T]:
#         pass
    
#     @abstractmethod
#     def delete_by_id(self, id: Any) -> bool:
#         pass
    
#     @abstractmethod
#     def delete(self, filter: Dict[str, Any]) -> bool:
#         pass
    
#     @abstractmethod
#     def delete_many(self, filter: Dict[str, Any]) -> int:
#         pass