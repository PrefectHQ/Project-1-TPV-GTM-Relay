from marvin import ai_fn
from pathlib import Path
from prefect import flow, task
from prefect_aws import S3Bucket

@task
@ai_fn
async def analyze_data(data: dict) -> str:
    """produce a report from the data"""

@flow
async def debt(file_path: Path):
    s3: S3Bucket = await S3Bucket.load("project-1-debt-data")
    data: dict = await s3.read_path(path=file_path)
    
    return await analyze_data(data=data)