#!/usr/bin/env python3
import aws_cdk as cdk


from src.models.config import AccountConfigStack
from stacks.S3SampleStack import S3SampleStack

app = cdk.App()

environment: str = "development"

aws_account = AccountConfigStack(environment=environment).aws_account

S3SampleStack(
    app,
    f"{environment}-S3SampleStack",
    env=cdk.Environment(account=aws_account.account_id, region=aws_account.region),
)


app.synth()
