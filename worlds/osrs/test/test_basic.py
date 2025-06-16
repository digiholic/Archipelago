from . import OSRSTestBase


class BasicTests(OSRSTestBase):
    def test_camdozaal_not_sphere_one(self) -> None:
        self.assertFalse( self.can_reach_location("(Camdozaal) Obtain a ~|barronite handle|~"))
        self.assertTrue(self.multiworld.get_all_state(False).can_reach_location("(Camdozaal) Obtain a ~|barronite handle|~",self.player))

    def test_ardougne_cloak_not_sphere_one(self) -> None:
        print(self.multiworld.get_location("~|Ardougne Diary#Easy|~ Complete the Easy Diary",self.player).access_rule.__self__.explain(self.multiworld.get_all_state(False)))
        self.assertFalse( self.can_reach_location("~|Ardougne Diary#Easy|~ Complete the Easy Diary"))
        self.assertTrue(self.multiworld.get_all_state(False).can_reach_location("~|Ardougne Diary#Easy|~ Complete the Easy Diary",self.player))
    
    def test_lumbridge_diary_not_in_logic(self)-> None:
        print(self.multiworld.get_location("~|Lumbridge and Draynor Diary#Elite|~ Task 6",self.player).access_rule.__self__.explain(self.multiworld.get_all_state(False)))
        self.assertTrue(self.multiworld.get_all_state(False).can_reach_location("~|Lumbridge and Draynor Diary#Elite|~ Task 6",self.player))
    
    def test_sweeps(self)->None:
        self.multiworld.state.sweep_for_advancements()
        state = self.multiworld.get_all_state(False)
        state.sweep_for_advancements()
    
    def test_sphere_one_size(self)->None:
        print([location for location in self.multiworld.get_locations(self.player) if location.can_reach(self.multiworld.state) and location.address is not None])
        self.collect_by_name("Area: Groats' Farm")
        self.collect_by_name("Area: Lumbridge Mill")
        self.collect_by_name("Area: Lumbridge Castle Backyard")
        print([location for location in self.multiworld.get_locations(self.player) if location.can_reach(self.multiworld.state) and location.address is not None])
        pass