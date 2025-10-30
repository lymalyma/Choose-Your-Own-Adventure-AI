from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
# We don't need the manual parser anymore
# from langchain_core.output_parsers import PydanticOutputParser 

from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode
from core.models import StoryLLMResponse, StoryNodeLLM

from dotenv import load_dotenv

load_dotenv()

class StoryGenerator:
 
    @classmethod 
    def _get_llm(cls):
        return ChatOpenAI(model="gpt-4o").with_structured_output(StoryLLMResponse)
        
    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy") -> Story:
        
        try: 
            llm_with_parser = cls._get_llm()

            prompt = ChatPromptTemplate.from_messages([
                ("system", STORY_PROMPT), 
                ("human", f"Create the story with this theme: {theme}")
            ])
            
            chain = prompt | llm_with_parser
            
            # This is guaranteed to be a StoryLLMResponse object
            story_structure = chain.invoke({})

            story_db = Story(title=story_structure.title, session_id=session_id)
            db.add(story_db)
            db.flush()

            # This is guaranteed to be a StoryNodeLLM object
            root_node_data = story_structure.rootNode

            # We don't need this check anymore, it will never be a dict
            # if isinstance(root_node_data, dict): 
            #     root_node_data = StoryNodeLLM.model_validate(root_node_data)

            cls._process_story_node(db, story_db.id, root_node_data, is_root=True)
            db.commit()
            return story_db
        
        except Exception as e: 
            print(f"CRITICAL FAILURE in generate_story: {e}")
            raise e
        
    @classmethod 
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNode: 
        
        # We can now directly access attributes.
        # We are guaranteed they exist if the Pydantic model is valid.
        node = StoryNode(
            story_id=story_id, 
            content=node_data.content, 
            is_root=is_root, 
            is_ending=node_data.isEnding, 
            is_winning_ending=node_data.isWinningEnding,
            options=[] 
        )

        db.add(node)
        db.flush()

        # We can also simplify this check
        if not node.is_ending and node_data.options:
            options_list = []
            for option_data in node_data.options: 
                
                # This is guaranteed to be a StoryNodeLLM object
                next_node = option_data.nextNode

                # We don't need this check, it will never be a dict
                # if isinstance(next_node, dict): 
                #     next_node = StoryNodeLLM.model_validate(next_node)

                child_node = cls._process_story_node(db, story_id, next_node, is_root=False)

                options_list.append({
                    "text": option_data.text, 
                    "node_id": child_node.id
                })

            node.options = options_list

        db.flush()
        return node