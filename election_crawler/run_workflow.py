import asyncio
from temporalio import activity, workflow
from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleIntervalSpec,
    ScheduleSpec,
    ScheduleState,
)
from temporalio.worker import Worker
from datetime import timedelta
from time import sleep
with workflow.unsafe.imports_passed_through():
    from election_crawler.reddit.Scraper import Scraper
    from election_crawler.reddit.config import subreddits

@activity.defn
async def runRedditCrawler():
    for sub in subreddits:
        scraper = Scraper(sub)
        scraper \
            .getPosts() \
            .getHotPosts() \
            .uploadToMongo()
        
        print(f"Finished scraping {sub}")
    
    return "Finished scraping all subreddits"

@workflow.defn
class RedditCrawler:
    @workflow.run
    async def run(self):
        res = await workflow.execute_activity(
            runRedditCrawler,
            start_to_close_timeout=timedelta(minutes=30)
        )
    

async def main():
    client = await Client.connect("localhost:7233")

    # worker = Worker(
    #     client,
    #     task_queue="reddit_crawler",
    #     workflows=[RedditCrawler],
    #     activities=[runRedditCrawler]
    # )

    await client.create_schedule(
        "reddit_crawler",
        Schedule(
            action=ScheduleActionStartWorkflow(
                RedditCrawler.run,
                id="reddit_crawler_workflow",
                task_queue="reddit_crawler",
            ),
            spec=ScheduleSpec(
                intervals=[ScheduleIntervalSpec(
                    every=timedelta(minutes=30),
                )]
            ),
            state=ScheduleState(note="Scrapes 25 posts from each subreddit every 30 minutes.")
        )
    )
    # await worker.run()

if __name__ == "__main__":
    asyncio.run(main())