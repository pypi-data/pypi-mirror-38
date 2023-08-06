# Client

## Creating a Client:
`client = brawlstars.Client(*args, **kwargs)`

| Argument | Description | Type |
|----------|-------------|------|
| token | The authorization header to be passed to access the API. | string |
| timeout* | How long to wait for response. | integer |

\*optional

## Client Attributes
| Variable | Description | Type |
|----------|-------------|------|
| \_base\_url* | Base URL to make requests to. | string |
| headers | Dictionary for headers to pass when making the request. Includes the token. | Dict |
| timeout | How long to wait for response. | integer |

\*immutable

## Client Methods
| Method | Description | Returns |
|--------|-------------|---------|
| get_band(tag) | Get information about a band with specified tag. | Band |
| get_player(tag) | Get information about a player with specified tag. | Player |
| get_player_leaderboard() | Get the leaderboard for players. | PlayerLeaderboard |
| get_band_leaderboard() | Get the leaderboard for bands. | BandLeaderboard |
