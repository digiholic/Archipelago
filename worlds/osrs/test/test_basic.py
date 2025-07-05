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

    def test_should_be_able_to_train_smithing(self) -> None:
        self.collect_by_name("Area: Lumbridge Castle")
        self.assertFalse( self.can_reach_location("Smith a ~|bronze mace|~"))
        self.collect_by_name("Area: East Lumbridge Swamp")
        self.assertTrue(  self.can_reach_location("Smith a ~|bronze mace|~"))

    def test_weapon_poison_not_sphere_one(self)-> None:
        self.assertFalse(self.can_reach_region("Weapon poison(+)"))
    
    def test_can_reach_max_quest_levels(self)-> None:
        all_state = self.multiworld.get_all_state(False)
        def assert_min_training(self:OSRSTestBase,state:CollectionState,skill_name:str,min_level:int):
            from worlds.osrs import HasTraining
            world:OSRSWorld = self.multiworld.worlds[1]
            rule = world.parse_rule(RuleElement("skill",f"{skill_name}_{str(min_level)}"))
            if rule is not None:
                self.assertTrue(rule.resolve(world).test(state))
        assert_min_training(self,all_state,"Attack",50)
        assert_min_training(self,all_state,"Strength",60)
        assert_min_training(self,all_state,"Defence",65)
        assert_min_training(self,all_state,"Ranged",62)
        assert_min_training(self,all_state,"Prayer",50)
        assert_min_training(self,all_state,"Magic",75)
        assert_min_training(self,all_state,"Runecraft",60)
        assert_min_training(self,all_state,"Construction",70)
        assert_min_training(self,all_state,"Agility",70)
        assert_min_training(self,all_state,"Herblore",70)
        assert_min_training(self,all_state,"Thieving",72)
        assert_min_training(self,all_state,"Crafting",70)
        assert_min_training(self,all_state,"Fletching",60)
        assert_min_training(self,all_state,"Slayer",69)
        assert_min_training(self,all_state,"Hunter",70)
        assert_min_training(self,all_state,"Mining",72)
        assert_min_training(self,all_state,"Smithing",70)
        assert_min_training(self,all_state,"Fishing",62)
        assert_min_training(self,all_state,"Cooking",70)
        assert_min_training(self,all_state,"Firemaking",75)
        assert_min_training(self,all_state,"Woodcutting",71)
        assert_min_training(self,all_state,"Farming",70)
    
    def test_can_reach_max_levels(self)-> None:
        all_state = self.multiworld.get_all_state(False)
        world = self.multiworld.worlds[1]
        def assert_min_training(self:OSRSTestBase,state:CollectionState,skill_name:str,min_level:int):
            world:OSRSWorld = self.multiworld.worlds[1]
            rule = world.parse_rule(RuleElement("skill",f"{skill_name}_{str(min_level)}"))
            if rule is not None:
                self.assertTrue(rule.resolve(world).test(state))
        for skill in skill_names:
            with self.subTest(skill_name=skill):
                assert_min_training(self,all_state,skill,99)

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
    
    def test_sphere_one_size(self)->None:
        print([location for location in self.multiworld.get_locations(self.player) if location.can_reach(self.multiworld.state) and location.address is not None])
        self.collect_by_name("Area: Groats' Farm")
        self.collect_by_name("Area: Lumbridge Mill")
        self.collect_by_name("Area: Lumbridge Castle Backyard")
        print([location for location in self.multiworld.get_locations(self.player) if location.can_reach(self.multiworld.state) and location.address is not None])
        pass