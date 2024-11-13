package models

// Post represents a Reddit post with relevant fields for LLM.
type Post struct {
	Subreddit        string    `json:"subreddit"`
	SubredditID      string    `json:"subreddit_id"`
	Title            string    `json:"title"`
	Selftext         string    `json:"selftext"`
	Author           string    `json:"author"`
	AuthorFlair      string    `json:"author_flair_text"`
	Score            int       `json:"score"`
	UpvoteRatio      float64   `json:"upvote_ratio"`
	NumComments      int       `json:"num_comments"`
	CreatedUTC       int64     `json:"created_utc"`
	LinkFlair        string    `json:"link_flair_text"`
	URL              string    `json:"url"`
	TotalAwards      int       `json:"total_awards_received"`
	Controversiality int       `json:"controversiality"`
	NumReports       int       `json:"num_reports"`
	CommentList      []Comment `json:"comments,omitempty"`
}

// Comment represents a Reddit comment with relevant fields for LLM.
type Comment struct {
	Author           string `json:"author"`
	AuthorFlair      string `json:"author_flair_text"`
	Body             string `json:"body"`
	Score            int    `json:"score"`
	Depth            int    `json:"depth"`
	Controversiality int    `json:"controversiality"`
}
