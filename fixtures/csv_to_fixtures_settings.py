
FIXTURES_AFFILIATIONS = {
    "category.csv": "categories.Category",
    "location.csv": "locations.Location",
    "user.csv": "users.User",
    "ad.csv": "ads.Ad",
}

MANY_TO_MANY_FIELDS = {
    "user.csv": {
        "location_id": "locations",
    }
}
