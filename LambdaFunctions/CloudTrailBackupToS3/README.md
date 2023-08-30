## Steps

### 1. Create the S3 bucket:

- Create a S3 bucket with required name in your required region

### 2. Create an IAM Role:

- Go to the AWS IAM Console.
- Create a new IAM role with permissions for CloudTrail (read access) and S3 (write access to the target S3 bucket).
- Attach this IAM role to your Lambda function when you create it.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["cloudtrail:LookupEvents"],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject"],
      "Resource": "arn:aws:s3:::your-s3-bucket-name/*"
    }
  ]
}
```

### 3. Create the Lambda Function:

- Go to the AWS Lambda Console.
- Click "Create function."
- Choose "Author from scratch."
- Fill in the function name, runtime (Python 3.8 or higher is recommended), and choose the IAM role you created in step 2.
- Click "Create function."
- Paste the code present in the main.py
- Set the General Configuration (Timeout and Memory) as per requirement
- Change the bucket name
-

```python
s3_bucket = 'aravindetagi'
```

### 4. Create a Scheduler in Amazon EvenBridge

- cron expression :

```
0 1 * * ? *
```

- Above cron gets executed at morning 1:00 AM everyday
