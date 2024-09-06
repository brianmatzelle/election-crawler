from temporalio import workflow
from temporalio.worker import Worker
from temporalio.client import Client
import asyncio
with workflow.unsafe.imports_passed_through():
    from election_crawler.run_workflow import RedditCrawler, runRedditCrawler, UpdateUnfinalizedPosts, runUpdateUnfinalizedPosts
    
async def main() -> None:
    client = await Client.connect("localhost:7233")

    crawler_worker = Worker(
        client,
        task_queue="reddit_crawler",
        workflows=[RedditCrawler],
        activities=[runRedditCrawler]
    )

    update_unfinalized_worker = Worker(
        client,
        task_queue="update_unfinalized",
        workflows=[UpdateUnfinalizedPosts],
        activities=[runUpdateUnfinalizedPosts]
    )

    workers: list = [crawler_worker, update_unfinalized_worker]
    await asyncio.gather(*[worker.run() for worker in workers])

if __name__ == "__main__":
    asyncio.run(main())