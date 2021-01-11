"""Cluster Entity"""
import dataclasses


@dataclasses.dataclass
class Cluster:
    """Entity representing a Server Cluster"""

    id: int
    name: str
    type: str

    def __repr__(self) -> str:
        """Overide __repr__"""
        return f"Cluster(id={self.id}, name={self.name}, type={self.type})"

    @classmethod
    def from_dict(cls, d):
        """Initialise an Object from a dictionary of parameters

        Parameters:
        d {dict}: dictionary representing the objects parameters

        Returns:
        {Cluster}
        """
        return cls(**d)

    def to_dict(self):
        """Return a dict representing a cluster object"""
        return dataclasses.asdict(self)
