from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.Notebook import Notebook

class AbstractNotebookRepository(ABC):

    @abstractmethod
    async def create_notebook(self,notebook:Notebook)->None:...
    
    @abstractmethod
    async def save(self,notebook:Notebook)->None:...
    
    @abstractmethod
    async def get_notebook(self,notebook_id:UUID)->Notebook|None:...
    
    @abstractmethod
    async def get_notebooks(self,user_id:UUID)->list[Notebook]:...
    
    @abstractmethod
    async def delete_notebook(self,notebook_id:UUID)->None:...