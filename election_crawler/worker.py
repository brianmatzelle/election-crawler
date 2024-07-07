from temporalio import workflow
from temporalio.worker import Worker
from temporalio.client import Client
import asyncio
with workflow.unsafe.imports_passed_through():
    from election_crawler.run_workflow import RedditCrawler, runRedditCrawler
    
async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="reddit_crawler",
        workflows=[RedditCrawler],
        activities=[runRedditCrawler]
    )

    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())