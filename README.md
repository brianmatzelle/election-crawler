# About

This project aims to archive public opinion of political subreddits, in the months leading to the 2024 United States election. The first post archived was created on **July 6, 2024.**

In `finetune/`, we inspect the data, decide which fields to include in the cleaned dataset. Only fields that are capable of mapping to an interesting finetuned models will be included in the cleaned dataset.

E.g.

| **Field(s)**              | **Finetuned LLM**                        |
| ------------------------------- | ---------------------------------------------- |
| `controversiality`            | Controversial post/comment generator           |
| `subreddit`                   | `r/Hasan_Piker` post generator               |
| `subreddit + comments`        | `r/Hasan_Piker` comment generator or chatbot |
| `upvote_ratio`                | Loved/hated post generator                     |
| `upvote_ratio + total_awards` | Viral post generator                           |

The data in this module is helpful for finetuning ONLY, not general data analysis. However, future research should be done to compare varying data within the corpus (idk if that's the right word lol). Some data analysis ideas for this are really interesting, but are outside of the scope of this project.

E.g.,

1. **Rate the toxicity of each community** (AKA subreddit) by using pre-existing models to determine the amount of hatespeech in comments, proportional to the total amount of comments scraped from each respective community. Consider removing controversial comments, since controversiality implies the community's rejection of that given opinion.
2. **Rate the contentiousness and the level of internal conflict** of a community, by measuring the proportionality of controversial comments to viral, or normal comments. The presupposition here is that controversiality represents a community's rejection of a comment or idea.  I argue that, a higher amount of rejection equates to more internal conflict and toxicity. This argument requires another presupposition to be agreed upon: communities battle a proportionally equal amount of "trolls" or "rage bait", i.e., dishonest actors aiming to disrupt discord within a community for trivial reasons. If this cannot be agreed upon, mitigating efforts to expell dishonest actors from the dataset would need to be taken. Analyzing each user's volume of interactions and judging the genuinity of each interaction should suffice. If a user's actions are consistently statistically extreme, it can be assumed that they are most likely an outlier, and therefore can be expelled from the dataset. I'm pretty sure  this can be done in 0(1) time, just update the user's rating when a new action is discovered.
3. Determinine what "**Viral**" means in each community, possibly by creating a normal distribution(?) of `upvote_count `s, then concluding what percentile should be considered "Viral." In my opinion, creating refined datasets such as this would allow for much stronger analysis. For example, after refining a subset of viral comments for each community, *(where each subset contains the 99th percentile of viral comments per community, therefore differing in sample size)*, one could compare the most celebrated ideas of each political community, then draw conclusions from there.
4. Hypothesize characteristics of an "echo chamber," then analyze the data accordingly to rank communities based their echo chamber rating.
