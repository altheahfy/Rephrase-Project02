
import pandas as pd
from rephrase_rule_functions import *

rules_df = pd.read_excel("rephrase_rules.xlsx", sheet_name="Rephrase文法分解ルール一覧")

def eval_rule_condition(tokens, i, condition_str):
    token = tokens[i]
    local_vars = {"token": token}
    try:
        if condition_str.startswith("match_"):
            func = globals().get(condition_str)
            if func:
                return func(tokens, i)
            else:
                print(f"関数未定義: {condition_str}")
                return None
        if eval(condition_str, {}, local_vars):
            return token.text, i, i
        return None
    except Exception as e:
        print(f"条件評価エラー: {e} (条件: {condition_str})")
        return None

def map_to_rephrase_slots(doc):
    result = []
    tokens = list(doc)
    i = 0
    while i < len(tokens):
        matched = False
        for _, rule in rules_df.iterrows():
            condition = rule["条件 (条件式または関数名)"]
            slot = rule["出力スロット"]
            matched_val = eval_rule_condition(tokens, i, condition)
            if matched_val:
                phrase, start_idx, end_idx = matched_val
                result.append((slot, phrase))
                print(f"DEBUG: マッチ -> {slot}, {phrase}")
                i = end_idx + 1
                matched = True
                break
        if not matched:
            i += 1
    return result
