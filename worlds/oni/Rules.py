from BaseClasses import CollectionState
from worlds.oni import ItemNames


def can_advanced_research(player, state: CollectionState) -> bool:
    # Need to be able to actually do the research, and handle liquids and gas
    return state.has_all([ItemNames.AdvancedResearchCenter, ItemNames.BetaResearchPoint], player) and \
           can_manage_liquid(player, state) and can_manage_gas(player, state)


def can_nuclear_research(player, state: CollectionState) -> bool:
    # Need the material science terminal, and also be able to make refined metal
    return state.has_all([ItemNames.NuclearResearchCenter, ItemNames.DeltaResearchPoint], player) and \
           state.has_any([ItemNames.ManualHighEnergyParticleSpawner, ItemNames.HighEnergyParticleSpawner],
                         player) and can_refine_metal(player, state)


def can_space_research(player, state: CollectionState) -> bool:
    return state.has_all([ItemNames.DLC1CosmicResearchCenter,
                          ItemNames.OrbitalResearchPoint], player) and can_reach_space(player, state)


def can_reach_space(player, state: CollectionState) -> bool:
    # Launchpad is non-negotiable
    running_state = state.has_any([ItemNames.LaunchPad], player)
    # Has any engine and fuel tank
    running_state = running_state and state.has_any([], player)
    # Has any crew module
    running_state = running_state and state.has_any(
        [ItemNames.HabitatModuleSmall, ItemNames.HabitatModuleMedium], player)
    # Has any nosecone
    running_state = running_state and state.has_any(
        [ItemNames.NoseconeBasic, ItemNames.NoseconeHarvest, ItemNames.HabitatModuleSmall], player)
    return running_state


def can_ranch(player, state: CollectionState) -> bool:
    return state.has_all(
        [ItemNames.CreatureDeliveryPoint, ItemNames.CreatureFeeder, ItemNames.RanchStation], player)


def can_make_plastic(player, state: CollectionState) -> bool:
    # Either polymer press chain, or ranching dreckos
    return state.has_all([ItemNames.OilWellCap, ItemNames.OilRefinery, ItemNames.Polymerizer], player) or \
           (can_ranch(player, state) and state.has(ItemNames.ShearingStation, player))


def can_refine_metal(player, state: CollectionState) -> bool:
    # Crusher, Refinery, or Smooth Hatches
    return state.has_any([ItemNames.RockCrusher, ItemNames.MetalRefinery], player) or can_ranch(player, state)


def can_manage_liquid(player, state: CollectionState) -> bool:
    # Some form of liquid pump
    running_state = state.has(ItemNames.LiquidPump, player) or \
                    (state.has(ItemNames.LiquidMiniPump, player) and can_make_plastic(player, state))
    # Some form of liquid pipe
    running_state = running_state and (
            state.has_any([ItemNames.LiquidConduit, ItemNames.InsulatedLiquidConduit], player) or
            state.has(ItemNames.LiquidConduitRadiant, player) and can_refine_metal(player, state))
    # Liquid Vent
    running_state = running_state and state.has(ItemNames.LiquidVent, player)
    return running_state


def can_manage_gas(player, state: CollectionState) -> bool:
    # Some form of gas pump
    running_state = state.has(ItemNames.GasPump, player) or \
                    (state.has(ItemNames.GasMiniPump, player) and can_make_plastic(player, state))
    # Some form of gas pipe
    running_state = running_state and (state.has_any(
        [ItemNames.GasConduit, ItemNames.InsulatedGasConduit, ItemNames.GasConduitRadiant], player))
    # Some form of gas vent
    running_state = running_state and state.has(ItemNames.GasVent, player) or \
                    (state.has(ItemNames.GasVentHighPressure, player) and
                     can_make_plastic(player, state) and can_refine_metal(player, state))
    return running_state
