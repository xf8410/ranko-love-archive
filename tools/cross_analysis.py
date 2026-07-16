#!/usr/bin/env python3
"""
赛马娘数据交叉分析工具
将umaDB角色数据与cardDB支援卡数据关联分析
"""

import json
import os

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def analyze():
    # 数据路径
    uma_db = load_json('../game-data/umaDB/umaDB_full.json')
    card_db = load_json('../game-data/cardDB/cardDB_full.json')
    
    print(f"角色总数: {len(uma_db)}")
    print(f"支援卡总数: {len(card_db)}")
    
    # 按角色ID统计支援卡
    chara_cards = {}
    for cid, card in card_db.items():
        chara_id = card.get('charaId', 0)
        if chara_id not in chara_cards:
            chara_cards[chara_id] = []
        chara_cards[chara_id].append(card)
    
    print(f"\n有支援卡的角色数: {len(chara_cards)}")
    
    # 按卡片类型统计
    type_names = {0: '速度', 1: '耐力', 2: '力量', 3: '根性', 4: '智力', 5: '友人'}
    type_count = {}
    for card in card_db.values():
        ct = card.get('cardType', -1)
        type_count[ct] = type_count.get(ct, 0) + 1
    
    print("\n卡片类型分布:")
    for t, c in sorted(type_count.items()):
        print(f"  {type_names.get(t, f'未知({t})')}: {c}张")
    
    # 稀有度分布
    rarity_names = {1: 'R', 2: 'SR', 3: 'SSR'}
    rarity_count = {}
    for card in card_db.values():
        r = card.get('rarity', 0)
        rarity_count[r] = rarity_count.get(r, 0) + 1
    
    print("\n稀有度分布:")
    for r, c in sorted(rarity_count.items()):
        print(f"  {rarity_names.get(r, f'未知({r})')}: {c}张")
    
    # 角色支援卡数量排名 (Top 10)
    chara_card_count = {}
    for cid, card in card_db.items():
        ci = card.get('charaId', 0)
        chara_card_count[ci] = chara_card_count.get(ci, 0) + 1
    
    print("\n支援卡数量最多的角色 (Top 10):")
    for ci, count in sorted(chara_card_count.items(), key=lambda x: -x[1])[:10]:
        # 查找角色名
        chara_name = "?"
        for kid, chara in uma_db.items():
            if str(chara.get('gameId', '')).endswith(str(ci)):
                chara_name = chara.get('name', '?')
                break
        if chara_name == '?':
            # 尝试直接匹配
            for kid in uma_db:
                if int(kid) // 10 == ci:
                    chara_name = uma_db[kid].get('name', '?')
                    break
        print(f"  ID {ci}: {chara_name} - {count}张支援卡")

if __name__ == '__main__':
    analyze()
