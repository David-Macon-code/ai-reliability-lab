import boto3
import json

bedrock = boto3.client('bedrock', region_name='us-east-1')  # or your region

# Get details for a specific version
response = bedrock.get_guardrail(
    guardrailIdentifier='9g6hem28nedj',  # e.g., 'abc123xyz' or full ARN
    guardrailVersion='1'  # or 'DRAFT' to compare
)

print(json.dumps(response, indent=2, default=str))

# Key fields to look for:
# - 'version': '1' (confirms it exists)
# - 'createdAt': timestamp (shows when it was "deployed")
# - 'status': Often 'READY' or similar for the guardrail overall (not per-version, but indicates health)
# - Full config details will be returned if the version is valid