
FIXTURES_AFFILIATIONS = {
    "category.csv": "ads.Category",
    "location.csv": "ads.Location",
    "user.csv": "ads.User",
    "ad.csv": "ads.Ad",
}

MANY_TO_MANY_FIELDS = {
    "user.csv": {
        "location_id": "locations",
    }
}
