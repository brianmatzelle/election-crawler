package main

import (
	"encoding/json"
	"fmt"
	"time"

	"github.com/mitchellh/mapstructure"
)

// Post represents a Reddit post with relevant fields for LLM.
type Post struct {
	Subreddit        string  `mapstructure:"subreddit"`
	SubredditID      string  `mapstructure:"subreddit_id"`
	Title            string  `mapstructure:"title"`
	Selftext         string  `mapstructure:"selftext"`
	Author           string  `mapstructure:"author"`
	AuthorFlair      string  `mapstructure:"author_flair_text"`
	Score            int     `mapstructure:"score"`
	UpvoteRatio      float64 `mapstructure:"upvote_ratio"`
	NumComments      int     `mapstructure:"num_comments"`
	CreatedUTC       int64   `mapstructure:"created_utc"`
	LinkFlair        string  `mapstructure:"link_flair_text"`
	URL              string  `mapstructure:"url"`
	TotalAwards      int     `mapstructure:"total_awards_received"`
	Controversiality int     `mapstructure:"controversiality"`
	NumReports       int     `mapstructure:"num_reports"`
	CommentList      []Comment
}

// Comment represents a Reddit comment with relevant fields for LLM.
type Comment struct {
	Author           string `mapstructure:"author"`
	AuthorFlair      string `mapstructure:"author_flair_text"`
	Body             string `mapstructure:"body"`
	Score            int    `mapstructure:"score"`
	Depth            int    `mapstructure:"depth"`
	Controversiality int    `mapstructure:"controversiality"`
}

func main() {
	// Simulate JSON data for the post object
	data := `{
    "_id": {
        "$oid": "6689c45c83d38d97d7a970eb"
    },
    "comments": {
        "lbyv8mn": {
            "all_awardings": [],
            "approved_at_utc": null,
            "approved_by": null,
            "archived": false,
            "associated_award": null,
            "author": "ImOnYew",
            "author_flair_background_color": null,
            "author_flair_css_class": null,
            "author_flair_richtext": [],
            "author_flair_template_id": null,
            "author_flair_text": null,
            "author_flair_text_color": null,
            "author_flair_type": "text",
            "author_fullname": "t2_skmh0wx7l",
            "author_is_blocked": false,
            "author_patreon_flair": false,
            "author_premium": false,
            "awarders": [],
            "banned_at_utc": null,
            "banned_by": null,
            "body": "He tries so hard to be a bully, talking over everyone. It's good that destiny can deal with it.",
            "body_html": "\u0026lt;div class=\"md\"\u0026gt;\u0026lt;p\u0026gt;He tries so hard to be a bully, talking over everyone. It\u0026amp;#39;s good that destiny can deal with it.\u0026lt;/p\u0026gt;\n\u0026lt;/div\u0026gt;",
            "can_gild": false,
            "can_mod_post": false,
            "collapsed": false,
            "collapsed_because_crowd_control": null,
            "collapsed_reason": null,
            "collapsed_reason_code": null,
            "comment_type": null,
            "controversiality": 0,
            "created": 1720309933,
            "created_utc": 1720309933,
            "depth": 0,
            "distinguished": null,
            "downs": 0,
            "edited": false,
            "gilded": 0,
            "gildings": {},
            "id": "lbyv8mn",
            "is_submitter": false,
            "likes": null,
            "link_id": "t3_1dx1b0z",
            "locked": false,
            "mod_note": null,
            "mod_reason_by": null,
            "mod_reason_title": null,
            "mod_reports": [],
            "name": "t1_lbyv8mn",
            "no_follow": false,
            "num_reports": null,
            "parent_id": "t3_1dx1b0z",
            "permalink": "/r/Destiny/comments/1dx1b0z/new_vegan/lbyv8mn/",
            "removal_reason": null,
            "replies": "",
            "report_reasons": null,
            "saved": false,
            "score": 17,
            "score_hidden": false,
            "send_replies": true,
            "stickied": false,
            "subreddit": "Destiny",
            "subreddit_id": "t5_2qnvz",
            "subreddit_name_prefixed": "r/Destiny",
            "subreddit_type": "public",
            "top_awarded_type": null,
            "total_awards_received": 0,
            "treatment_tags": [],
            "unrepliable_reason": null,
            "ups": 17,
            "user_reports": []
        },
        "lbyw648": {
            "all_awardings": [],
            "approved_at_utc": null,
            "approved_by": null,
            "archived": false,
            "associated_award": null,
            "author": "cjchristie98",
            "author_flair_background_color": null,
            "author_flair_css_class": null,
            "author_flair_richtext": [],
            "author_flair_template_id": null,
            "author_flair_text": null,
            "author_flair_text_color": null,
            "author_flair_type": "text",
            "author_fullname": "t2_bhq3k",
            "author_is_blocked": false,
            "author_patreon_flair": false,
            "author_premium": false,
            "awarders": [],
            "banned_at_utc": null,
            "banned_by": null,
            "body": "Honestly one of the most loud and insufferable people I’ve ever seen",
            "body_html": "\u0026lt;div class=\"md\"\u0026gt;\u0026lt;p\u0026gt;Honestly one of the most loud and insufferable people I’ve ever seen\u0026lt;/p\u0026gt;\n\u0026lt;/div\u0026gt;",
            "can_gild": false,
            "can_mod_post": false,
            "collapsed": false,
            "collapsed_because_crowd_control": null,
            "collapsed_reason": null,
            "collapsed_reason_code": null,
            "comment_type": null,
            "controversiality": 0,
            "created": 1720310320,
            "created_utc": 1720310320,
            "depth": 0,
            "distinguished": null,
            "downs": 0,
            "edited": false,
            "gilded": 0,
            "gildings": {},
            "id": "lbyw648",
            "is_submitter": false,
            "likes": null,
            "link_id": "t3_1dx1b0z",
            "locked": false,
            "mod_note": null,
            "mod_reason_by": null,
            "mod_reason_title": null,
            "mod_reports": [],
            "name": "t1_lbyw648",
            "no_follow": false,
            "num_reports": null,
            "parent_id": "t3_1dx1b0z",
            "permalink": "/r/Destiny/comments/1dx1b0z/new_vegan/lbyw648/",
            "removal_reason": null,
            "replies": "",
            "report_reasons": null,
            "saved": false,
            "score": 11,
            "score_hidden": false,
            "send_replies": true,
            "stickied": false,
            "subreddit": "Destiny",
            "subreddit_id": "t5_2qnvz",
            "subreddit_name_prefixed": "r/Destiny",
            "subreddit_type": "public",
            "top_awarded_type": null,
            "total_awards_received": 0,
            "treatment_tags": [],
            "unrepliable_reason": null,
            "ups": 11,
            "user_reports": []
        }
    },
    "data": {
        "all_awardings": [],
        "allow_live_comments": false,
        "approved_at_utc": null,
        "approved_by": null,
        "archived": false,
        "author": "TuningsGaming",
        "author_flair_background_color": null,
        "author_flair_css_class": null,
        "author_flair_richtext": [],
        "author_flair_template_id": null,
        "author_flair_text": null,
        "author_flair_text_color": null,
        "author_flair_type": "text",
        "author_fullname": "t2_bk93q",
        "author_is_blocked": false,
        "author_patreon_flair": false,
        "author_premium": false,
        "awarders": [],
        "banned_at_utc": null,
        "banned_by": null,
        "can_gild": false,
        "can_mod_post": false,
        "category": null,
        "clicked": false,
        "content_categories": null,
        "contest_mode": false,
        "created": 1720304607,
        "created_utc": 1720304607,
        "discussion_type": null,
        "distinguished": null,
        "domain": "i.redd.it",
        "downs": 0,
        "edited": false,
        "gilded": 0,
        "gildings": {},
        "hidden": false,
        "hide_score": false,
        "id": "1dx1b0z",
        "is_created_from_ads_ui": false,
        "is_crosspostable": false,
        "is_meta": false,
        "is_original_content": false,
        "is_reddit_media_domain": true,
        "is_robot_indexable": true,
        "is_self": false,
        "is_video": false,
        "likes": null,
        "link_flair_background_color": "#6b6031",
        "link_flair_css_class": "",
        "link_flair_richtext": [],
        "link_flair_template_id": "39762dde-f6f1-11eb-847a-1e223f890317",
        "link_flair_text": "Shitpost",
        "link_flair_text_color": "light",
        "link_flair_type": "text",
        "locked": false,
        "media": null,
        "media_embed": {},
        "media_only": false,
        "mod_note": null,
        "mod_reason_by": null,
        "mod_reason_title": null,
        "mod_reports": [],
        "name": "t3_1dx1b0z",
        "no_follow": false,
        "num_comments": 2,
        "num_crossposts": 0,
        "num_duplicates": 0,
        "num_reports": null,
        "over_18": false,
        "parent_whitelist_status": "some_ads",
        "permalink": "/r/Destiny/comments/1dx1b0z/new_vegan/",
        "pinned": false,
        "post_hint": "image",
        "preview": {
            "enabled": true,
            "images": [
                {
                    "id": "dPX2k2hooVh4_i1hGMJN-dY0dAfO2tHaVgQDYg2DGx0",
                    "resolutions": [
                        {
                            "height": 107,
                            "url": "https://preview.redd.it/s420ibwt4zad1.jpeg?width=108\u0026amp;crop=smart\u0026amp;auto=webp\u0026amp;s=6e9f43528c06bd016e0584190ca9f6a5bab6d310",
                            "width": 108
                        },
                        {
                            "height": 214,
                            "url": "https://preview.redd.it/s420ibwt4zad1.jpeg?width=216\u0026amp;crop=smart\u0026amp;auto=webp\u0026amp;s=e349113d8d0c8986cca7087c05e49902e9ebc23b",
                            "width": 216
                        },
                        {
                            "height": 317,
                            "url": "https://preview.redd.it/s420ibwt4zad1.jpeg?width=320\u0026amp;crop=smart\u0026amp;auto=webp\u0026amp;s=a8b4bbb1699edca1530fd1b2b55092588165ccca",
                            "width": 320
                        }
                    ],
                    "source": {
                        "height": 614,
                        "url": "https://preview.redd.it/s420ibwt4zad1.jpeg?auto=webp\u0026amp;s=628f61f3bdc4696bdb1573f73a37045c0f424b46",
                        "width": 618
                    },
                    "variants": {}
                }
            ]
        },
        "pwls": 7,
        "quarantine": false,
        "removal_reason": null,
        "removed_by": null,
        "removed_by_category": null,
        "report_reasons": null,
        "saved": false,
        "score": 121,
        "secure_media": null,
        "secure_media_embed": {},
        "selftext": "",
        "selftext_html": null,
        "send_replies": true,
        "spoiler": false,
        "stickied": false,
        "subreddit": "Destiny",
        "subreddit_id": "t5_2qnvz",
        "subreddit_name_prefixed": "r/Destiny",
        "subreddit_subscribers": 248289,
        "subreddit_type": "public",
        "suggested_sort": "confidence",
        "thumbnail": "https://b.thumbs.redditmedia.com/FZZx4uUVnUxEIxec45vF2HYi1vYDgcOOLKiYPelm-hc.jpg",
        "thumbnail_height": 139,
        "thumbnail_width": 140,
        "title": "New Vegan",
        "top_awarded_type": null,
        "total_awards_received": 0,
        "treatment_tags": [],
        "ups": 121,
        "upvote_ratio": 0.95,
        "url": "https://i.redd.it/s420ibwt4zad1.jpeg",
        "url_overridden_by_dest": "https://i.redd.it/s420ibwt4zad1.jpeg",
        "user_reports": [],
        "view_count": null,
        "visited": false,
        "whitelist_status": "some_ads",
        "wls": 7
    },
    "finalized": true,
    "id": "1dx1b0z"
}`

	// Unmarshal the JSON into a map
	var jsonData map[string]interface{}
	err := json.Unmarshal([]byte(data), &jsonData)
	if err != nil {
		fmt.Println("Error unmarshaling JSON:", err)
		return
	}

	// Extract main post data
	var post Post
	err = mapstructure.Decode(jsonData["data"], &post)
	if err != nil {
		fmt.Println("Error decoding post data:", err)
		return
	}

	// Extract comments
	commentsMap := jsonData["comments"].(map[string]interface{})
	for _, commentData := range commentsMap {
		var comment Comment
		err = mapstructure.Decode(commentData, &comment)
		if err == nil {
			post.CommentList = append(post.CommentList, comment)
		}
	}

	// Print extracted post and comments data
	fmt.Println("Extracted Post Data:")
	fmt.Printf("Subreddit: %s\n", post.Subreddit)
	fmt.Printf("Subreddit ID: %s\n", post.SubredditID)
	fmt.Printf("Title: %s\n", post.Title)
	fmt.Printf("Selftext: %s\n", post.Selftext)
	fmt.Printf("Author: %s\n", post.Author)
	fmt.Printf("Author Flair: %s\n", post.AuthorFlair)
	fmt.Printf("Score: %d\n", post.Score)
	fmt.Printf("Upvote Ratio: %.2f\n", post.UpvoteRatio)
	fmt.Printf("Number of Comments: %d\n", post.NumComments)
	fmt.Printf("Created UTC: %s\n", time.Unix(post.CreatedUTC, 0).Format(time.RFC3339))
	fmt.Printf("Link Flair: %s\n", post.LinkFlair)
	fmt.Printf("URL: %s\n", post.URL)
	fmt.Printf("Total Awards Received: %d\n", post.TotalAwards)
	fmt.Printf("Controversiality: %d\n", post.Controversiality)
	fmt.Printf("Number of Reports: %d\n\n", post.NumReports)

	fmt.Println("Extracted Comments:")
	for i, comment := range post.CommentList {
		fmt.Printf("Comment %d:\n", i+1)
		fmt.Printf("\tAuthor: %s\n", comment.Author)
		fmt.Printf("\tAuthor Flair: %s\n", comment.AuthorFlair)
		fmt.Printf("\tBody: %s\n", comment.Body)
		fmt.Printf("\tScore: %d\n", comment.Score)
		fmt.Printf("\tDepth: %d\n", comment.Depth)
		fmt.Printf("\tControversiality: %d\n", comment.Controversiality)
	}
}
