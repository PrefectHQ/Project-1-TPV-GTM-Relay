from marvin import ai_fn
from pathlib import Path
from prefect import flow, task
from prefect_aws import S3Bucket, AwsCredentials
import asyncio


@task
@ai_fn
async def analyze_data(data: dict) -> str:
    """produce a report from the data"""


@task
async def save_report(report: str, s3_key: Path):
    AwsCredentials("sales-engineering-tpv-user")

    s3: S3Bucket = await S3Bucket.load("project-1-debt-data")
    await s3.write_path(path=f"output/{s3_key}", data=report)
    return s3_key


@flow
async def debt(file_path: str):
    s3: S3Bucket = await S3Bucket.load("dbt-data")
    data: dict = await s3.read_path(path=file_path)

    await analyze_data(data=data)
    await save_report()


if __name__ == "__main__":
    asyncio.run(debt(file_path=r"raw-data/1999-dti-data.csv"))
