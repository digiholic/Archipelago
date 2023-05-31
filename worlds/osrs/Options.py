from Options import Choice, Range, Toggle, DefaultOnToggle

class Goal(Choice):
    display_name = "Goal"
    option_jad = "Fight Caves"
    option_zuk = "Inferno"
    option_cox = "Chambers of Xeric"
    option_tob = "Theatre of Blood"
    option_toa = "Tombs of Amascut"
    option_bounty = "Hit List"

class WildernessBosses(Choice):
    """
    Whether to include Wilderness Bosses as Location checks.
    None - No wilderness bosses
    Demibosses only - Crazy Archaeologist, Chaos Fanatic, and Scorpia
    Lesser Bosses - Above plus Spindel, Calvar'ion, Artio, and Chaos Elemental
    All - Above plus Callisto, Venenatis, and Vet'ion
    """
    display_name = "Include Wildnerness Bosses"
    option_none = "None"
    option_demi = "Demibosses only"
    option_lesser = "Lesser Bosses"
    option_full = "All"


class SlayerBosses(Toggle):
    """
    Whether to include the bosses that can only be killed on Slayer Task as Location Checks.
    These bosses are Grotesque Guardians, Abyssal Sire, Kraken, Cerberus,
    Thermonuclear Smoke Devil, and Alchemical Hydra
    """
    display_name = "Slayer Bosses"


class KeyBosses(DefaultOnToggle):
    """
    Whether to include bosses that require keys to attempt as Location Checks.
    These bosses are Obor, Bryophyta, and Skotizo
    """
    display_name = "Keyed Bosses"

class Hespori(DefaultOnToggle):
    """
    Whether to include The Hespori as a Location Check.
    """
    display_name = "Hespori"


OSRSOptions = {
    "wilderness_bosses": WildernessBosses
}