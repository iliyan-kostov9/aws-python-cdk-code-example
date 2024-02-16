
class LambdaStack(cdk.Stack):

    const fn = new lambda.Function(this, 'MyFunction', {
    runtime: lambda.Runtime.NODEJS_18_X,
    handler: 'index.handler',
    code: lambda.Code.fromAsset(path.join(__dirname, 'lambda-handler')),
    });
