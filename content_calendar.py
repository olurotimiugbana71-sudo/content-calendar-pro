from datetime import datetime, timedelta
import json, os

class ContentCalendar:
    def __init__(self):
        self.data_file = "calendar_data.json"
        self.posts = []
        if os.path.exists(self.data_file):
            with open(self.data_file) as f:
                self.posts = json.load(f)
    
    def save(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.posts, f, indent=2)
    
    def add_post(self, post_data):
        post = {
            "id": len(self.posts) + 1,
            "date": post_data.get("date", datetime.now().strftime("%Y-%m-%d")),
            "time": post_data.get("time", "9:00 AM"),
            "platform": post_data.get("platform", "Instagram"),
            "content_type": post_data.get("content_type", "Post"),
            "caption": post_data.get("caption", ""),
            "hashtags": post_data.get("hashtags", []),
            "industry": post_data.get("industry", "Business"),
            "status": "Scheduled",
            "created": datetime.now().isoformat()
        }
        self.posts.append(post)
        self.save()
        return post
    
    def get_week(self, start_date=None):
        if start_date is None:
            start_date = datetime.now()
        week_start = start_date - timedelta(days=start_date.weekday())
        calendar = {}
        for i in range(7):
            day = (week_start + timedelta(days=i)).strftime("%Y-%m-%d")
            calendar[day] = [p for p in self.posts if p["date"] == day]
        return calendar
    
    def get_analytics(self):
        if not self.posts:
            return None
        platforms = {}
        statuses = {}
        types = {}
        for p in self.posts:
            platforms[p["platform"]] = platforms.get(p["platform"], 0) + 1
            statuses[p["status"]] = statuses.get(p["status"], 0) + 1
            types[p["content_type"]] = types.get(p["content_type"], 0) + 1
        
        return {
            "total_posts": len(self.posts),
            "by_platform": platforms,
            "by_status": statuses,
            "by_type": types,
            "total_hashtags": sum(len(p.get("hashtags", [])) for p in self.posts)
        }
    
    def get_upcoming(self, limit=5):
        today = datetime.now().strftime("%Y-%m-%d")
        upcoming = [p for p in self.posts if p["date"] >= today and p["status"] == "Scheduled"]
        upcoming.sort(key=lambda x: x["date"])
        return upcoming[:limit]