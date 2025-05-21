
import os

from modtools.lsx.game import Dependencies, Progression
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)


class BladesingingExpanded(Replacer):
    def __init__(self):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="BladesingingExpanded",
                         description="A class replacer for BladesingingSchool.")

        self.mod.add(Dependencies.ShortModuleDesc(
            Folder="UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77",
            MD5="f94d034502139cf8b65a1597554e7236",
            Name="UnlockLevelCurve",
            PublishHandle=4166963,
            UUID="a2ffd0e4-c407-8642-2611-c934ea0b0a77",
            Version64=72057594037927960,
        ))

    @progression(CharacterClass.WIZARD, 1)
    def wizard_level_1(self, progression: Progression) -> None:
        progression.Boosts = [
            'ActionResource(SpellSlot,4,1)',
            'ProficiencyBonus(SavingThrow,Intelligence)',
            'ProficiencyBonus(SavingThrow,Wisdom)',
            'Proficiency(Daggers)',
            'Proficiency(Quarterstaffs)',
            'Proficiency(LightCrossbows)',
            'ActionResource(ArcaneRecoveryPoint,2,0)',
        ]
        progression.PassivesAdded = ['UnlockedSpellSlotLevel1']
        progression.Selectors = [
            'SelectSpells(3cae2e56-9871-4cef-bba6-96845ea765fa,3,0,,,,AlwaysPrepared)',
            'SelectSpells(11f331b0-e8b7-473b-9d1f-19e8e4178d7d,6,0)',
            'AddSpells(34c3321d-75ab-4b50-a44d-cbac8705a360,,,,AlwaysPrepared)',
            'SelectAbilityBonus(b9149c8e-52c8-46e5-9cb6-fc39301c05fe,AbilityBonus,2,1)',
            'SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)',
            'SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)',
        ]

    @progression(CharacterClass.WIZARD, 2)
    def wizard_level_2(self, progression: Progression) -> None:
        progression.AllowImprovement = True
        progression.Boosts = ['ActionResource(SpellSlot,2,1)']

    @progression(CharacterClass.WIZARD, 3)
    def wizard_level_3(self, progression: Progression) -> None:
        progression.Boosts = [
            'ActionResource(SpellSlot,2,1)',
            'ActionResource(SpellSlot,4,2)',
            'ActionResource(ArcaneRecoveryPoint,2,0)',
        ]
        progression.PassivesAdded = ['UnlockedSpellSlotLevel2']

    @progression(CharacterClass.WIZARD, 4)
    def wizard_level_4(self, progression: Progression) -> None:
        progression.AllowImprovement = True
        progression.Boosts = ['ActionResource(SpellSlot,2,2)']

    @progression(CharacterClass.WIZARD, 5)
    def wizard_level_5(self, progression: Progression) -> None:
        progression.Boosts = ['ActionResource(SpellSlot,4,3)', 'ActionResource(ArcaneRecoveryPoint,2,0)']
        progression.PassivesAdded = ['UnlockedSpellSlotLevel3']

    @progression(CharacterClass.WIZARD, 6)
    def wizard_level_6(self, progression: Progression) -> None:
        progression.AllowImprovement = True
        progression.Boosts = ['ActionResource(SpellSlot,2,3)']

    @progression(CharacterClass.WIZARD, 7)
    def wizard_level_7(self, progression: Progression) -> None:
        progression.Boosts = ['ActionResource(SpellSlot,2,4)', 'ActionResource(ArcaneRecoveryPoint,2,0)']

    @progression(CharacterClass.WIZARD, 8)
    def wizard_level_8(self, progression: Progression) -> None:
        progression.AllowImprovement = True
        progression.Boosts = ['ActionResource(SpellSlot,2,4)']

    @progression(CharacterClass.WIZARD, 9)
    def wizard_level_9(self, progression: Progression) -> None:
        progression.Boosts = [
            'ActionResource(SpellSlot,2,4)',
            'ActionResource(SpellSlot,2,5)',
            'ActionResource(ArcaneRecoveryPoint,2,0)',
        ]

    @progression(CharacterClass.WIZARD, 10)
    def wizard_level_10(self, progression: Progression) -> None:
        progression.AllowImprovement = True
        progression.Boosts = ['ActionResource(SpellSlot,2,5)']

    @progression(CharacterClass.WIZARD, 11)
    def wizard_level_11(self, progression: Progression) -> None:
        progression.Boosts = ['ActionResource(SpellSlot,2,6)', 'ActionResource(ArcaneRecoveryPoint,2,0)']

    @progression(CharacterClass.WIZARD, 12)
    def wizard_level_12(self, progression: Progression) -> None:
        progression.AllowImprovement = True

    @progression(CharacterClass.WIZARD, 13)
    def wizard_level_13(self, progression: Progression) -> None:
        progression.Boosts = ['ActionResource(SpellSlot,2,7)', 'ActionResource(ArcaneRecoveryPoint,2,0)']

    @progression(CharacterClass.WIZARD, 14)
    def wizard_level_14(self, progression: Progression) -> None:
        progression.AllowImprovement = True

    @progression(CharacterClass.WIZARD, 15)
    def wizard_level_15(self, progression: Progression) -> None:
        progression.Boosts = ['ActionResource(SpellSlot,2,8)', 'ActionResource(ArcaneRecoveryPoint,2,0)']

    @progression(CharacterClass.WIZARD, 16)
    def wizard_level_16(self, progression: Progression) -> None:
        progression.AllowImprovement = True

    @progression(CharacterClass.WIZARD, 17)
    def wizard_level_17(self, progression: Progression) -> None:
        progression.Boosts = ['ActionResource(SpellSlot,2,9)', 'ActionResource(ArcaneRecoveryPoint,2,0)']

    @progression(CharacterClass.WIZARD, 18)
    def wizard_level_18(self, progression: Progression) -> None:
        progression.AllowImprovement = True
        progression.Boosts = ['ActionResource(SpellSlot,2,5)']

    @progression(CharacterClass.WIZARD, 19)
    def wizard_level_19(self, progression: Progression) -> None:
        progression.AllowImprovement = True
        progression.Boosts = ['ActionResource(SpellSlot,2,6)', 'ActionResource(ArcaneRecoveryPoint,2,0)']

    @progression(CharacterClass.WIZARD, 20)
    def wizard_level_20(self, progression: Progression) -> None:
        progression.Boosts = ['ActionResource(SpellSlot,2,7)']
        progression.Selectors = [
            'SelectSpells(e52c4e1e-0476-47c0-843c-092c4b8506a7,2,0,SignatureSpells,,None,AlwaysPrepared,UntilRest)',
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 2)
    def wizard_bladesinging_level_2(self, progression: Progression) -> None:
        progression.Boosts = [
            'Proficiency(LightArmor)',
            'Proficiency(Daggers)',
            'Proficiency(Sickles)',
            'Proficiency(Shortswords)',
            'Proficiency(Rapiers)',
            'Proficiency(Scimitars)',
            'Proficiency(Longswords)',
            'ProficiencyBonus(Skill,Performance)',
            'ActionResource(Bladesong,4,0)',
        ]
        progression.PassivesAdded = [
            'TraininginWarandSong',
            'Bladesong_Armor_Message',
            'Bladesong_Weapon_Message',
            'Bladesong_Shield_Message',
            'Bladesong_Weapon',
            'Bladesong_Shield',
            'Bladesong_Unarmed',
        ]
        progression.Selectors = [
            'SelectEquipment(5309613d-e7cb-4176-95b6-0c8b796d47d0,1,WarAndSong)',
            'AddSpells(e97297e2-5cc9-45c9-ae8d-5a24257dd176,,,,AlwaysPrepared)',
            'SelectSpells(11f331b0-e8b7-473b-9d1f-19e8e4178d7d,2,0)',
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 3)
    def wizard_bladesinging_level_3(self, progression: Progression) -> None:
        progression.Selectors = ['SelectSpells(80c6b070-c3a6-4864-84ca-e78626784eb4,2,0)']

    @progression(CharacterClass.WIZARD_BLADESINGING, 4)
    def wizard_bladesinging_level_4(self, progression: Progression) -> None:
        progression.Selectors = [
            'SelectSpells(3cae2e56-9871-4cef-bba6-96845ea765fa,1,0,,,,AlwaysPrepared)',
            'SelectSpells(80c6b070-c3a6-4864-84ca-e78626784eb4,2,0)',
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 5)
    def wizard_bladesinging_level_5(self, progression: Progression) -> None:
        progression.Boosts = ['ActionResource(Bladesong,2,0)']
        progression.Selectors = ['SelectSpells(22755771-ca11-49f4-b772-13d8b8fecd93,2,0)']

    @progression(CharacterClass.WIZARD_BLADESINGING, 6)
    def wizard_bladesinging_level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = ['ExtraAttack']
        progression.Selectors = ['SelectSpells(22755771-ca11-49f4-b772-13d8b8fecd93,2,0)']

    @progression(CharacterClass.WIZARD_BLADESINGING, 7)
    def wizard_bladesinging_level_7(self, progression: Progression) -> None:
        progression.Selectors = ['SelectSpells(820b1220-0385-426d-ae15-458dc8a6f5c0,2,0)']

    @progression(CharacterClass.WIZARD_BLADESINGING, 8)
    def wizard_bladesinging_level_8(self, progression: Progression) -> None:
        progression.Selectors = ['SelectSpells(820b1220-0385-426d-ae15-458dc8a6f5c0,2,0)']

    @progression(CharacterClass.WIZARD_BLADESINGING, 9)
    def wizard_bladesinging_level_9(self, progression: Progression) -> None:
        progression.Boosts = ['ActionResource(Bladesong,2,0)']
        progression.Selectors = ['SelectSpells(f781a25e-d288-43b4-bf5d-3d8d98846687,2,0)']

    @progression(CharacterClass.WIZARD_BLADESINGING, 10)
    def wizard_bladesinging_level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = ['SongOfDefense']
        progression.Selectors = [
            'SelectSpells(3cae2e56-9871-4cef-bba6-96845ea765fa,1,0,,,,AlwaysPrepared)',
            'SelectSpells(f781a25e-d288-43b4-bf5d-3d8d98846687,2,0)',
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 11)
    def wizard_bladesinging_level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = ['SongOfDefense_6']
        progression.Selectors = ['SelectSpells(bc917f22-7f71-4a25-9a77-7d2f91a96a65,2,0)']

    @progression(CharacterClass.WIZARD_BLADESINGING, 12)
    def wizard_bladesinging_level_12(self, progression: Progression) -> None:
        progression.Selectors = ['SelectSpells(bc917f22-7f71-4a25-9a77-7d2f91a96a65,2,0)']

    @progression(CharacterClass.WIZARD_BLADESINGING, 13)
    def wizard_bladesinging_level_13(self, progression: Progression) -> None:
        progression.Selectors = ['SelectSpells(bc917f22-7f71-4a25-9a77-7d2f91a96a65,2,0)']

    @progression(CharacterClass.WIZARD_BLADESINGING, 14)
    def wizard_bladesinging_level_14(self, progression: Progression) -> None:
        progression.Selectors = ['SelectSpells(bc917f22-7f71-4a25-9a77-7d2f91a96a65,2,0)']

    @progression(CharacterClass.WIZARD_BLADESINGING, 15)
    def wizard_bladesinging_level_15(self, progression: Progression) -> None:
        progression.Selectors = ['SelectSpells(bc917f22-7f71-4a25-9a77-7d2f91a96a65,2,0)']

    @progression(CharacterClass.WIZARD_BLADESINGING, 16)
    def wizard_bladesinging_level_16(self, progression: Progression) -> None:
        progression.Selectors = ['SelectSpells(bc917f22-7f71-4a25-9a77-7d2f91a96a65,2,0)']

    @progression(CharacterClass.WIZARD_BLADESINGING, 17)
    def wizard_bladesinging_level_17(self, progression: Progression) -> None:
        progression.Selectors = ['SelectSpells(bc917f22-7f71-4a25-9a77-7d2f91a96a65,2,0)']

    @progression(CharacterClass.WIZARD_BLADESINGING, 18)
    def wizard_bladesinging_level_18(self, progression: Progression) -> None:
        progression.Selectors = ['SelectSpells(bc917f22-7f71-4a25-9a77-7d2f91a96a65,2,0)']

    @progression(CharacterClass.WIZARD_BLADESINGING, 19)
    def wizard_bladesinging_level_19(self, progression: Progression) -> None:
        progression.Selectors = ['SelectSpells(bc917f22-7f71-4a25-9a77-7d2f91a96a65,2,0)']

    @progression(CharacterClass.WIZARD_BLADESINGING, 20)
    def wizard_bladesinging_level_20(self, progression: Progression) -> None:
        progression.Selectors = ['SelectSpells(bc917f22-7f71-4a25-9a77-7d2f91a96a65,2,0)']


def main() -> None:
    bladesinging_expanded = BladesingingExpanded()
    bladesinging_expanded.build()


if __name__ == "__main__":
    main()
