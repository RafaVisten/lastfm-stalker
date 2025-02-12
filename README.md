# Last.fm Stalker
Extremely simple app made using [Flask](https://github.com/pallets/flask) and the [pylast](https://github.com/pylast/pylast) python library for checking what people are currently listening to.

Does the same thing [this website](https://jakeledoux.com/live/) does except it takes a manual list of users instead of your friendlist, so no login is needed.

If you want to run it locally, generate your own Last.fm API key / secret and create a .env file insde the project like so:
```
LASTFM_API_KEY="yourkeyhere"
LASTFM_API_SECRET="yoursecrethere"
```
