# ===== Step 12: 認知動詞（Cognitive Verbs）統合 =====
# 目標: ChatGPTの34ルール辞書を100％統合 (30→34ルール)
# 残り4ルール: 認知動詞のthat節処理を中心とした高度パターン

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from step11_passive_voice import Step11RuleEngine

class RephraseIntegrationStep12(Step11RuleEngine):
    """Step 12: 認知動詞（Cognitive Verbs）統合クラス"""
    
    def __init__(self):
        super().__init__()
        self.step_name = "Step 12: Cognitive Verbs"
        
    # ===== Step 12: 認知動詞ルール =====
    
    def rule_cognition_verb_that_clause(self, words):
        """認知動詞 + that節処理（S V O1[that-clause]）"""
        results = []
        cognition_verbs = ['think', 'believe', 'know', 'realize', 'figure']
        
        for i, word in enumerate(words):
            if word.lower() in cognition_verbs:
                # that節を探す
                that_start = -1
                for j in range(i + 1, len(words)):
                    if words[j].lower() == 'that':
                        that_start = j
                        break
                
                # that省略の場合も考慮
                if that_start == -1 and i + 1 < len(words):
                    # 動詞直後に主語らしき語があればthat節として処理
                    next_word = words[i + 1]
                    if next_word.lower() in ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'this', 'that', 'the']:
                        that_start = i + 1
                        that_omitted = True
                    else:
                        that_omitted = False
                else:
                    that_omitted = False
                
                if that_start != -1:
                    # 認知動詞をV Slotに配置
                    results.append({
                        'position': i,
                        'slot': 'V',
                        'value': word,
                        'type': 'word',
                        'rule_id': 'cognition-verb',
                        'priority': 25,
                        'note': f'認知動詞（{word.lower()}）',
                        'pattern': 'cognitive'
                    })
                    
                    # that節をO1スロットに配置
                    if that_omitted:
                        that_clause = ' '.join(words[that_start:])
                        clause_note = f'that節（that省略）: {that_clause[:30]}...'
                    else:
                        that_clause = ' '.join(words[that_start:])
                        clause_note = f'that節: {that_clause[:30]}...'
                    
                    results.append({
                        'position': that_start,
                        'slot': 'O1',
                        'value': that_clause,
                        'type': 'clause',
                        'rule_id': 'cognition-that-clause',
                        'priority': 25,
                        'note': clause_note,
                        'pattern': 'cognitive'
                    })
                    
        return results

    def rule_figure_out_phrasal(self, words):
        """句動詞 'figure out' 処理"""
        results = []
        
        for i in range(len(words) - 1):
            if (words[i].lower() == 'figure' and 
                words[i + 1].lower() == 'out'):
                
                results.append({
                    'position': i,
                    'slot': 'V',
                    'value': 'figure out',
                    'type': 'phrasal_verb',
                    'rule_id': 'figure-out-phrasal',
                    'priority': 26,
                    'note': '句動詞（figure out）',
                    'pattern': 'phrasal'
                })
                
        return results

    def rule_say_quotation(self, words):
        """say + 直接話法・間接話法処理"""
        results = []
        
        for i, word in enumerate(words):
            if word.lower() == 'say':
                # 直接話法（引用符）を探す
                quote_content = None
                for j in range(i + 1, len(words)):
                    if '"' in words[j] or "'" in words[j]:
                        # 引用符で始まる場合
                        quote_parts = []
                        in_quote = True
                        for k in range(j, len(words)):
                            quote_parts.append(words[k])
                            if k > j and ('"' in words[k] or "'" in words[k]):
                                break
                        quote_content = ' '.join(quote_parts)
                        break
                
                if quote_content:
                    # say動詞
                    results.append({
                        'position': i,
                        'slot': 'V',
                        'value': word,
                        'type': 'word',
                        'rule_id': 'say-verb',
                        'priority': 24,
                        'note': '発話動詞（say）'
                    })
                    
                    # 引用内容をO1に
                    results.append({
                        'position': j,
                        'slot': 'O1',
                        'value': quote_content,
                        'type': 'quotation',
                        'rule_id': 'say-quotation',
                        'priority': 24,
                        'note': f'直接話法: {quote_content[:20]}...'
                    })
                    
        return results

    def rule_reporting_verbs(self, words):
        """伝達動詞（tell, ask, explain等）+ 間接話法"""
        results = []
        reporting_verbs = ['tell', 'ask', 'explain', 'mention', 'suggest', 'propose']
        
        for i, word in enumerate(words):
            if word.lower() in reporting_verbs:
                # 動詞をVスロットに配置
                results.append({
                    'position': i,
                    'slot': 'V',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'reporting-verb',
                    'priority': 24,
                    'note': f'伝達動詞（{word.lower()}）',
                    'pattern': 'reporting'
                })
                
                # 直後の人称代名詞・名詞をO1（間接目的語）として処理
                if i + 1 < len(words):
                    next_word = words[i + 1]
                    if next_word.lower() in ['me', 'him', 'her', 'us', 'them'] or next_word.lower() == 'you':
                        results.append({
                            'position': i + 1,
                            'slot': 'O1',
                            'value': next_word,
                            'type': 'word',
                            'rule_id': 'reporting-indirect-obj',
                            'priority': 24,
                            'note': f'間接目的語（{next_word}）'
                        })
                        
                        # さらにその後のthat節をO2として処理
                        for j in range(i + 2, len(words)):
                            if words[j].lower() == 'that':
                                remaining_clause = ' '.join(words[j:])
                                results.append({
                                    'position': j,
                                    'slot': 'O2',
                                    'value': remaining_clause,
                                    'type': 'clause',
                                    'rule_id': 'reporting-that-clause',
                                    'priority': 24,
                                    'note': f'that節: {remaining_clause[:25]}...'
                                })
                                break
                    
        return results

    # ===== 統合処理 =====
    
    def analyze_sentence(self, sentence):
        """Step 12: 認知動詞統合解析"""
        words = sentence.split()
        
        # Step 11までのすべてのルールを継承
        slots = super().process_sentence(sentence)
        
        # Step 12: 認知動詞ルールを適用
        new_results = []
        new_results.extend(self.rule_cognition_verb_that_clause(words))
        new_results.extend(self.rule_figure_out_phrasal(words))
        new_results.extend(self.rule_say_quotation(words))
        new_results.extend(self.rule_reporting_verbs(words))
        
        # 新しい結果をスロットに統合
        for result in new_results:
            slot = result['slot']
            if slot not in slots:
                slots[slot] = []
                
            # 既存の結果と優先度比較
            should_add = True
            if slots[slot]:
                existing = slots[slot][0]
                if result.get('priority', 0) <= existing.get('priority', 0):
                    should_add = False
                    
            if should_add:
                slots[slot] = [result]
                
        return slots


def run_step12_tests():
    """Step 12統合テスト"""
    print("=== Step 12 Cognitive Verbs統合テスト ===")
    
    analyzer = RephraseIntegrationStep12()
    
    test_sentences = [
        # Step 11までの継続テスト
        "The book is written by John",
        "I should study hard", 
        "The book should be written",
        "I could have done it",
        
        # Step 12: 認知動詞テスト
        "I think that he is smart",
        "I believe you are right", 
        "She knows that it is true",
        "We realized that time was running out",
        "I figure out the problem",
        "He said \"Hello world\"",
        "She told me that she was tired",
        "They asked us what we wanted",
        
        # 複合テスト
        "I think that the book should be written",
        "She believes that I could have done better",
        "We know that they might have been there",
    ]
    
    for sentence in test_sentences:
        print(f"\n入力: {sentence}")
        try:
            slots = analyzer.analyze_sentence(sentence)
            for slot, candidates in slots.items():
                if candidates:
                    candidate = candidates[0]
                    pattern_info = f" [{candidate.get('pattern', '')}]" if candidate.get('pattern') else ""
                    print(f"{slot}: {candidate['value']} ({candidate.get('note', candidate['type'])}){pattern_info}")
        except Exception as e:
            print(f"エラー: {e}")


if __name__ == "__main__":
    run_step12_tests()
