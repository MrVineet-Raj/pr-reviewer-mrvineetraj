import json
import re

def extract_json(text: str):
    """Try several strategies to find and parse JSON in LLM text."""
    # direct parse
    try:
        return json.loads(text)
    except Exception:
        pass

    # code block with ```json or ```
    m = re.search(r"```(?:json)?\n(.*?)```", text, re.S | re.I)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except Exception:
            pass

    # first { ... } or [ ... ] (simple heuristic)
    for open_ch, close_ch in [('{', '}'), ('[', ']')]:
        start = text.find(open_ch)
        end = text.rfind(close_ch)
        if start != -1 and end != -1 and end > start:
            candidate = text[start:end + 1]
            try:
                return json.loads(candidate)
            except Exception:
                pass

    raise ValueError("No valid JSON found in text")

# ...existing code...


# ...existing code...

def post_review_comments(state:ReviewState):
    # similar to generate_review_comments — reuse helper
    messages = state.get("llm_messages")
    updated_messages = messages + [{
            "role": "user",
            "content": SYSTEM_PROMPTS.get("inline_review")
        }]
    llm_resp = openai.responses.create(
       model="gpt-5.1",
       reasoning={"effort":"medium"},
       input=updated_messages
    )

    try:
        parsed = _extract_json(llm_resp.output_text)
    except ValueError as e:
        print("JSON parse error:", e)
        print("LLM output:", llm_resp.output_text)
        return

    comments = parsed if isinstance(parsed, list) else parsed.get("comments") or []
    description = parsed.get("description") if isinstance(parsed, dict) else ""

    github_services.postReviewComments(
        owner=state.get("owner"),
        pull_number=state.get("pull_number"),
        repo=state.get("repo"),
        reviews=comments,
        description=description,
    )
# ...existing code...