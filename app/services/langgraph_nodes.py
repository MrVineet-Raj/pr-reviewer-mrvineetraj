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
    print("Fetching PR Diff")
    diff = github_services.getDiffData(
        owner=state.get("owner"),
        pull_number=state.get("pull_number"),
        repo=state.get("repo")
    )

    return {
        "llm_messages": [
            {"role": "system", "content": SYSTEM_PROMPTS.get("base")},
            {"role": "user", "content": diff.result}
        ]
    }

def generate_walkthrough(state: ReviewState):
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

def generate_diff_table(state: ReviewState):
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

def generate_sequence_diagram(state: ReviewState):
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

def generate_activity_diagram(state: ReviewState):
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

def generate_poetic_lines(state: ReviewState):
    print("Generating activity diagram")
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


def post_pr_comment(state:ReviewState):
    print("Posting  Comment")
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
    
    # github_services.postPRComments(owner=state.get("owner"),pull_number=state.get("pull_number"),repo=state.get("repo"),body=body)

def generate_review_comments(state:ReviewState):
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
    
    print(llm_resp_json)
    return {
        "inline_review_description":llm_resp_json.get("description"),
        "inline_reviews":llm_resp_json.get("review") 
    }




def post_review_comments(state:ReviewState):
    owner = state.get("owner")
    repo = state.get("repo")
    pull_number = state.get("pull_number")
    inline_review_description = state.get("inline_review_description")
    inline_reviews = state.get("inline_reviews")

    github_services.postReviewComments(owner,pull_number,repo,inline_reviews,inline_review_description)
    print(inline_reviews)



# {
#     owner: owner,
#     repo: repo,
#     pull_number: pull_number,
#     event: "COMMENT",
#     body: aiResp?.critical_review.description,
#     comments: aiResp?.critical_review.review,
# }



    

# def prReview(owner: str, pull_number: int, repo: str):
#     graph = StateGraph(ReviewState)

#     graph.add_node("fetch_diff", fetch_diff_node)

#     graph.add_edge(Start, "fetch_diff")
#     graph.add_edge("fetch_diff", End)

#     compiled = graph.compile()

#     return compiled.invoke({
#         "owner": owner,
#         "pull_number": pull_number,
#         "repo": repo,
#         "messages": []
#     })
