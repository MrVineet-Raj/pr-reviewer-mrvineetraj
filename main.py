import requests
from app.core.config import env_conf
import json




owner = "mrvineet-raj"
repo = "bookstore"
pr_number = 1

url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"

response = requests.get(url, headers={
    "Accept": "application/vnd.github+json"
})

data = response.json()
with open("pr_response.json", "w") as f:
    json.dump(data, f, indent=2)

diff_url  = data.get("diff_url")
diff_response = requests.get(diff_url, headers={
    # "Accept": "application/vnd.github+text"
})

# print(diff_response.text)
diff_data = diff_response.text
with open("diff_data.txt", "w") as f:
    f.write(diff_data)