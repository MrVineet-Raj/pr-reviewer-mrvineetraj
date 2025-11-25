from app.core.config import env_conf
import requests;
import json
from pydantic import BaseModel
from typing import List

class GithubServiceOutput:
  result:str
  success:bool

  def __init__(self,result:str,success:str):
    self.result = result
    self.success = success


class ReviewSchema(BaseModel):
  body:str
  path:str
  start_line:int
  side: str
  line:int

  def __init__(self,result:str,success:str):
    self.result = result
    self.success = success


class GithubServices:
  def getDiffData(self,owner:str,pull_number:int,repo:str)->GithubServiceOutput:
    try:
      diff_url = f"https://github.com/{owner}/{repo}/pull/{pull_number}.diff"
      diff_response = requests.get(diff_url)
      diff_data = diff_response.text

      return GithubServiceOutput(result=diff_data,success=True)
    except Exception as e:
      return GithubServiceOutput(result=f"{type(e).__name__}, {e}",success=False)
    

  def postPRComments(self,owner:str,pull_number:int,repo:str,body:str)->GithubServiceOutput:
    try:
      url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pull_number}/comments"

      response = requests.post(
        url, 
        headers={
          "Accept": "application/vnd.github+json",
          "X-GitHub-Api-Version": "2022-11-28" ,
          "Authorization":f"Bearer {env_conf.GITHUB_PAT_TOKEN}"
        },
        json={
          "body":body
        }
      )

      data = response.json()

      if data.get("status"):
        print(data.status)
        return GithubServiceOutput(result=f"{data.message}",success=False)



      return GithubServiceOutput(result="Comment posted successfully",success=True)
    except Exception as e:
      return GithubServiceOutput(result=f"{type(e).__name__}, {e}",success=False)
    
  def postReviewComments(owner:str,pull_number:int,repo:str,reviews:List[ReviewSchema])->GithubServiceOutput:
    try:
      url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/comments "

      response = requests.post(url, headers={
          "Accept": "application/vnd.github+json",
          "X-GitHub-Api-Version": "2022-11-28" ,
          "Authorization":f"Bearer {env_conf.GITHUB_PAT_TOKEN}"
      },body={json.dump({"body":reviews})})

      return GithubServiceOutput(result="Comment posted successfully",success=True)
    except Exception as e:
      return GithubServiceOutput(result=f"{type(e).__name__}, {e}",success=False)



github_services = GithubServices()