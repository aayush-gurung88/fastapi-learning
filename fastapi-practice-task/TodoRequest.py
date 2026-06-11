from typing import Optional

from pydantic import BaseModel, Field


#  this is validation schema 

class TodoRequest(BaseModel):
    id: Optional [int] = Field(description= "During Todo creation ID is not required", default=None)
    title: str = Field(min_length=2 , max_length=15)
    description: str = Field(min_length=2 , max_length=50)
    is_completed:Optional [bool] = Field(default=False)
    priority: int = Field(ge=1 , le=5) #le - less than equal to , greater than equal to

    model_config ={
        "json_schema_extra":{
            "example":{
                "title":"Todo Title",
                "description":" Todo description",
                "is_completed":False,
                "priority":4
            }
        }
    }