from app.core.config import env_conf
from openai import OpenAI
import json
from langgraph.graph import MessagesState
from pydantic import BaseModel
from app.services.github_service import github_services
from app.core.prompt import SYSTEM_PROMPTS

openai = OpenAI(api_key=env_conf.OPENAI_API_KEY)

class ReviewState(MessagesState):
    owner: str
    pull_number: int
    repo: str
    walkthrough: str | None = None  
    file_change_table: str | None = None  
    sequence_diagram: str | None = None  
    activity_diagram: str | None = None
    poem:str | None = None
    er_diagram:str | None = None  
    inline_review_description:str | None = None  
    inline_reviews:any 
    llm_messages:any


def fetch_diff_node(state: ReviewState):
    """
    Fetches the diff data for a pull request from GitHub and initializes LLM messages.
    
    Args:
        state (ReviewState): Current state containing owner, pull_number, and repo
        
    Returns:
        dict: Contains llm_messages with system prompt and diff data
        
    Raises:
        Exception: Re-raises any exceptions from GitHub API calls
    """
    try:
        print("Fetching PR Diff")
        diff = github_services.getDiffData(
            owner=state.get("owner"),
            pull_number=state.get("pull_number"),
            repo=state.get("repo")
        )

        if not diff.success:
            raise Exception(
                f"{diff.result}"
            )

        return {
            "llm_messages": [
                {"role": "system", "content": SYSTEM_PROMPTS.get("base")},
                {"role": "user", "content": diff.result}
            ]
        }
    except Exception as e:
        print(f"Error fetching diff: {e}")
        raise

def generate_walkthrough(state: ReviewState):
    """
    Generates a walkthrough description of the pull request changes using LLM.
    
    Args:
        state (ReviewState): Current state containing llm_messages
        
    Returns:
        dict: Contains the generated walkthrough text
    """
    try:
        print("Generating walkthrough")
        messages = state.get("llm_messages")
        updated_messages = messages + [{
            "role": "user",
            "content": SYSTEM_PROMPTS.get("walkthrough")
        }]
        llm_resp = openai.responses.create(
           model="gpt-5.1",      reasoning={
               "effort":"none"
           },
           input=updated_messages
        )

        walkthrough = llm_resp.output_text
        return {
            "walkthrough":walkthrough
        }
    
    except Exception as e:
        print(f"Error generating walkthrough: {e}")
        raise

def generate_diff_table(state: ReviewState):
    """
    Generates a formatted table of file changes from the pull request diff.
    
    Args:
        state (ReviewState): Current state containing llm_messages
        
    Returns:
        dict: Contains the generated file changes table
    """
    try:
        print("Generating diff table")
        messages = state.get("llm_messages")
        updated_messages = messages + [{
            "role": "user",
            "content": SYSTEM_PROMPTS.get("changes")
        }]
        llm_resp = openai.responses.create(
           model="gpt-5.1",      reasoning={
               "effort":"none"
           },
           input=updated_messages
        )

        file_change_table = llm_resp.output_text
        return {
            "file_change_table":file_change_table
        }
    except Exception as e:
        print(f"Error generating diff table: {e}")
        raise

def generate_sequence_diagram(state: ReviewState):
    """
    Generates a sequence diagram representation of the code changes flow.
    
    Args:
        state (ReviewState): Current state containing llm_messages
        
    Returns:
        dict: Contains the generated sequence diagram markup
    """
    try:
        print("Generating sequence diagram")
        messages = state.get("llm_messages")
        updated_messages = messages + [{
            "role": "user",
            "content": SYSTEM_PROMPTS.get("sequence_diagram")
        }]

        llm_resp = openai.responses.create(
           model="gpt-5.1",
           reasoning={
               "effort":"medium"
           },
           input=updated_messages
        )

        sequence_diagram = llm_resp.output_text
        return {
            "sequence_diagram":sequence_diagram
        }
    except Exception as e:
        print(f"Error generating sequence diagram: {e}")
        raise

def generate_activity_diagram(state: ReviewState):
    """
    Generates an activity diagram showing the workflow of code changes.
    
    Args:
        state (ReviewState): Current state containing llm_messages
        
    Returns:
        dict: Contains the generated activity diagram markup
    """
    try:
        print("Generating activity diagram")
        messages = state.get("llm_messages")
        updated_messages = messages + [{
            "role": "user",
            "content": SYSTEM_PROMPTS.get("activity_diagram")
        }]
        llm_resp = openai.responses.create(
           model="gpt-5.1",
                 reasoning={
               "effort":"medium"
           },
           input=updated_messages
        )

        activity_diagram = llm_resp.output_text
        return {
            "activity_diagram":activity_diagram
        }
    except Exception as e:
        print(f"Error generating activity diagram: {e}")
        return {"activity_diagram": "Error generating activity diagram"}

def generate_poetic_lines(state: ReviewState):
    """
    Generates creative poetic lines describing the pull request changes.
    
    Args:
        state (ReviewState): Current state containing llm_messages
        
    Returns:
        dict: Contains the generated poem text
    """
    try:
        print("Generating poetic lines")
        messages = state.get("llm_messages")
        updated_messages = messages + [{
            "role": "user",
            "content": SYSTEM_PROMPTS.get("poem")
        }]

        llm_resp = openai.responses.create(
           model="gpt-5.1",
           reasoning={
               "effort":"none"
           },
           input=updated_messages
        )

        poem = llm_resp.output_text
        return {
            "poem":poem
        }
    except Exception as e:
        print(f"Error generating poetic lines: {e}")
        raise


def post_pr_comment(state:ReviewState):
    """
    Posts a comprehensive comment to the pull request containing all generated content.
    Combines walkthrough, file changes, diagrams, and poem into a formatted comment.
    
    Args:
        state (ReviewState): Current state containing all generated content
    """
    try:
        print("Posting Comment")
        walkthrough = state.get("walkthrough")
        file_change_table = state.get("file_change_table")
        sequence_diagram = state.get("sequence_diagram")
        activity_diagram = state.get("activity_diagram")
        poem = state.get("poem")

        body = f"""
# Walkthrough
{walkthrough}

# File Changes
{file_change_table}

# Sequence Diagrams
{sequence_diagram}

# Activity Diagrams
{activity_diagram}


{poem}

"""
        
        res = github_services.postPRComments(owner=state.get("owner"),pull_number=state.get("pull_number"),repo=state.get("repo"),body=body)

        if not res.success:
            raise Exception(
                f"{res.result}"
            )
    except Exception as e:
        print(f"Error posting PR comment: {e}")
        raise

def generate_review_comments(state:ReviewState):
    """
    Generates inline review comments for specific lines of code in the pull request.
    Returns structured JSON with description and individual review comments.
    
    Args:
        state (ReviewState): Current state containing llm_messages
        
    Returns:
        dict: Contains inline_review_description and inline_reviews array
    """
    print("Generating Review Comments")
    try:
        messages = state.get("llm_messages")
        updated_messages = messages + [{
                "role": "user",
                "content": SYSTEM_PROMPTS.get("inline_review")
            }]
        llm_resp = openai.responses.create(
           model="gpt-5.1",
           reasoning={
               "effort":"low"
           },
           input=updated_messages
        )

        llm_resp_json = json.loads(llm_resp.output_text)
        
        return {
            "inline_review_description":llm_resp_json.get("description"),
            "inline_reviews":llm_resp_json.get("review") 
        }
    except Exception as e:
        print(f"Error generating review comments: {e}")
        raise


def post_review_comments(state:ReviewState):
    """
    Posts the generated inline review comments to the GitHub pull request.
    
    Args:
        state (ReviewState): Current state containing review data and PR information
    """
    print("Posting Review Comments")
    try:
        owner = state.get("owner")
        repo = state.get("repo")
        pull_number = state.get("pull_number")
        inline_review_description = state.get("inline_review_description")
        inline_reviews = state.get("inline_reviews")

        res = github_services.postReviewComments(owner,pull_number,repo,inline_reviews,inline_review_description)
        if not res.success:
            raise Exception(
                f"{res.result}"
            )
        
    except Exception as e:
        print(f"Error posting review comments: {e}")
        raise
