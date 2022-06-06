from minirpg.characters import Player, Enemy
from minirpg.rpg import Combat

player = Player(name="Karol", player_class="TEST")
enemy = Enemy(name="CrazyGoblin")
combat = Combat(player, enemy)
combat.print_info()
combat.player_attack()
