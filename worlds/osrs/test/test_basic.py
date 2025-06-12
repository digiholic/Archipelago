from . import OSRSTestBase


class BasicTests(OSRSTestBase):
    def test_camdozaal_not_sphere_one(self) -> None:
        assert not self.can_reach_location("(Camdozaal) Obtain a ~|barronite handle|~")