# Introduction

This repository is intended to demonstrate the basic process of developing Infrastructure as Code (short for IaC) on the AWS platform by using CDK (Construct Development Kit).
AWS CDK can be written in many programming languages, including:

- TypeScript
- JavaScript
- `Python`
- Java
- C# .Net
- Go

However in this example we'll be mainly using Python for that matter.

## Getting Started

Before going to the fun stuff of writing code, we'll need to make sure we have the neccessary dependencies on our local machine, in order for us to fully integrate CDK into our infrastructure.

1. Dependencies

| Package   | Version | Link    |
|-----------|---------|---------|
|AWS profile| -       | [link](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html)|
|Node js    | >=14.0.0| [link](https://nodejs.org/en/download)|
| Python    | >=3.7.0 | [link](https://www.python.org/downloads/)|
| AWS CLI   |  v2     | [link](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)|


2. Installation guide

In order for us to deploy any resources to our AWS profile, our local machine needs to authenticate and authorize to AWS. There are 2 approaches to tackle that:

1. AWS SSO
Prerequisite: your accout needs to have IAM Identity Center enabled

2. Creating a new user for programmatic access
Prerequisite: you need to have `iam:CreateUser` permission in your account, if you simply only have root (admin) account, then you have more than enough  access to satisfy this requirement

### AWS SSO

Open a terminal and type:

```bash
aws configure sso
```

Follow the command propmts - at the very end the CLI would ask you to authorize the AWS connection by opening a window browser, please verify this part also.

Once you have installed the dependneices, listed above, open a terminal window and type the following command:

### Creating a new user for programmatic access

Open the AWS management console and in the search bar type `iam` on the search bar like [in here](https://imgur.com/a/gg4PZ8R)
Next go to the [users options](https://imgur.com/kuol5cK), create a [new user](https://imgur.com/va6bF1N). Enter a [username](https://www.simplified.guide/_media/aws/iam/create-programmatic-access-user/aws-console-iam-users-add.png?w=700&tok=fcecba). Type a user friendly name.
# TODO: check for which permissions to attach
Click create. Now you should see the newly created [user](https://imgur.com/eR3Ggbm). Click on the user, scroll on the `Security credentials` and at the bottom you'll see [Create access key](https://imgur.com/kyHmkXo). Next you'll have a window for `Access keys best practices & alternatives`. Click on the `Third-party service` and that you confirm the action by clicking on the checkbox.
Add a description value, for example `access-keys-for-cdk`, and copy the [access keys and secret access key](https://imgur.com/sLzVafM.png) to either manually (at `~/.aws/credentials`) or by running `aws configure`.

## Install CDK

Next you need to install the aws-cdk globally on your system by using npm package:

```bash
npm install -g aws-cdk
```

Verify the installation by running:

```bash
cdk --version
```

If the output looks something like `2.X.X (build d111111)`, then the installation was successfull.

Next you'd need to verify if you have an active session with your AWS profile by running:

```bash
aws sts get-caller-identity
```

If you have a valid connection, it should output something like: `account id | IAM identity | account id`

## Setup a local project

Next we need now to setup a local project (you can also connect the project to a remote VCS of your choice). Start by creating an empty directory:

```bash
mkdir cdk-python
```

**Note**: the name of the root directory (in this case cdk-python) would actually inherit the same name as the Cloudformation template when you get at the deploy stage

Now initalize a CDK app by running:

```bash
cdk init app --language python
```

In the `cdk init` command it fortunatelly created for us a  virtual environment for us to use it. Let's activate it and install the neeeded dependencies, listed in the `requirements.txt` file!:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

To verify that the CDK is able to recognize the defaultly created stack, run:

```bash
cdk ls
```

If you see an output of the name of your directory like in my example being: `AwsPythonCdkCodeExampleStack`, then you can proceed to the next step!

Now let's add another stack, that esentially creates us a simple S3 bucket. create a new directory `stacks` and let's name it `S3.Sample.py`

```bash
mkdir stacks
touch S3Sample.py
```

You can paste the following sample code into the .py file:

```python
import aws_cdk as cdk
import aws_cdk.aws_s3 as s3


class S3Sample(cdk.Stack):

    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "MyFirstBucket", versioned=False)

```

You can add this stack to that `app.py` file for the cdk to fetch the stack and deploy it to your AWS environment.
Put this following code snippt at the `app.py` file, right after the `AwsPythonCdkCodeExampleStack` stack definition:

```python

S3Sample(app, "S3Sample")


app.synth()
```

alright now let's synthetize our AWS Cloudformation template by running:

**Note**: Ensure that in the terminal you are located on the root of the project, since the CDK Toolkit (e.g CLI) will try to fetch all of the configuration files in that directory structure order.

```bash
cdk synth
```

If you see a message like:

```bash
Supply a stack id (AwsPythonCdkCodeExampleStack, S3Sample) to display its template.
```

Then you have successfully converted your python cdk code into Cloudformation template. You can find it under `cdk.out` directory

**Hold on!** Before deploying we need to bootstrap our app. The bootstrapping process involves by deploying a `CDKToolkit` template into your AWS account, which would at the end manage and provision your stacks on the cloud.
Replace the `ACCOUNT-NUMBER` and `REGION` with your value

```bash
cdk bootstrap aws://ACCOUNT-NUMBER/REGION
```

Finally deploy the templates into your AWS env:

```bash
cdk deploy S3Sample
```

If everything is deployed successfully, then in the terminal you should see

```bash
Stack ARN:
arn:aws:cloudformation:REGION:ACCOUNT-NUMBER:...
```

Congrats, you now know how to use CDK !

### Cleaning up

Now we can easily destory our newly created CloudFormation stack simply by running:

```bash
cdk destroy S3Sample
```

## Contribute

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:

- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)
