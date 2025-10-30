from typing import List, Optional 
from pydantic import BaseModel, Field

# Note: We don't need Dict or Any anymore
# from typing import List, Dict, Any, Optional 


class StoryOptionLLM(BaseModel): 
    text: str = Field(description="the text of the option shown to the user")
    
    # --- FIX 1 ---
    # The 'nextNode' is not a generic dictionary,
    # it is another 'StoryNodeLLM'.
    # We use a string for the type hint because StoryNodeLLM isn't defined yet.
    nextNode: 'StoryNodeLLM' = Field(description="the next node that this option leads to")


class StoryNodeLLM(BaseModel):
    content: str = Field(description="the content of the story node")
    isEnding: bool = Field(description="whether this node is an ending node")
    isWinningEnding: bool = Field(description="whether this ending is a winning ending node")
    # This line is correct, it uses the class we just defined.
    options: Optional[List[StoryOptionLLM]] = Field(default=None, description="the options for this node")


class StoryLLMResponse(BaseModel):
    title: str = Field(description="the title of the story")
    rootNode: StoryNodeLLM = Field(description="the root node of the story")    


# --- FIX 2 ---
# At the end of the file, we tell all models that use
# forward references (the string hints) to rebuild themselves.
StoryOptionLLM.model_rebuild()
StoryNodeLLM.model_rebuild()
StoryLLMResponse.model_rebuild()