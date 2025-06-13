from . import OSRSTestBase


class BasicTests(OSRSTestBase):
    def test_camdozaal_not_sphere_one(self) -> None:
        assert not self.can_reach_location("(Camdozaal) Obtain a ~|barronite handle|~")
    
    def test_lumbridge_diary_not_in_logic(self)-> None:
        print(self.multiworld.get_location("~|Lumbridge and Draynor Diary#Elite|~ Task 6",self.player).access_rule.__self__.explain(self.multiworld.get_all_state(False)))
        assert self.multiworld.get_all_state(False).can_reach_location("~|Lumbridge and Draynor Diary#Elite|~ Task 6",self.player)
    
    def test_sweeps(self)->None:
        self.multiworld.state.sweep_for_advancements()
        state = self.multiworld.get_all_state(False)
        state.sweep_for_advancements()