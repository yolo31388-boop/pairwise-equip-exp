"""装备经验与升级系统 - 含6个bug"""
from dataclasses import dataclass, field

@dataclass
class Equipment:
    eid: str
    name: str
    level: int = 1
    exp: int = 0
    exp_to_next: int = 100
    max_level: int = 100
    breakthrough_materials: dict = field(default_factory=dict)
    unique_skill: str = ""

class EquipExp:
    def __init__(self):
        self.equipment: dict[str, Equipment] = {}

    def get_exp_from_kill(self, monster_level: int, player_level: int) -> int:
        # bug1: 只看击杀数
        return 10

    def get_exp_required(self, level: int) -> int:
        # bug2: 线性
        return 100

    def needs_breakthrough(self, level: int) -> bool:
        # bug3: 不需要突破
        return False

    def transfer_exp(self, source: Equipment, target: Equipment) -> int:
        # bug4: 不能转移
        return 0

    def get_breakthrough_skill(self, level: int) -> str:
        # bug5: 无质变技能
        return ""

    def is_exp_maxed(self, equip: Equipment) -> bool:
        # bug6: 不提示
        return equip.exp >= equip.exp_to_next
