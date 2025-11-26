from app.core.config import env_conf
import requests
from typing import List, Optional

class GithubServiceOutput:
    def __init__(self, result: str, success: bool):
        self.result = result
        self.success = success


class GithubServices:

    def getDiffData(self, owner: str, pull_number: int, repo: str) -> GithubServiceOutput:
        try:
            diff_url = f"https://github.com/{owner}/{repo}/pull/{pull_number}.diff"
            diff_response = requests.get(diff_url)
            
            if diff_response.status_code != 200:
                return GithubServiceOutput(
                    result=f"Failed to fetch diff: {diff_response.text}",
                    success=False
                )

            return GithubServiceOutput(result=diff_response.text, success=True)
        except Exception as e:
            return GithubServiceOutput(result=f"{type(e).__name__}: {e}", success=False)


    def postPRComments(self, owner: str, pull_number: int, repo: str, body: str) -> GithubServiceOutput:
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pull_number}/comments"

            response = requests.post(
                url,
                headers={
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                    "Authorization": f"Bearer {env_conf.GITHUB_PAT_TOKEN}"
                },
                json={"body": body}
            )

            if response.status_code not in (200, 201):
                return GithubServiceOutput(
                    result=f"Failed: {response.text}",
                    success=False
                )

            return GithubServiceOutput(result="Comment posted successfully", success=True)

        except Exception as e:
            return GithubServiceOutput(result=f"{type(e).__name__}: {e}", success=False)


    def postReviewComments(self, owner: str, pull_number: int, repo: str, reviews: List[dict],description:str) -> GithubServiceOutput:
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/reviews"

            response = requests.post(
                url,
                headers={
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                    "Authorization": f"Bearer {env_conf.GITHUB_PAT_TOKEN}"
                },
                json={"body": description,"event": "COMMENT","comments":reviews}  # Format depending on GitHub spec
            )

            print(response.json())

            if response.status_code not in (200, 201):
                return GithubServiceOutput(
                    result=f"Failed: {response.text}",
                    success=False
                )

            return GithubServiceOutput(result="Review comment posted successfully", success=True)

        except Exception as e:
            return GithubServiceOutput(result=f"{type(e).__name__}: {e}", success=False)


github_services = GithubServices()