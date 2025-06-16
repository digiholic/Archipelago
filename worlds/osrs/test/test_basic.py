from . import OSRSTestBase
from rule_builder import *
from worlds.osrs import *


class BasicTests(OSRSTestBase):
    def test_camdozaal_not_sphere_one(self) -> None:
        self.assertFalse( self.can_reach_location("(Camdozaal) Obtain a ~|barronite handle|~"))
        self.assertTrue(self.multiworld.get_all_state(False).can_reach_location("(Camdozaal) Obtain a ~|barronite handle|~",self.player))

    def test_ardougne_cloak_not_sphere_one(self) -> None:
        print(self.multiworld.get_location("~|Ardougne Diary#Easy|~ Complete the Easy Diary",self.player).access_rule.__self__.explain_str(self.multiworld.get_all_state(False)))
        self.assertFalse( self.can_reach_location("~|Ardougne Diary#Easy|~ Complete the Easy Diary"))
        self.assertTrue(self.multiworld.get_all_state(False).can_reach_location("~|Ardougne Diary#Easy|~ Complete the Easy Diary",self.player))

    def test_state_doodles(self) -> None:
        all_state = self.multiworld.get_all_state(False)
        all_state.sweep_for_advancements()
        world:OSRSWorld = self.multiworld.worlds[1]
        rule_a = Has('~|Plague City|~ 1')
        rule_b = CanReachRegion('Dwellberries')
        rule_c = CanReachRegion('Alrena')
        rule_d = Has('Area: Chaos Druid Tower')
        rule_e = Has('~|Rune Mysteries|~ 1')
        rule1 = And(rule_a,rule_b)
        rule2 = And(rule_b,rule_c)
        rule3 = And(rule_a,rule_d)
        rule4 = And(rule_a,rule_c)
        rule5 = And(rule_b,rule_d)
        rule6 = And(rule_c,rule_d)
        rule7 = And(rule_e, rule_b)
        rule0 = Or(rule_a,rule_b)
        print(world.resolve_rule(rule0).explain_str(all_state))
        print(world.resolve_rule(rule1).explain_str(all_state))
        print(world.resolve_rule(rule3).explain_str(all_state))
        self.assertTrue(world.resolve_rule(rule_a).test(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule_b).test(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule_c).test(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule_d).test(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule_e).test(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule0).test(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule2).test(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule3).test(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule4).test(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule5).test(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule6).test(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule7).test(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule1).test(all_state))  #fails

    def test_state_doodles2(self) -> None:
        all_state = self.multiworld.get_all_state(False)
        all_state.sweep_for_advancements()
        world:OSRSWorld = self.multiworld.worlds[1]
        rule_a = Has('~|Plague City|~ 1')
        rule_b = CanReachRegion('Dwellberries')
        rule_e = Has('~|Rune Mysteries|~ 1')
        rule1 = rule_a & rule_b
        rule2 = rule_e & rule_b
        rule0 = rule_e | rule_b
        rrule_a = world.resolve_rule(rule_a)
        rrule_b = world.resolve_rule(rule_b)
        rrule_e = world.resolve_rule(rule_e)
        rrule0 = world.resolve_rule(rule0)
        rrule1 = world.resolve_rule(rule1)
        rrule2 = world.resolve_rule(rule2)
        print(rrule0.explain_str(all_state))
        print(rrule1.explain_str(all_state))
        print(rrule2.explain_str(all_state))
        self.assertTrue((rrule_a).test(all_state)) #passes
        self.assertTrue((rrule_b).test(all_state)) #passes
        self.assertTrue((rrule_e).test(all_state)) #passes
        self.assertTrue((rrule0).test(all_state)) #passes
        self.assertTrue((rrule2).test(all_state)) #passes
        self.assertTrue((rrule1).test(all_state))  #fails

    def test_find_the_shadow(self) -> None:
        all_state = self.multiworld.get_all_state(False)
        all_state.sweep_for_advancements()
        world:OSRSWorld = self.multiworld.worlds[1]
        failures = []
        rule_b = CanReachRegion('Dwellberries')
        for location_row in sub_quests:
            rule_a = Has(location_row.name)
            if world.resolve_rule(rule_a).test(all_state) and world.resolve_rule(rule_b).test(all_state) and not world.resolve_rule(And(rule_a,rule_b)).test(all_state):
                self.assertTrue(all_state.can_reach_region("Dwellberries",self.player) and all_state.has(location_row.name,self.player))
                failures.append(location_row.name)
        print(failures)
        self.assertEqual(len(failures),0)
            
    
    def test_lumbridge_diary_not_in_logic(self)-> None:
        print(self.multiworld.get_location("~|Lumbridge and Draynor Diary#Elite|~ Task 6",self.player).access_rule.__self__.explain_str(self.multiworld.get_all_state(False)))
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