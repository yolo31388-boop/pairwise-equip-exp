"""装备经验与升级系统"""
from dataclasses import dataclass, field

BREAKTHROUGH_LEVELS = (30, 50, 70, 90)
TRANSFER_RATE = 0.8

BREAKTHROUGH_SKILLS = {
    30: "觉醒·利刃",
    50: "觉醒·破甲",
    70: "觉醒·嗜血",
    90: "觉醒·神威",
}

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
        # 按怪物等级与玩家等级差计算，高级怪给更多经验
        base = 10
        diff = monster_level - player_level
        multiplier = max(0.1, 1.0 + diff * 0.05)
        return max(1, int(base * monster_level * multiplier / 10))

    def get_exp_required(self, level: int) -> int:
        # 指数递增，高级别升级更慢
        return int(100 * (1.1 ** (level - 1)))

    def needs_breakthrough(self, level: int) -> bool:
        # 关键等级需要突破材料和突破任务
        return level in BREAKTHROUGH_LEVELS

    def transfer_exp(self, source: Equipment, target: Equipment) -> int:
        # 经验按比例转移，有转移损耗
        transferred = int(source.exp * TRANSFER_RATE)
        source.exp -= transferred
        target.exp += transferred
        return transferred

    def get_breakthrough_skill(self, level: int) -> str:
        # 关键等级解锁专属词条和技能
        return BREAKTHROUGH_SKILLS.get(level, "")

    def is_exp_maxed(self, equip: Equipment) -> bool:
        return equip.exp >= equip.exp_to_next

    def get_max_notification(self, equip: Equipment) -> str:
        # 经验满时明确提示，自动停止获取
        if self.is_exp_maxed(equip):
            return f"装备[{equip.name}]经验已满({equip.exp}/{equip.exp_to_next})，请升级或突破，不再获取经验"
        return ""
