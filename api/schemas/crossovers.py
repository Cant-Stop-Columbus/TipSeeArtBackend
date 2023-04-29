from api.schemas.artist import ArtistForUser
from api.schemas.user import UserSafe


class UserArtist(UserSafe):
    artist: ArtistForUser
