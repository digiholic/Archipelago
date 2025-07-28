from . import OSRSTestBase
from rule_builder import *
from worlds.osrs import *
import unittest
from ..Options import MaxDropRate, FullMaxDropRate, DisableCulling
from ..LogicCSV.regions_generated2 import location_rows, sub_quests, region_rows, resource_rows, monster_drops

class FullTests(OSRSTestBase):
    run_default_tests = False  # type: ignore
    options = {
        "max_drop_rate": MaxDropRate.range_end,
        "full_drop_rate": FullMaxDropRate.range_end,
        "disable_culling": True
    }

    def test_creates_all_regions(self)->None:
        all_state = self.multiworld.get_all_state(False)
        region_cache = self.multiworld.regions.region_cache[1]
        for region_row in region_rows:
            assert isinstance(region_row,RegionRow)
            with self.subTest(region_name=region_row.id):
                self.assertIn(region_row.id,region_cache,f"Region {region_row.id} was not created")
                self.assertTrue(all_state.can_reach_region(region_row.id,1),f"Cannot reach region {region_row.id}")
        for region_row in resource_rows:
            assert isinstance(region_row,ResourceRow)
            with self.subTest(region_name=region_row.name):
                self.assertIn(region_row.name,region_cache,f"Resource {region_row.name} was not created")
                self.assertTrue(all_state.can_reach_region(region_row.name,1),f"Cannot reach resource {region_row.name}")
        for region_row in monster_drops:
            assert isinstance(region_row,MonsterRow)
            with self.subTest(region_name=region_row.name):
                self.assertIn(region_row.name,region_cache,f"Drop table {region_row.name} was not created")
                self.assertTrue(all_state.can_reach_region(region_row.name,1),f"Cannot reach drop table {region_row.name}")
    
    def test_creates_all_sub_quests(self)->None:
        all_state = self.multiworld.get_all_state(False)
        location_cache = self.multiworld.regions.location_cache[1]
        for sub_quest in sub_quests:
            assert isinstance(sub_quest,LocationRow)
            with self.subTest(sub_quest_name=sub_quest.name):
                self.assertIn(sub_quest.name,location_cache,f"Sub Quest step {sub_quest.name} was not created")
                self.assertTrue(all_state.can_reach_location(sub_quest.name,1),f"Sub Quest step {sub_quest.name} is not reachable")

    def test_creates_all_locations(self)->None:
        all_state = self.multiworld.get_all_state(False)
        location_cache = self.multiworld.regions.location_cache[1]
        for location_row in location_rows:
            assert isinstance(location_row,LocationRow)
            with self.subTest(location_name=location_row.name):
                self.assertIn(location_row.name,location_cache,f"Location {location_row.name} was not created")
                self.assertTrue(all_state.can_reach_location(location_row.name,1),f"Location {location_row.name} is not reachable")

    def test_camdozaal_not_sphere_one(self) -> None:
        self.assertFalse( self.can_reach_location("(Camdozaal) Obtain a ~|barronite handle|~"))
        self.assertTrue(self.multiworld.get_all_state(False).can_reach_location("(Camdozaal) Obtain a ~|barronite handle|~",self.player))

    def test_ardougne_cloak_not_sphere_one(self) -> None:
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
                self.assertTrue(rule.resolve(world)(state))
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
                self.assertTrue(rule.resolve(world)(state))
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
        self.assertTrue(world.resolve_rule(rule_a)(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule_b)(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule_c)(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule_d)(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule_e)(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule0)(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule2)(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule3)(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule4)(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule5)(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule6)(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule7)(all_state)) #passes
        self.assertTrue(world.resolve_rule(rule1)(all_state))  #fails
            
    
    def test_lumbridge_diary_not_in_logic(self)-> None:
        self.assertTrue(self.multiworld.get_all_state(False).can_reach_location("~|Lumbridge and Draynor Diary#Elite|~ Task 6",self.player))
