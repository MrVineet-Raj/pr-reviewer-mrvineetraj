from langgraph.graph import StateGraph,END,START
from app.services.langgraph_nodes import ReviewState,fetch_diff_node,generate_walkthrough,generate_diff_table,generate_sequence_diagram,generate_activity_diagram,post_pr_comment,generate_review_comments,post_review_comments,generate_poetic_lines

def pr_review(owner: str, pull_number: int, repo: str):
    graph = StateGraph(ReviewState)

    graph.add_node("fetch_diff", fetch_diff_node)
    graph.add_node("generate_walkthrough", generate_walkthrough)
    graph.add_node("generate_diff_table", generate_diff_table)
    graph.add_node("generate_sequence_diagram", generate_sequence_diagram)
    graph.add_node("generate_activity_diagram", generate_activity_diagram)
    graph.add_node("post_pr_comment", post_pr_comment)
    graph.add_node("generate_review_comments", generate_review_comments)
    graph.add_node("post_review_comments", post_review_comments)
    graph.add_node("generate_poetic_lines", generate_poetic_lines)

    graph.add_edge(START, "fetch_diff")
    graph.add_edge("fetch_diff", "generate_walkthrough")
    graph.add_edge("generate_walkthrough", "generate_diff_table")
    graph.add_edge("generate_diff_table", "generate_sequence_diagram")
    graph.add_edge("generate_sequence_diagram", "generate_poetic_lines")
    graph.add_edge("generate_poetic_lines", "generate_activity_diagram")
    graph.add_edge("generate_activity_diagram", "post_pr_comment")
    graph.add_edge("post_pr_comment", "generate_review_comments")
    graph.add_edge("generate_review_comments","post_review_comments")
    graph.add_edge("post_review_comments", END)

    compiled = graph.compile()

    return compiled.invoke({
        "owner": owner,
        "pull_number": pull_number,
        "repo": repo,
        "llm_messages": []
    })
