from dataclasses import dataclass, field
import boto3
import json
import os


@dataclass(frozen=True)
class AWSAccountWrapper:
    region: str = field(init=True, default="eu-west-1")
    account_id: str = field(init=True, default="123456789012")
    role_name: any = field(init=False, default=None)
    session: any = field(init=False, default=None)
    sts_client: any = field(init=False, default=None)
    iam_client: any = field(init=False, default=None)
    organizations_client: any = field(init=False, default=None)
    assume_role_session: any = field(init=False, default=None)
    assumed_session: any = field(init=False, default=None)

    # TODO: Implement __post_init__ method
    # def __post_init__(self):
    #     self.assume_role()

    def assume_role(self):
        self.session = boto3.Session()
        self.sts_client = self.session.client("sts")
        self.iam_client = self.session.client("iam")
        self.organizations_client = self.session.client("organizations")
        self.assume_role_session = self.sts_client.assume_role(
            RoleArn=f"arn:aws:iam::{self.account_id}:role/{self.role_name}",
            RoleSessionName="cross_account_session",
        )
        self.assumed_session = boto3.Session(
            aws_access_key_id=self.assume_role_session["Credentials"]["AccessKeyId"],
            aws_secret_access_key=self.assume_role_session["Credentials"][
                "SecretAccessKey"
            ],
            aws_session_token=self.assume_role_session["Credentials"]["SessionToken"],
        )
        self.sts_client = self.assumed_session.client("sts")


def _build_aws_account_wrapper(config: dict) -> AWSAccountWrapper:

    return AWSAccountWrapper(
        account_id=str(config.get("account_id")),
        region=str(config.get("region")),
    )


@dataclass(frozen=False)
class AccountConfigStack:
    aws_account: AWSAccountWrapper

    def __init__(self, environment: str = "development") -> None:

        config_file_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "config",
            f"config-{environment}.json",
        )

        with open(
            config_file_path,
            "r",
            encoding="utf-8",
        ) as config_file:
            config_json = json.load(config_file)

        self.aws_account = _build_aws_account_wrapper(config_json)
