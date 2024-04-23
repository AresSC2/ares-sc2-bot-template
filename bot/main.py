from typing import Optional

from ares import AresBot
from ares.consts import UnitRole, ALL_STRUCTURES
from ares.behaviors.combat import CombatManeuver
from ares.behaviors.combat.group import AMoveGroup

from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point2

class AnglerBot(AresBot):
    def __init__(self, game_step_override: Optional[int] = None):
        """Initiate custom bot

        Parameters
        ----------
        game_step_override :
            If proied elsewherevided, set the game_step to this value regardless of how it was
            specif
        """
        super().__init__(game_step_override)

        self._assigned_main_army: bool = False

    async def on_step(self, iteration: int) -> None:
        await super(AnglerBot, self).on_step(iteration)
        #retrieve all attacking units
        attackers: Units = self.mediator.get_units_by_role(UnitRole.ATTACKING)
    
        #retrieve main army if one has been assigned
        main_army: Units = self.mediator.get_units_by_role(role=UnitRole.MAIN_ARMY, unit_type=UnitTypeId.ZEALOT)
        print("Main Army assigned")
    
        self.control_main_army(
            main_army=main_army,
            target=self.enemy_start_locations[0]
        )

        # at 10 seconds assign all zealots to MAIN_ARMY role
        # This will remove them from the ATTACKING automatically
        if not self._assigned_main_army and self.time > 2:
            self._assigned_main_army = True
            zealots: list[Unit] = [
                u for u in attackers if u.type_id == UnitTypeId.ZEALOT
            ]
            for zealot in zealots:
                self.mediator.assign_role(tag=zealot.tag, role=UnitRole.MAIN_ARMY
                )
    def control_main_army(self, main_army: Units, target: Point2) -> None:
        #declare a new group maneuver
        group_maneuver: CombatManeuver = CombatManeuver()
        #add group behaviors
        group_maneuver.add(
            AMoveGroup(
                group= main_army,
                group_tags={r.tag for r in main_army},
                target=target
            )
        )
        self.register_behavior(group_maneuver)

    async def on_start(self, unit: Unit) -> None:
        #When a unit is created,
        #assign it to ATTACKING role
        await super(AnglerBot, self).on_start(unit)
        type_id: UnitTypeId = unit.type_id
        # don't assign structures
        if type_id in ALL_STRUCTURES:
            return
        
        #assign all other units to ATTACKING role by default
        self.mediator.assign_role(tag=unit.tag, role=UnitRole.ATTACKING)
        print("Unit assigned to ATTACKING role")

    
    """
    Can use `python-sc2` hooks as usual, but make a call the inherited method in the superclass
    Examples:
    """
    # async def on_start(self) -> None:
    #     await super(MyBot, self).on_start()
    #
    #     # on_start logic here ...
    #
    # async def on_end(self, game_result: Result) -> None:
    #     await super(MyBot, self).on_end(game_result)
    #
    #     # custom on_end logic here ...
    #
    # async def on_building_construction_complete(self, unit: Unit) -> None:
    #     await super(MyBot, self).on_building_construction_complete(unit)
    #
    #     # custom on_building_construction_complete logic here ...
    #
    # async def on_unit_created(self, unit: Unit) -> None:
    #     await super(MyBot, self).on_unit_created(unit)
    #
    #     # custom on_unit_created logic here ...
    #
    # async def on_unit_destroyed(self, unit_tag: int) -> None:
    #     await super(MyBot, self).on_unit_destroyed(unit_tag)
    #
    #     # custom on_unit_destroyed logic here ...
    #
    # async def on_unit_took_damage(self, unit: Unit, amount_damage_taken: float) -> None:
    #     await super(MyBot, self).on_unit_took_damage(unit, amount_damage_taken)
    #
    #     # custom on_unit_took_damage logic here ...
