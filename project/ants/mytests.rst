This file holds the tests that you create. Remember to import the python file(s)
you wish to test, along with any other modules you may need.
Run your tests with "python3 ok -t --suite SUITE_NAME --case CASE_NAME -v"
--------------------------------------------------------------------------------

Suite 1
    case 1
    >>> from ants import *
    >>> hive,layout= Hive(make_test_assault_plan()),dry_layout
    >>> dimensions = (1,9)
    >>> colony = AntColony(None, hive, ant_types(), dry_layout, dimensions)


        >>> # Testing ant in place is bodyguard and ant contained is throwerant 
        >>> bodyguard = BodyguardAnt()
        >>> thrower = ThrowerAnt()
        >>> bee = Bee(2)
        >>> # Place bodyguard before thrower
        >>> colony.places["tunnel_0_0"].add_insect(bodyguard)
        >>> colony.places["tunnel_0_0"].add_insect(thrower)
        >>> colony.places["tunnel_0_3"].add_insect(bee)
        >>> colony.places["tunnel_0_0"].ant
        BodyguardAnt(2, tunnel_0_0)
        >>> colony.places["tunnel_0_0"].ant.ant
        ThrowerAnt(1, tunnel_0_0)
        >>> bodyguard.action(colony)
        >>> bee.armor
        1

Suite 2
    >>> from ants import *
    >>> hive,layout= Hive(make_test_assault_plan()),dry_layout
    >>> dimensions = (1,9)
    >>> colony = AntColony(None, hive, ant_types(), dry_layout, dimensions)
    
          >>> # Testing bodyguard performs thrower's action
          >>> bodyguard = BodyguardAnt()
          >>> thrower = ThrowerAnt()
          >>> bee = Bee(2)
          >>> # Place thrower before bodyguard
          >>> colony.places["tunnel_0_0"].add_insect(thrower)
          >>> colony.places["tunnel_0_0"].add_insect(bodyguard)
          >>> colony.places["tunnel_0_3"].add_insect(bee)
          >>> colony.places["tunnel_0_0"].ant
          BodyguardAnt(2, tunnel_0_0)
          >>> colony.places["tunnel_0_0"].ant.ant
          ThrowerAnt(1, tunnel_0_0)

Suite 11
      >>> import ants, importlib
      >>> importlib.reload(ants)
      >>> hive = ants.Hive(ants.AssaultPlan()
        >>> dimensions = (1,9)
        >>> colony = AntColony(None, hive, ant_types(), layout, dimensions)
    
    >>> # Testing water with Ants
    >>> test_ant1 = HarvesterAnt()
    >>> test_ant2 = ThrowerAnt()
    >>> test_bee = Bee(10)
    >>> test_bee.watersafe = False
    >>> test_water = Water('Water Test1')
    >>> test_water.add_insect(test_ant1)
    >>> test_water.add_insect(test_ant2)
        >>> test_water.add_insect(test_bee)
    >>> test_ant2.armor
    0
    >>> test_ant1.armor
    0
    >>> test_water.ant
    
    >>> test_water.bees
    []

>>> # Testing water inheritance
>>> def new_add_insect(self, insect):
...     raise NotImplementedError()

>>> Place.add_insect = new_add_insect
>>> test_bee = Bee(1)
>>> test_water = Water('Water Test4')
>>> passed = False
>>> try:
...     test_water.add_insect(test_bee)
... except NotImplementedError:
...     passed = True

>>> passed
True

Suite 13
>>> import ants, importlib
>>> hive = ants.Hive(ants.AssaultPlan())
>>> dimensions = (2, 9)
>>> colony = ants.AntColony(None, hive, ants.ant_types(), ants.dry_layout, dimensions)
>>> # QueenAnt Placement
>>> queen = ants.QueenAnt()
>>> impostor = ants.QueenAnt()
>>> front_ant, back_ant = ants.ThrowerAnt(), ants.ThrowerAnt()
>>> tunnel = [colony.places['tunnel_0_{0}'.format(i)] for i in range(9)]
>>> tunnel[1].add_insect(back_ant)
>>> tunnel[7].add_insect(front_ant)
>>> tunnel[4].add_insect(impostor)
>>> impostor.action(colony)
>>> impostor.armor            # Impostors must die!
0
>>> tunnel[4].ant is None
True
>>> back_ant.damage           # Ants should not be buffed
1
>>> front_ant.damage
1
>>> tunnel[4].add_insect(queen)
>>> queen.action(colony)
>>> queen.armor               # Long live the Queen!
1
>>> back_ant.damage           # Ants behind queen should be buffed
2
>>> front_ant.damage
1

Suite 14
>>> import ants, importlib
>>> hive = ants.Hive(ants.AssaultPlan())
>>> dimensions = (2, 9)
>>> colony = ants.AntColony(None, hive, ants.ant_types(), ants.dry_layout, dimensions)
>>> # QueenAnt Removal
>>> queen = ants.QueenAnt()
>>> impostor = ants.QueenAnt()
>>> place = colony.places["tunnel_0_2"]
>>> place.add_insect(impostor)
>>> place.remove_insect(impostor)
>>> place.ant is impostor
False
>>> place.add_insect(queen)
>>> place.ant is queen
True
>>> place.remove_insect(queen)
>>> place.ant is queen
True

Suite 15
>>> import ants, importlib
>>> hive = ants.Hive(ants.AssaultPlan())
>>> dimensions = (2, 9)
>>> colony = ants.AntColony(None, hive, ants.ant_types(), ants.dry_layout, dimensions)
>>> # Extensive damage doubling tests
>>> queen_tunnel, side_tunnel = [[colony.places['tunnel_{0}_{1}'.format(i, j)] for j in range(9)] for i in range(2)]
>>> queen = ants.QueenAnt()
>>> queen_tunnel[7].add_insect(queen)
>>> queen
QueenAnt(1, tunnel_0_7)
>>> queen.place.exit is False
False
>>> # Turn 0
>>> thrower = ants.ThrowerAnt()
>>> fire = ants.FireAnt()
>>> ninja = ants.NinjaAnt()
>>> side = ants.ThrowerAnt()
>>> front = ants.NinjaAnt()
>>> queen_tunnel[0].add_insect(thrower)
>>> queen_tunnel[1].add_insect(fire)
>>> queen_tunnel[2].add_insect(ninja)
>>> queen_tunnel[8].add_insect(front)
>>> side_tunnel[0].add_insect(side)
>>> buffed_ants = [thrower, fire, ninja]
>>> old_dmgs = [ant.damage for ant in buffed_ants]
>>> queen
QueenAnt(1, tunnel_0_7)
>>> queen.action(colony)
>>> for ant, dmg in zip(buffed_ants, old_dmgs):
...     assert ant.damage == dmg * 2, "{0}'s damage is {1}, but should be {2}".format(ant, ant.damage, dmg * 2)
>>> for ant in [side, front]:
...     assert ant.damage == dmg,\
...         "{0}'s damage is {1}, but should be {2}".format(ant, ant.damage, dmg)
>>> assert queen.damage == 1,\
...     'QueenAnt damage was modified to {0}'.format(ant.damage)
>>> queen.ants_double
[NinjaAnt(1, tunnel_0_2), FireAnt(1, tunnel_0_1), ThrowerAnt(1, tunnel_0_0)]
>>> queen
QueenAnt(1, tunnel_0_7)
>>> # Turn 1
>>> tank = ants.TankAnt()
>>> guard = ants.BodyguardAnt()
>>> queen_tank = ants.TankAnt()
>>> queen_tunnel[6].add_insect(tank)          # Not protecting an ant
>>> queen_tunnel[1].add_insect(guard)         # Guarding FireAnt
>>> queen_tunnel[7].add_insect(queen_tank)    # Guarding QueenAnt
>>> buffed_ants.extend([tank, guard])
>>> old_dmgs.extend([ant.damage for ant in [tank, guard, queen_tank]])
>>> queen.action(colony)
>>> queen.queen
True
>>> queen
QueenAnt(1, tunnel_0_7)
>>> queen.place.exit is True
False
>>> queen.place.exit.ant
TankAnt(2, tunnel_0_6)
>>> queen.ants_double
[NinjaAnt(1, tunnel_0_2), FireAnt(1, tunnel_0_1), ThrowerAnt(1, tunnel_0_0), TankAnt(2, tunnel_0_6), BodyguardAnt(2, tunnel_0_1)]
>>> tank.damage
2
>>> guard.damage
0
>>> queen_tank.damage
1
>>> thrower.damage
2
>>> for ant, dmg in zip(buffed_ants, old_dmgs):
...     assert ant.damage == dmg * 2, "{0}'s damage is {1}, but should be {2}".format(ant, ant.damage, dmg * 2)

>>> # Turn 2
>>> thrower1 = ants.ThrowerAnt()
>>> thrower2 = ants.ThrowerAnt()
>>> queen_tunnel[6].add_insect(thrower1)      # Add thrower1 in TankAnt
>>> queen_tunnel[5].add_insect(thrower2)
>>> buffed_ants.extend([thrower1, thrower2])
>>> old_dmgs.extend([ant.damage for ant in [thrower1, thrower2]])
>>> queen.action(colony)
>>> thrower1.damage
2
>>> thrower2.damage
2
>>> for ant, dmg in zip(buffed_ants, old_dmgs):
...     assert ant.damage == dmg * 2,\
...         "{0}'s damage is {1}, but should be {2}".format(ant, ant.damage, dmg * 2)

>>> # Turn 3
>>> tank.reduce_armor(tank.armor)             # Expose thrower1
>>> queen.action(colony)
>>> thrower1.damage
2
>>> for ant, dmg in zip(buffed_ants, old_dmgs):
...     assert ant.damage == dmg * 2,\
...         "{0}'s damage is {1}, but should be {2}".format(ant, ant.damage, dmg * 2)