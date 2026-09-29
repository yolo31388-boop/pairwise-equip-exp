"""装备经验与升级系统 - 红态测试"""
import pytest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from equip.exp import EquipExp, Equipment

class TestExpByMonsterLevel:
    def test_higher_level_monster_gives_more_exp(self):
        ee = EquipExp()
        e1 = ee.get_exp_from_kill(monster_level=1, player_level=50)
        e100 = ee.get_exp_from_kill(monster_level=100, player_level=50)
        assert e100 > e1  # bug1: 都是10

class TestExpRequirementGrowth:
    def test_higher_level_requires_more_exp(self):
        ee = EquipExp()
        r1 = ee.get_exp_required(1)
        r99 = ee.get_exp_required(99)
        assert r99 > r1 * 10  # bug2: 线性=100

class TestBreakthroughRequirement:
    def test_certain_levels_require_breakthrough(self):
        ee = EquipExp()
        assert ee.needs_breakthrough(30) == True  # bug3: False
        assert ee.needs_breakthrough(15) == False

class TestExpTransfer:
    def test_exp_can_be_transferred(self):
        ee = EquipExp()
        src = Equipment("s1", "old", exp=500)
        dst = Equipment("d1", "new", exp=0)
        transferred = ee.transfer_exp(src, dst)
        assert transferred > 0  # bug4: 0
        assert dst.exp > 0

class TestUniqueSkill:
    def test_breakthrough_unlocks_unique_skill(self):
        ee = EquipExp()
        skill = ee.get_breakthrough_skill(50)
        assert skill != ""  # bug5: 空

class TestExpMaxNotification:
    def test_maxed_exp_has_clear_indicator(self):
        ee = EquipExp()
        equip = Equipment("e1", "sword", exp=100, exp_to_next=100)
        assert ee.is_exp_maxed(equip) == True
        # 应该有提示方法
        assert hasattr(ee, "get_max_notification")
