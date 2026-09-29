"""装备经验与升级系统"""
from dataclasses import dataclass, field

# 突破关键等级：到达这些等级需要突破材料与突破任务
BREAKTHROUGH_LEVELS = (20, 30, 50, 70, 90)

# 经验转移损耗比例（保留 80%）
TRANSFER_KEEP_RATIO = 0.8

# 各突破等级解锁的专属词条/技能
BREAKTHROUGH_SKILLS = {
    20: "锋芒初露",
    30: "破甲",
    50: "无双",
    70: "神威",
    90: "天人合一",
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
        # 经验按怪物等级与玩家等级差计算：高级怪给更多经验，
        # 低级怪经验衰减，最低保底 1 点
        base = 10
        diff = monster_level - player_level
        if diff >= 0:
            return base + monster_level + diff * 2
        decayed = base + monster_level + diff * 2
        return max(1, decayed)

    def get_exp_required(self, level: int) -> int:
        # 升级所需经验按等级指数递增，高级别升级更慢
        return int(100 * (1.15 ** (level - 1)))

    def needs_breakthrough(self, level: int) -> bool:
        # 关键等级需要突破材料和突破任务，不是经验满就升
        return level in BREAKTHROUGH_LEVELS

    def get_breakthrough_materials(self, level: int) -> dict:
        if not self.needs_breakthrough(level):
            return {}
        return {
            "突破石": level // 10,
            "精炼核心": max(1, level // 30),
        }

    def transfer_exp(self, source: Equipment, target: Equipment) -> int:
        # 装备经验可按比例转移到新装备，有转移损耗
        transferred = int(source.exp * TRANSFER_KEEP_RATIO)
        if transferred <= 0:
            return 0
        source.exp -= transferred
        target.exp += transferred
        return transferred

    def get_breakthrough_skill(self, level: int) -> str:
        # 关键等级解锁专属词条和技能，产生质变
        unlocked = ""
        for lv in sorted(BREAKTHROUGH_SKILLS):
            if level >= lv:
                unlocked = BREAKTHROUGH_SKILLS[lv]
        return unlocked

    def is_exp_maxed(self, equip: Equipment) -> bool:
        return equip.exp >= equip.exp_to_next

    def get_max_notification(self, equip: Equipment) -> str:
        # 经验满时给出明确提示
        if not self.is_exp_maxed(equip):
            return ""
        if self.needs_breakthrough(equip.level):
            return (
                f"装备[{equip.name}]经验已满（{equip.exp}/{equip.exp_to_next}），"
                f"需要突破材料{self.get_breakthrough_materials(equip.level)}并完成突破任务才能继续升级"
            )
        return f"装备[{equip.name}]经验已满（{equip.exp}/{equip.exp_to_next}），请及时升级"

    def add_exp(self, equip: Equipment, amount: int) -> int:
        # 经验满时自动停止获取，不浪费
        if self.is_exp_maxed(equip):
            return 0
        room = equip.exp_to_next - equip.exp
        gained = min(amount, room)
        equip.exp += gained
        return gained
