
- aws configure  ( to create default profile)

- aws configure list (to see creds of default profile) 

- aws configure list --profile <profile-name>

(configure specific profile)
- aws configure --profile dmart-uat



- aws s3 ls --profile dmart-uat


aws configure list-profiles


aws sts get-caller-identity

aws sts get-caller-identity --profile <profile-name>

