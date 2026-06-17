import random

class HashtagEngine:
    def __init__(self):
        self.database = {
            "Technology": {
                "trending": ["#tech","#innovation","#AI","#coding","#programming","#developer","#startup","#digital"],
                "niche": ["#techtips","#devlife","#coders","#technews","#pythoncode","#webdev","#appdev"],
                "engagement": ["#techcommunity","#learnprogramming","#techie","#futuretech"]
            },
            "Business": {
                "trending": ["#business","#entrepreneur","#success","#marketing","#startup","#growth","#leadership"],
                "niche": ["#smallbusiness","#biztips","#businessowner","#solopreneur","#businesstips"],
                "engagement": ["#businesscommunity","#entrepreneurlife","#hustle","#grind","#businessgrowth"]
            },
            "Health": {
                "trending": ["#health","#fitness","#wellness","#healthylifestyle","#selfcare","#mentalhealth"],
                "niche": ["#healthtips","#fitnessmotivation","#healthyeating","#fitlife","#gymlife"],
                "engagement": ["#healthcommunity","#fitnessjourney","#mentalhealthmatters","#bodypositive"]
            },
            "Fashion": {
                "trending": ["#fashion","#style","#ootd","#fashionblogger","#beauty","#streetstyle"],
                "niche": ["#fashionista","#styleinspo","#fashionstyle","#outfitideas","#fashiondaily"],
                "engagement": ["#fashioncommunity","#styleblogger","#fashionlover","#fashionaddict"]
            },
            "Food": {
                "trending": ["#food","#foodie","#instafood","#yummy","#delicious","#cooking","#homemade"],
                "niche": ["#foodstagram","#foodlover","#foodblogger","#cheflife","#kitchen","#baking"],
                "engagement": ["#foodcommunity","#foodgasm","#hungry","#foodshare","#tasty"]
            },
            "Travel": {
                "trending": ["#travel","#travelgram","#wanderlust","#adventure","#explore","#vacation"],
                "niche": ["#travelblogger","#traveladdict","#globetrotter","#backpacking"],
                "engagement": ["#travelcommunity","#passionpassport","#worldtraveler","#traveldeeper"]
            }
        }
        self.general = {
            "trending": ["#viral","#trending","#explore","#fyp","#foryou"],
            "daily": ["#mondaymotivation","#tuesdaytip","#wednesdaywisdom","#throwbackthursday","#fridayfeeling"],
            "engagement": ["#like","#comment","#share","#follow","#community"]
        }
    
    def get_hashtags(self, industry, count=15):
        data = self.database.get(industry, self.database["Business"])
        trending = random.sample(data["trending"], min(5, len(data["trending"])))
        niche = random.sample(data["niche"], min(5, len(data["niche"])))
        engagement = random.sample(data["engagement"], min(3, len(data["engagement"])))
        general = random.sample(self.general["engagement"], 2)
        all_tags = trending + niche + engagement + general
        random.shuffle(all_tags)
        return all_tags[:count]
    
    def get_best_times(self, industry):
        times = {
            "Technology": ["9 AM","12 PM","5 PM","8 PM"],
            "Business": ["7 AM","11 AM","2 PM","6 PM"],
            "Health": ["6 AM","12 PM","5 PM","9 PM"],
            "Fashion": ["10 AM","1 PM","7 PM","9 PM"],
            "Food": ["8 AM","12 PM","6 PM","8 PM"],
            "Travel": ["8 AM","2 PM","7 PM","10 PM"]
        }
        return times.get(industry, ["9 AM","12 PM","3 PM","7 PM"])
    
    def get_ideas(self, industry):
        ideas = {
            "Technology": ["Share a tech tip","Behind-the-scenes of your work","Tool recommendation","Industry news","Career advice"],
            "Business": ["Business lesson learned","Client success story","Productivity hack","Industry trend","Networking tip"],
            "Health": ["Quick workout","Healthy recipe","Wellness tip","Mental health check","Fitness progress"],
            "Fashion": ["Outfit of the day","Style tip","New collection","Trend alert","Wardrobe essential"],
            "Food": ["Recipe reveal","Cooking tip","Restaurant review","Food photo tip","Meal prep idea"],
            "Travel": ["Destination highlight","Travel tip","Trip photo","Packing hack","Budget travel advice"]
        }
        return ideas.get(industry, ideas["Business"])