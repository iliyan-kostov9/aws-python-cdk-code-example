#!/usr/bin/env python3
import aws_cdk as cdk


from src.models.config import AccountConfigStack
from stacks.S3Sample import S3Sample

app = cdk.App()

aws_account = AccountConfigStack(environment="development").aws_account

S3Sample(
    app,
    "S3Sample",
    env=cdk.Environment(account=aws_account.account_id, region=aws_account.region),
)


app.synth()
