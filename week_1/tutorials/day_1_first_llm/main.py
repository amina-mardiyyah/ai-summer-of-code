import json
from anthropic import AnthropicVertex
from google.oauth2 import credentials, service_account
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-m', '--model', 
                    required=True, help='Anthropic model to use', 
                    choices=['claude_sonnet_3-5','haiku-3']) 
parser.add_argument('-gcp_cred', required=True, 
                    help='your generated gcp service credentials')

args = parser.parse_args()




#Load service account json generated from Google Cloud
with open(args.gcp_cred, "r") as f:
    print("Loading gcp credentials.....")
    secrets = json.load(f)
    print("Credentials successfully loaded")

_credentials = service_account.Credentials.from_service_account_info(
    secrets, 
    scopes=['https://www.googleapis.com/auth/cloud-platform.read-only']
                                                                     )
regions = ["us-east5",
           "us-central1",
           "europe-west1",
           "europe-west4"]
#region = "europe-west1"

if args.model == "claude_sonnet_3-5":
    models = "claude-3-5-sonnet@20240620"
    region = regions[0]

elif args.model == "haiku-3":
    models = "claude-3-haiku@20240307"
    region = regions[1]


print("Instantiating Anthropic Vertex.............")
client = AnthropicVertex(credentials=_credentials, 
                          project_id=secrets["project_id"],
                          region=region)

print("Starting Q&A system...\n")


message = client.messages.create(
    model = models,
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "Hey Claude!",
        }
    ],
)
print(message.content[0].text)

