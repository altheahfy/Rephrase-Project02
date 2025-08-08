# ===== Step 13: サブクローズ分解エンジン =====
# 目標: Rephraseの複文対応 - 1階層サブクローズ分解のみ
# 方針: 多重入れ子は扱わず、直下のサブクローズのみ分解

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from step12_cognitive_verbs import RephraseIntegrationStep12

class RephraseIntegrationStep13(RephraseIntegrationStep12):
    """Step 13: サブクローズ分解エンジン"""
    
    def __init__(self):
        super().__init__()
        self.step_name = "Step 13: Subclause Decomposition"
        
    def decompose_that_clause(self, clause_text):
        """that節を1階層サブクローズに分解"""
        if not clause_text.strip():
            return {}
            
        # that節全体を使用（thatも保持）
        inner_text = clause_text.strip()
        words = inner_text.split()
        if len(words) < 2:
            return {}
            
        subslots = {}
        
        # that + 主語を sub-s として扱う
        if words[0].lower() == 'that':
            if len(words) > 1:
                if words[1].lower() in ['i', 'you', 'he', 'she', 'it', 'we', 'they']:
                    subslots['sub-s'] = f"{words[0]} {words[1]}"  # "that he"
                    remaining = words[2:]
                elif words[1].lower() == 'the' and len(words) > 2:
                    # "that the man who came" のような複合主語
                    # 動詞っぽい語まで探す
                    verb_pos = -1
                    for i, word in enumerate(words[2:], 2):
                        if self.is_likely_verb(word):
                            verb_pos = i
                            break
                    
                    if verb_pos > 0:
                        subslots['sub-s'] = ' '.join(words[:verb_pos])  # "that the man who"
                        remaining = words[verb_pos:]
                    else:
                        subslots['sub-s'] = f"{words[0]} {words[1]}"  # "that the"
                        remaining = words[2:]
                else:
                    subslots['sub-s'] = f"{words[0]} {words[1]}"  # "that something"
                    remaining = words[2:]
            else:
                return {}
        else:
            # that省略の場合
            if words[0].lower() in ['i', 'you', 'he', 'she', 'it', 'we', 'they']:
                subslots['sub-s'] = words[0]
                remaining = words[1:]
            elif words[0].lower() == 'the' and len(words) > 1:
                # "the man who came" のような複合主語
                verb_pos = -1
                for i, word in enumerate(words[1:], 1):
                    if self.is_likely_verb(word):
                        verb_pos = i
                        break
                
                if verb_pos > 0:
                    subslots['sub-s'] = ' '.join(words[:verb_pos])
                    remaining = words[verb_pos:]
                else:
                    subslots['sub-s'] = words[0]
                    remaining = words[1:]
            else:
                subslots['sub-s'] = words[0]
                remaining = words[1:]
            
        if not remaining:
            return subslots
            
        # sub-aux, sub-v の検出
        aux_verbs = ['is', 'are', 'am', 'was', 'were', 'will', 'would', 'can', 'could', 
                    'should', 'must', 'might', 'may', 'have', 'has', 'had']
                    
        if remaining[0].lower() in aux_verbs:
            subslots['sub-aux'] = remaining[0]
            if len(remaining) > 1:
                subslots['sub-v'] = remaining[1]
                if len(remaining) > 2:
                    # 残りをsub-o1またはsub-c1として扱う
                    rest = ' '.join(remaining[2:])
                    if remaining[1].lower() in ['is', 'are', 'am', 'was', 'were']:
                        subslots['sub-c1'] = rest
                    else:
                        subslots['sub-o1'] = rest
        else:
            subslots['sub-v'] = remaining[0]
            if len(remaining) > 1:
                # 残りをsub-o1として扱う（1つの塊）
                subslots['sub-o1'] = ' '.join(remaining[1:])
                
        return subslots
    
    def is_likely_verb(self, word):
        """語が動詞らしいかの簡単な判定"""
        verb_indicators = ['is', 'are', 'am', 'was', 'were', 'do', 'does', 'did',
                          'have', 'has', 'had', 'will', 'would', 'can', 'could',
                          'should', 'must', 'might', 'may', 'came', 'knows', 'said', 
                          'think', 'believes', 'goes', 'likes', 'wants', 'needs']
        return word.lower() in verb_indicators or word.lower().endswith('ed') or word.lower().endswith('ing')
    
    def decompose_wh_clause(self, clause_text):
        """wh節を1階層サブクローズに分解"""
        words = clause_text.split()
        if len(words) < 2:
            return {}
            
        subslots = {}
        
        # wh語をsub-o1として扱う（what, where, when等）
        if words[0].lower() in ['what', 'where', 'when', 'why', 'how', 'who']:
            subslots['sub-o1'] = words[0]  # または適切なスロット
            remaining = words[1:]
            
            if remaining and remaining[0].lower() in ['i', 'you', 'he', 'she', 'it', 'we', 'they']:
                subslots['sub-s'] = remaining[0]
                if len(remaining) > 1:
                    subslots['sub-v'] = remaining[1]
                    if len(remaining) > 2:
                        subslots['sub-o1'] = ' '.join(remaining[2:])
                        
        return subslots
    
    def enhance_cognitive_verb_with_subclause(self, words):
        """認知動詞のthat節にサブクローズ分解を適用"""
        results = []
        cognition_verbs = {
            'think': 'think', 'thinks': 'think', 'thought': 'think',
            'believe': 'believe', 'believes': 'believe', 'believed': 'believe', 
            'know': 'know', 'knows': 'know', 'knew': 'know', 'known': 'know',
            'realize': 'realize', 'realizes': 'realize', 'realized': 'realize',
            'figure': 'figure', 'figures': 'figure', 'figured': 'figure'
        }
        
        for i, word in enumerate(words):
            if word.lower() in cognition_verbs:
                base_form = cognition_verbs[word.lower()]
                
                # that節を探す
                that_start = -1
                for j in range(i + 1, len(words)):
                    if words[j].lower() == 'that':
                        that_start = j
                        break
                
                # that省略の場合も考慮
                if that_start == -1 and i + 1 < len(words):
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
                        'rule_id': 'cognition-verb-enhanced',
                        'priority': 26,  # 少し高い優先度
                        'note': f'認知動詞（{base_form}）',
                        'pattern': 'cognitive'
                    })
                    
                    # that節を取得してサブクローズ分解
                    if that_omitted:
                        that_clause = ' '.join(words[that_start:])
                    else:
                        that_clause = ' '.join(words[that_start:])
                    
                    # サブクローズ分解実行
                    if that_clause.lower().startswith('what') or that_clause.lower().startswith('where'):
                        subslots = self.decompose_wh_clause(that_clause)
                    else:
                        subslots = self.decompose_that_clause(that_clause)
                    
                    # サブクローズ付きO1スロットを作成
                    results.append({
                        'position': that_start,
                        'slot': 'O1',
                        'value': that_clause,
                        'type': 'subclause',
                        'rule_id': 'cognition-subclause',
                        'priority': 26,
                        'note': f'that節（サブクローズ分解済み）: {that_clause[:25]}...',
                        'pattern': 'cognitive',
                        'subslots': subslots  # サブクローズ情報
                    })
                    
        return results
    
    def analyze_sentence(self, sentence):
        """Step 13: サブクローズ分解統合解析"""
        # Step 12の処理を継承
        slots = super().analyze_sentence(sentence)
        
        # Step 13: サブクローズ分解強化版認知動詞ルールを適用
        words = sentence.split()
        enhanced_results = self.enhance_cognitive_verb_with_subclause(words)
        
        # 強化版の結果で既存を上書き
        for result in enhanced_results:
            slot = result['slot']
            if slot not in slots:
                slots[slot] = []
                
            # より高い優先度なので置き換え
            if result.get('priority', 0) > 25:  # Step 12の優先度より高い
                slots[slot] = [result]
                
        return slots


def test_subclause_decomposition():
    """サブクローズ分解テスト"""
    print("=== Step 13: サブクローズ分解テスト ===")
    
    analyzer = RephraseIntegrationStep13()
    
    test_sentences = [
        # 基本的なthat節
        "I think that he is smart",
        "She believes that we are ready", 
        
        # 複合主語のthat節  
        "I think that the man who came knows what we need",
        
        # that省略
        "I believe you are right",
        
        # wh節
        "I know what he thinks",
        "She knows where we should go",
    ]
    
    for sentence in test_sentences:
        print(f"\n入力: {sentence}")
        try:
            slots = analyzer.analyze_sentence(sentence)
            
            for slot, candidates in slots.items():
                if candidates:
                    candidate = candidates[0]
                    value = candidate['value']
                    note = candidate.get('note', candidate['type'])
                    pattern_info = f" [{candidate.get('pattern', '')}]" if candidate.get('pattern') else ""
                    
                    print(f"  {slot}: {value} ({note}){pattern_info}")
                    
                    # サブクローズ情報があれば表示
                    if 'subslots' in candidate and candidate['subslots']:
                        for sub_slot, sub_value in candidate['subslots'].items():
                            print(f"    └─ {sub_slot}: {sub_value}")
                            
        except Exception as e:
            print(f"  ❌ エラー: {e}")


if __name__ == "__main__":
    test_subclause_decomposition()
