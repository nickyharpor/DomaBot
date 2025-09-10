from mongo import Mongo

class TelegramUserManager:
    def __init__(self, mongo: Mongo, collection: str = "telegram_users"):
        self.mongo = mongo
        self.collection = collection

    def save_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
        """Save a new user to MongoDB if not already existing."""
        existing = self.mongo.find(self.collection, {"user_id": user_id})
        if not existing:
            user_data = {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "subscriptions": []
            }
            return self.mongo.insert(self.collection, user_data)
        return None

    def get_user(self, user_id: int):
        """Retrieve user info from MongoDB."""
        return self.mongo.find(self.collection, {"user_id": user_id})

    def update_user(self, user_id: int, update_data: dict):
        """Update user info in MongoDB."""
        return self.mongo.update(self.collection, {"user_id": user_id}, {"$set": update_data})

    def add_subscription(self, user_id: int, event: str):
        """Add an event subscription for a user."""
        return self.mongo.update(
            self.collection,
            {"user_id": user_id},
            {"$addToSet": {"subscriptions": event}}
        )

    def remove_subscription(self, user_id: int, event: str):
        """Remove an event subscription for a user."""
        return self.mongo.update(
            self.collection,
            {"user_id": user_id},
            {"$pull": {"subscriptions": event}}
        )

    def list_subscriptions(self, user_id: int):
        """List all subscriptions of a user."""
        user = self.mongo.find(self.collection, {"user_id": user_id})
        for u in user:
            return u.get("subscriptions", [])
        return []
