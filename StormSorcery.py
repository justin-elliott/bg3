
from functools import cached_property
import os

from moddb import Bolster, spells_always_prepared
from modtools.gamedata import PassiveData
from modtools.lsx.game import ClassDescription, Progression, SpellList
from modtools.replacers import (
    CharacterClass,
    class_description,
    DontIncludeProgression,
    progression,
    Replacer,
)


class StormSorcery(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="StormSorcery",
                         description="A class replacer for StormSorcery.",
                         **kwds)

    @cached_property
    def _bolster(self) -> str:
        return Bolster(self.mod).add_bolster()

    @cached_property
    def _electrostatic_generator(self) -> str:
        name = f"{self.mod.get_prefix()}_ElectrostaticGenerator"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Electrostatic Generator"}
        loca[f"{name}_Description"] = {"en": """
            Every turn while in combat, you generate [1]
            <LSTag Type="Status" Tooltip="MAG_CHARGED_LIGHTNING">Lightning Charges</LSTag>.
        """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=["2"],
            Icon="statIcons_LightningCharge",
            Properties=["Highlighted", "OncePerTurn"],
            StatsFunctorContext=["OnTurn"],
            Conditions=["Combat()"],
            StatsFunctors=[
                "IF(not HasStatus('MAG_CHARGED_LIGHTNING',context.Source)):" +
                    "ApplyStatus(SELF,MAG_CHARGED_LIGHTNING_LIGHTNING_DAMAGE_ONCE_TECHNICAL,100,0)",
                "ApplyStatus(MAG_CHARGED_LIGHTNING_GENERATE_CHARGE_FX,100,0)",
                "IF(not IsDischargingLightning(context.Source)):ApplyStatus(MAG_CHARGED_LIGHTNING,100,2)",
                "ApplyStatus(MAG_CHARGED_LIGHTNING_DURATION_TECHNICAL,100,1)",
            ],
        ))

        return name

    @cached_property
    def _wintry_mix(self) -> str:
        name = f"{self.mod.get_prefix()}_WintryMix"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Wintry Mix"}
        loca[f"{name}_Description"] = {"en": """
            When you deal Cold damage, you inflict [1] turns of <LSTag Type="Status" Tooltip="WET">Wet</LSTag> on the
            target.
        """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=["3"],
            Icon="Spell_Conjuration_SleetStorm",
            Properties=["Highlighted"],
            StatsFunctorContext=["OnDamage"],
            Conditions=["IsDamageTypeCold()"],
            StatsFunctors=["ApplyStatus(WET,100,3)"],
        ))

        return name

    @cached_property
    def _spelllist_level_1(self) -> str:
        name = f"{self.mod.get_prefix()} level 1 spells"
        uuid = self.make_uuid(name)
        self.mod.add(SpellList(
            Name=name,
            Spells=[
                "Shout_ArmorOfAgathys",
                self._bolster,
                "Projectile_RayOfFrost",
                "Target_ShockingGrasp",
            ],
            UUID=uuid,
        ))
        return uuid

    @class_description(CharacterClass.SORCERER)
    @class_description(CharacterClass.SORCERER_DRACONIC)
    @class_description(CharacterClass.SORCERER_SHADOWMAGIC)
    @class_description(CharacterClass.SORCERER_STORM)
    @class_description(CharacterClass.SORCERER_WILDMAGIC)
    def sorcerer_can_learn_spells(self, description: ClassDescription) -> None:
        description.CanLearnSpells = True
        description.MustPrepareSpells = True

    @progression(CharacterClass.SORCERER, range(1, 21))
    @progression(CharacterClass.SORCERER, 1, is_multiclass=True)
    @progression(CharacterClass.SORCERER_DRACONIC, range(1, 21))
    @progression(CharacterClass.SORCERER_SHADOWMAGIC, range(1, 21))
    @progression(CharacterClass.SORCERER_STORM, range(1, 21))
    @progression(CharacterClass.SORCERER_WILDMAGIC, range(1, 21))
    def sorcerer_spells_always_prepared(self, progression: Progression) -> None:
        if not spells_always_prepared(progression):
            raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 1)
    def stormsorcery_level_1(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._electrostatic_generator, self._wintry_mix]
        progress.Selectors = [
            f"AddSpells({self._spelllist_level_1},,,,AlwaysPrepared)",
            "AddSpells(12150e11-267a-4ecc-a3cc-292c9e2a198d,,,,AlwaysPrepared)",  # Fly
        ]

    @progression(CharacterClass.SORCERER_STORM, 2)
    def stormsorcery_level_2(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 3)
    def stormsorcery_level_3(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 4)
    def stormsorcery_level_4(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 5)
    def stormsorcery_level_5(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 6)
    def stormsorcery_level_6(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 7)
    def stormsorcery_level_7(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 8)
    def stormsorcery_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 9)
    def stormsorcery_level_9(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 10)
    def stormsorcery_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 11)
    def stormsorcery_level_11(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 12)
    def stormsorcery_level_12(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 13)
    def stormsorcery_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 14)
    def stormsorcery_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 15)
    def stormsorcery_level_15(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 16)
    def stormsorcery_level_16(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 17)
    def stormsorcery_level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 18)
    def stormsorcery_level_18(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 19)
    def stormsorcery_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 20)
    def stormsorcery_level_20(self, _: Progression) -> None:
        raise DontIncludeProgression()


def main() -> None:
    storm_sorcery = StormSorcery(
        classes=[CharacterClass.SORCERER_STORM],
        feats=2,
        spells=2,
        warlock_spells=2,
        actions=2,
    )
    storm_sorcery.build()


if __name__ == "__main__":
    main()
