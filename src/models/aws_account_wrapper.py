class AWSAccountWrapper:

    # This class is used to wrap the AWS account and role information
    def __init__(self, account_id, account_name, role_name):
        self.account_id = account_id
        self.account_name = account_name
        self.role_name = role_name
        self.session = None
        self.sts_client = None
        self.iam_client = None
        self.organizations_client = None
        self.assume_role()

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
