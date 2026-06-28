from dataclasses import dataclass


@dataclass
class Artist:
    ArtistId: int
    Name: str
    nTracce: int # aggiunto per fare il programma

    def __hash__(self):
        return hash(self.ArtistId)

    def __str__(self):
        return f"{self.Name} - {self.ArtistId}"
