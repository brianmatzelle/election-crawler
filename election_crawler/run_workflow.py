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
            .getHotPosts() \
            .uploadToMongo()
        
        print(f"Finished scraping {sub}, sleeping for 10 seconds")
        sleep(10)
    
    return "Finished scraping all subreddits"

@workflow.defn
class RedditCrawler:
    @workflow.run
    async def run(self):
        res = await workflow.execute_activity(
            runRedditCrawler,
            start_to_close_timeout=timedelta(minutes=30)
        )

@activity.defn
async def runUpdateUnfinalizedPosts():
    for sub in subreddits:
        scraper = Scraper(sub)
        log: str = scraper.update_unfinalised_posts()
        
        print(f"finalized posts for {sub}, sleeping for 5 seconds")
        sleep(5)

    return log

@workflow.defn
class UpdateUnfinalizedPosts:
    @workflow.run
    async def run(self):
        log = await workflow.execute_activity(
            runUpdateUnfinalizedPosts,
            start_to_close_timeout=timedelta(minutes=45)
        )
        return log
    

async def main():
    client = await Client.connect("localhost:7233")

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

    await client.create_schedule(
        "update_unfinalized",
        Schedule(
            action=ScheduleActionStartWorkflow(
                UpdateUnfinalizedPosts.run,
                id="update_unfinalized_workflow",
                task_queue="update_unfinalized",
            ),
            spec=ScheduleSpec(
                intervals=[ScheduleIntervalSpec(
                    every=timedelta(minutes=15),
                    offset=timedelta(minutes=7)
                )],
                jitter=timedelta(minutes=1)
            ),
            state=ScheduleState(note="Updates unfinalised posts every 15 minutes.")
        )
    )


if __name__ == "__main__":
    asyncio.run(main())