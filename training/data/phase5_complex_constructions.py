"""
Phase 5: 複合構文検出システム
関係詞構文、名詞節、不定詞、動名詞、仮定法、受動態の検出

対象構文:
1. 関係詞構文 (制限的/非制限的/省略)
2. 名詞節構文 (that/wh-clause/同格節)  
3. 不定詞構文 (目的/結果)
4. 動名詞構文
5. 仮定法構文
6. 受動態構文
"""

import spacy
import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

class ComplexConstructionType(Enum):
    # 関係詞構文 (3)
    RELATIVE_CLAUSE_RESTRICTIVE = "制限的関係詞節"
    RELATIVE_CLAUSE_NON_RESTRICTIVE = "非制限的関係詞節"
    RELATIVE_PRONOUN_OMISSION = "関係代名詞省略"
    
    # 名詞句/節構文 (2)
    NOUN_CLAUSE = "名詞節"
    APPOSITIVE_CLAUSE = "同格節"
    
    # 不定詞構文 (2)
    INFINITIVE_PURPOSE = "目的の不定詞"
    INFINITIVE_RESULT = "結果の不定詞"
    
    # 動名詞構文 (1)
    GERUND_CONSTRUCTION = "動名詞構文"
    
    # 仮定法構文 (1)
    SUBJUNCTIVE_MOOD = "仮定法"
    
    # 受動態構文 (1)
    PASSIVE_VOICE = "受動態"

@dataclass
class ComplexConstructionResult:
    construction_type: ComplexConstructionType
    confidence: float
    original_text: str
    analysis: str
    rephrase_slots: Dict[str, str]

class Phase5ComplexConstructions:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy英語モデルが見つかりません。'python -m spacy download en_core_web_sm'でインストールしてください。")
            self.nlp = None
            
        # 関係代名詞リスト
        self.relative_pronouns = {
            'who', 'whom', 'whose', 'which', 'that', 'where', 'when', 'why'
        }
        
        # 名詞節導入語
        self.noun_clause_introducers = {
            'that', 'what', 'who', 'whom', 'whose', 'which', 'where', 'when', 
            'why', 'how', 'whether', 'if'
        }
        
        # 目的を表す表現
        self.purpose_markers = {
            'to', 'in order to', 'so as to', 'in order that', 'so that'
        }
        
        # 結果を表す表現  
        self.result_markers = {
            'so as to', 'such as to', 'too', 'enough'
        }
        
        # 動名詞構文マーカー
        self.gerund_markers = {
            'enjoy', 'finish', 'suggest', 'avoid', 'consider', 'admit',
            'deny', 'imagine', 'practice', 'risk', 'mind', 'miss'
        }
        
        # 仮定法マーカー
        self.subjunctive_markers = {
            'if', 'unless', 'suppose', 'supposing', 'provided', 'providing',
            'as long as', 'on condition that', 'wish', 'would rather'
        }

    def detect_construction(self, text: str) -> List[ComplexConstructionResult]:
        """複合構文を検出する"""
        if not self.nlp:
            return []
            
        results = []
        doc = self.nlp(text)
        
        # 各構文タイプをチェック
        results.extend(self._detect_relative_clauses(doc, text))
        results.extend(self._detect_noun_clauses(doc, text))
        results.extend(self._detect_infinitive_constructions(doc, text))
        results.extend(self._detect_gerund_constructions(doc, text))
        results.extend(self._detect_subjunctive_mood(doc, text))
        results.extend(self._detect_passive_voice(doc, text))
        
        return results

    def _detect_relative_clauses(self, doc, text: str) -> List[ComplexConstructionResult]:
        """関係詞構文を検出する"""
        results = []
        
        for token in doc:
            # 制限的関係詞節
            if (token.text.lower() in self.relative_pronouns and 
                token.dep_ in ['nsubj', 'dobj', 'pobj']):
                
                # コンマで区切られているかチェック
                is_non_restrictive = self._has_comma_separation(doc, token)
                
                if is_non_restrictive:
                    construction_type = ComplexConstructionType.RELATIVE_CLAUSE_NON_RESTRICTIVE
                    analysis = f"非制限的関係詞節: '{token.text}'で導かれる補足情報"
                else:
                    construction_type = ComplexConstructionType.RELATIVE_CLAUSE_RESTRICTIVE
                    analysis = f"制限的関係詞節: '{token.text}'で導かれる必要不可欠な情報"
                
                rephrase_slots = {
                    'relative_pronoun': token.text,
                    'antecedent': str(token.head),
                    'relative_clause': self._extract_relative_clause(doc, token)
                }
                
                results.append(ComplexConstructionResult(
                    construction_type=construction_type,
                    confidence=0.85,
                    original_text=text,
                    analysis=analysis,
                    rephrase_slots=rephrase_slots
                ))
        
        # 関係代名詞省略をチェック
        omission_result = self._detect_relative_pronoun_omission(doc, text)
        if omission_result:
            results.append(omission_result)
            
        return results

    def _detect_noun_clauses(self, doc, text: str) -> List[ComplexConstructionResult]:
        """名詞節を検出する"""
        results = []
        
        for token in doc:
            if token.text.lower() in self.noun_clause_introducers:
                # that節の検出
                if token.text.lower() == 'that' and token.dep_ == 'mark':
                    clause_type = "that節"
                    analysis = f"名詞節: '{token.text}'で導かれる内容節"
                    
                # wh-節の検出
                elif token.text.lower() in ['what', 'who', 'where', 'when', 'why', 'how']:
                    clause_type = "wh-節"
                    analysis = f"名詞節: '{token.text}'で導かれる疑問詞節"
                    
                # 同格節の検出
                elif (token.text.lower() == 'that' and 
                      self._is_appositive_clause(doc, token)):
                    construction_type = ComplexConstructionType.APPOSITIVE_CLAUSE
                    analysis = f"同格節: 名詞の内容を説明する'{token.text}'節"
                    
                    results.append(ComplexConstructionResult(
                        construction_type=construction_type,
                        confidence=0.80,
                        original_text=text,
                        analysis=analysis,
                        rephrase_slots={
                            'noun': str(token.head.head) if token.head.head else '',
                            'clause_content': self._extract_clause_content(doc, token)
                        }
                    ))
                    continue
                else:
                    continue
                
                results.append(ComplexConstructionResult(
                    construction_type=ComplexConstructionType.NOUN_CLAUSE,
                    confidence=0.85,
                    original_text=text,
                    analysis=analysis,
                    rephrase_slots={
                        'clause_introducer': token.text,
                        'clause_content': self._extract_clause_content(doc, token),
                        'clause_type': clause_type
                    }
                ))
        
        return results

    def _detect_infinitive_constructions(self, doc, text: str) -> List[ComplexConstructionResult]:
        """不定詞構文を検出する"""
        results = []
        
        for token in doc:
            if token.text.lower() == 'to' and token.pos_ == 'PART':
                # 目的の不定詞
                if self._is_purpose_infinitive(doc, token, text):
                    results.append(ComplexConstructionResult(
                        construction_type=ComplexConstructionType.INFINITIVE_PURPOSE,
                        confidence=0.80,
                        original_text=text,
                        analysis="目的の不定詞: 行為の目的を表す",
                        rephrase_slots={
                            'main_verb': self._find_main_verb(doc, token),
                            'purpose_infinitive': self._extract_infinitive_phrase(doc, token)
                        }
                    ))
                
                # 結果の不定詞
                elif self._is_result_infinitive(doc, token, text):
                    results.append(ComplexConstructionResult(
                        construction_type=ComplexConstructionType.INFINITIVE_RESULT,
                        confidence=0.75,
                        original_text=text,
                        analysis="結果の不定詞: 行為の結果を表す",
                        rephrase_slots={
                            'cause': self._find_cause_element(doc, token),
                            'result_infinitive': self._extract_infinitive_phrase(doc, token)
                        }
                    ))
        
        return results

    def _detect_gerund_constructions(self, doc, text: str) -> List[ComplexConstructionResult]:
        """動名詞構文を検出する"""
        results = []
        
        for token in doc:
            # 動名詞を取る動詞の検出を拡張
            if token.pos_ == 'VERB':
                for child in token.children:
                    # VBG（動名詞）を目的語として取る
                    if child.tag_ == 'VBG' and child.dep_ in ['dobj', 'xcomp']:
                        # 動名詞を取る典型的動詞かチェック
                        if (token.lemma_ in self.gerund_markers or 
                            self._is_gerund_taking_context(token, child)):
                            
                            results.append(ComplexConstructionResult(
                                construction_type=ComplexConstructionType.GERUND_CONSTRUCTION,
                                confidence=0.85,
                                original_text=text,
                                analysis=f"動名詞構文: '{token.text}'が動名詞'{child.text}'を目的語にとる",
                                rephrase_slots={
                                    'gerund_taking_verb': token.text,
                                    'gerund': child.text,
                                    'gerund_phrase': self._extract_gerund_phrase(doc, child)
                                }
                            ))
            
            # 動名詞が主語になっているケース
            elif token.tag_ == 'VBG' and token.dep_ == 'nsubj':
                results.append(ComplexConstructionResult(
                    construction_type=ComplexConstructionType.GERUND_CONSTRUCTION,
                    confidence=0.80,
                    original_text=text,
                    analysis=f"動名詞構文: '{token.text}'が主語として機能",
                    rephrase_slots={
                        'gerund': token.text,
                        'gerund_phrase': self._extract_gerund_phrase(doc, token),
                        'function': 'subject'
                    }
                ))
        
        return results

    def _detect_subjunctive_mood(self, doc, text: str) -> List[ComplexConstructionResult]:
        """仮定法を検出する"""
        results = []
        
        # 仮定法の典型的パターン
        if re.search(r'\b(if|wish|would rather|suppose)\b.*\b(were|had|would|could|should)\b', text, re.IGNORECASE):
            # より詳細な分析
            for token in doc:
                if token.text.lower() in self.subjunctive_markers:
                    # 仮定法過去/過去完了の検出
                    subjunctive_type = self._identify_subjunctive_type(doc, token, text)
                    
                    results.append(ComplexConstructionResult(
                        construction_type=ComplexConstructionType.SUBJUNCTIVE_MOOD,
                        confidence=0.75,
                        original_text=text,
                        analysis=f"仮定法: {subjunctive_type}",
                        rephrase_slots={
                            'condition_marker': token.text,
                            'subjunctive_type': subjunctive_type,
                            'condition_clause': self._extract_condition_clause(doc, token),
                            'main_clause': self._extract_main_clause(doc, token)
                        }
                    ))
                    break
        
        return results

    def _detect_passive_voice(self, doc, text: str) -> List[ComplexConstructionResult]:
        """受動態を検出する"""
        results = []
        
        for token in doc:
            # 標準的な受動態: auxpass + VBN
            if token.dep_ == 'auxpass' and token.lemma_ == 'be':
                # 対応する過去分詞を探す
                for sibling in token.head.children:
                    if sibling.dep_ == 'auxpass' and sibling == token:
                        past_participle = token.head
                        if past_participle.tag_ == 'VBN':
                            # 主語を探す（nsubjpass）
                            passive_subject = self._find_passive_subject_by_dep(doc)
                            # by句を探す
                            by_phrase = self._find_by_phrase(doc, past_participle)
                            
                            results.append(ComplexConstructionResult(
                                construction_type=ComplexConstructionType.PASSIVE_VOICE,
                                confidence=0.95,
                                original_text=text,
                                analysis=f"受動態: be動詞'{token.text}' + 過去分詞'{past_participle.text}'",
                                rephrase_slots={
                                    'be_verb': token.text,
                                    'past_participle': past_participle.text,
                                    'subject': passive_subject,
                                    'by_phrase': by_phrase if by_phrase else 'なし'
                                }
                            ))
                            break
        
        # 別パターン: be動詞 + 過去分詞の直接検出
        for token in doc:
            if (token.lemma_ == 'be' and token.pos_ in ['VERB', 'AUX'] and
                any(child.tag_ == 'VBN' for child in token.children)):
                
                past_participle = next(
                    (child for child in token.children if child.tag_ == 'VBN'), 
                    None
                )
                
                if past_participle and past_participle.dep_ != 'ROOT':
                    continue  # 既に処理済み
                
                # by句の検出
                by_phrase = self._find_by_phrase(doc, past_participle or token)
                
                results.append(ComplexConstructionResult(
                    construction_type=ComplexConstructionType.PASSIVE_VOICE,
                    confidence=0.90,
                    original_text=text,
                    analysis=f"受動態: be動詞'{token.text}' + 過去分詞'{past_participle.text if past_participle else 'unknown'}'",
                    rephrase_slots={
                        'be_verb': token.text,
                        'past_participle': past_participle.text if past_participle else '',
                        'subject': self._find_passive_subject(doc, token),
                        'by_phrase': by_phrase if by_phrase else 'なし'
                    }
                ))
        
        # get/have + 過去分詞の受動態も検出
        for token in doc:
            if token.lemma_ in ['get', 'have'] and token.pos_ == 'VERB':
                for child in token.children:
                    if child.tag_ == 'VBN' and child.dep_ in ['dobj', 'ccomp']:
                        results.append(ComplexConstructionResult(
                            construction_type=ComplexConstructionType.PASSIVE_VOICE,
                            confidence=0.75,
                            original_text=text,
                            analysis=f"受動態: {token.text}動詞 + 過去分詞'{child.text}'",
                            rephrase_slots={
                                'auxiliary_verb': token.text,
                                'past_participle': child.text,
                                'subject': self._find_passive_subject(doc, token),
                                'by_phrase': self._find_by_phrase(doc, child) or 'なし'
                            }
                        ))
        
        return results

    # ヘルパーメソッド
    def _has_comma_separation(self, doc, token) -> bool:
        """関係詞節がコンマで区切られているかチェック"""
        for i, t in enumerate(doc):
            if t == token:
                # 前にコンマがあるかチェック
                if i > 0 and doc[i-1].text == ',':
                    return True
                # 関係詞節の終わりにコンマがあるかチェック  
                for j in range(i+1, len(doc)):
                    if doc[j].text == ',' and doc[j].head == token.head:
                        return True
                break
        return False

    def _extract_relative_clause(self, doc, relative_pronoun) -> str:
        """関係詞節を抽出"""
        clause_tokens = []
        for token in doc:
            if token.head == relative_pronoun or self._is_in_relative_clause(token, relative_pronoun):
                clause_tokens.append(token)
        return ' '.join([t.text for t in sorted(clause_tokens, key=lambda x: x.i)])

    def _detect_relative_pronoun_omission(self, doc, text: str) -> Optional[ComplexConstructionResult]:
        """関係代名詞の省略を検出"""
        # 典型的な省略パターン: "The book I read" (that省略)
        for token in doc:
            if (token.pos_ == 'NOUN' and 
                any(child.pos_ == 'VERB' and child.dep_ == 'relcl' for child in token.children)):
                
                return ComplexConstructionResult(
                    construction_type=ComplexConstructionType.RELATIVE_PRONOUN_OMISSION,
                    confidence=0.70,
                    original_text=text,
                    analysis="関係代名詞省略: thatまたはwhichが省略されている",
                    rephrase_slots={
                        'antecedent': token.text,
                        'omitted_pronoun': 'that/which',
                        'relative_clause': str(next(child for child in token.children if child.dep_ == 'relcl'))
                    }
                )
        return None

    def _is_appositive_clause(self, doc, token) -> bool:
        """同格節かどうかを判定"""
        # 特定の名詞（fact, idea, news等）の後のthat節
        appositive_nouns = {'fact', 'idea', 'news', 'belief', 'hope', 'fear', 'rumor'}
        if token.head and token.head.lemma_.lower() in appositive_nouns:
            return True
        return False

    def _extract_clause_content(self, doc, introducer) -> str:
        """節の内容を抽出"""
        clause_tokens = []
        for token in doc:
            if token.head == introducer or self._is_in_clause(token, introducer):
                clause_tokens.append(token)
        return ' '.join([t.text for t in sorted(clause_tokens, key=lambda x: x.i)])

    def _is_purpose_infinitive(self, doc, to_token, text: str) -> bool:
        """目的の不定詞かどうかを判定"""
        # "in order to", "so as to"などの明示的マーカー
        text_lower = text.lower()
        if any(marker in text_lower for marker in self.purpose_markers):
            return True
        
        # 文脈から目的を推定
        infinitive_verb = None
        for child in to_token.children:
            if child.pos_ == 'VERB':
                infinitive_verb = child
                break
        
        if infinitive_verb:
            # 動作を表す動詞の場合は目的の可能性が高い
            action_verbs = {'go', 'come', 'buy', 'get', 'find', 'see', 'meet', 'help'}
            if infinitive_verb.lemma_ in action_verbs:
                return True
        
        return False

    def _is_result_infinitive(self, doc, to_token, text: str) -> bool:
        """結果の不定詞かどうかを判定"""
        # "too...to", "so...as to", "such...as to"パターン
        if re.search(r'\b(too|so|such)\b.*\bto\b', text, re.IGNORECASE):
            return True
        
        # "enough to"パターン
        if re.search(r'\benough\s+to\b', text, re.IGNORECASE):
            return True
        
        return False

    def _find_main_verb(self, doc, to_token) -> str:
        """主動詞を見つける"""
        for token in doc:
            if token.pos_ == 'VERB' and token.dep_ == 'ROOT':
                return token.text
        return ''

    def _extract_infinitive_phrase(self, doc, to_token) -> str:
        """不定詞句を抽出"""
        phrase_tokens = [to_token]
        for child in to_token.children:
            if child.pos_ == 'VERB':
                phrase_tokens.append(child)
                phrase_tokens.extend(list(child.subtree))
        return ' '.join([t.text for t in sorted(set(phrase_tokens), key=lambda x: x.i)])

    def _find_cause_element(self, doc, to_token) -> str:
        """原因要素を見つける"""
        for token in doc:
            if token.text.lower() in ['too', 'so', 'such', 'enough']:
                return token.text
        return ''

    def _extract_gerund_phrase(self, doc, gerund_token) -> str:
        """動名詞句を抽出"""
        phrase_tokens = [gerund_token]
        phrase_tokens.extend(list(gerund_token.subtree))
        return ' '.join([t.text for t in sorted(phrase_tokens, key=lambda x: x.i)])

    def _identify_subjunctive_type(self, doc, marker_token, text: str) -> str:
        """仮定法の種類を特定"""
        if 'were' in text or 'had' in text:
            if 'had' in text and re.search(r'\bhad\s+\w+ed\b', text):
                return "仮定法過去完了（過去の仮定）"
            else:
                return "仮定法過去（現在の仮定）"
        elif any(modal in text for modal in ['would', 'could', 'should', 'might']):
            return "仮定法（条件文の帰結）"
        else:
            return "仮定法"

    def _extract_condition_clause(self, doc, marker_token) -> str:
        """条件節を抽出"""
        # 条件節の抽出ロジック
        clause_tokens = []
        for token in doc:
            if (token.head == marker_token or 
                self._is_in_conditional_clause(token, marker_token)):
                clause_tokens.append(token)
        return ' '.join([t.text for t in sorted(clause_tokens, key=lambda x: x.i)])

    def _extract_main_clause(self, doc, marker_token) -> str:
        """主節を抽出"""
        main_clause_tokens = []
        for token in doc:
            if token.dep_ == 'ROOT' or self._is_in_main_clause(token):
                main_clause_tokens.append(token)
        return ' '.join([t.text for t in sorted(main_clause_tokens, key=lambda x: x.i)])

    def _find_by_phrase(self, doc, past_participle) -> Optional[str]:
        """by句を見つける"""
        for child in past_participle.children:
            if child.text.lower() == 'by':
                by_phrase_tokens = [child]
                by_phrase_tokens.extend(list(child.subtree))
                return ' '.join([t.text for t in sorted(by_phrase_tokens, key=lambda x: x.i)])
        return None

    def _find_passive_subject(self, doc, be_verb) -> str:
        """受動態の主語を見つける"""
        for child in be_verb.children:
            if child.dep_ == 'nsubj':
                return child.text
        return ''

    def _is_in_relative_clause(self, token, relative_pronoun) -> bool:
        """トークンが関係詞節に含まれているかチェック"""
        current = token
        while current.head != current:
            if current.head == relative_pronoun:
                return True
            current = current.head
        return False

    def _is_in_clause(self, token, introducer) -> bool:
        """トークンが節に含まれているかチェック"""
        current = token
        while current.head != current:
            if current.head == introducer:
                return True
            current = current.head
        return False

    def _is_in_conditional_clause(self, token, marker) -> bool:
        """トークンが条件節に含まれているかチェック"""
        return self._is_in_clause(token, marker)

    def _is_in_main_clause(self, token) -> bool:
        """トークンが主節に含まれているかチェック"""
        return token.dep_ in ['ROOT', 'ccomp', 'xcomp']

    def _is_gerund_taking_context(self, verb_token, gerund_token) -> bool:
        """動名詞を取る文脈かどうかを判定"""
        # enjoy, like, love, hate, start, begin, continueなど
        gerund_taking_verbs = {
            'enjoy', 'like', 'love', 'hate', 'start', 'begin', 'continue',
            'stop', 'quit', 'finish', 'complete', 'suggest', 'recommend',
            'avoid', 'consider', 'practice', 'keep', 'mind', 'miss', 'risk'
        }
        return verb_token.lemma_ in gerund_taking_verbs

    def _find_passive_subject_by_dep(self, doc) -> str:
        """依存関係を使って受動態の主語を見つける"""
        for token in doc:
            if token.dep_ == 'nsubjpass':
                return token.text
        return ''

def test_phase5_constructions():
    """Phase 5構文のテスト"""
    detector = Phase5ComplexConstructions()
    
    test_cases = [
        # 関係詞構文
        "The book that I read was interesting.",           # 制限的関係詞節
        "My brother, who lives in Tokyo, is a doctor.",    # 非制限的関係詞節  
        "The movie I watched yesterday was great.",        # 関係代名詞省略
        
        # 名詞節
        "I think that he is right.",                       # that節
        "I know what you mean.",                           # wh-節
        "The fact that he failed surprised us.",           # 同格節
        
        # 不定詞構文
        "I went to the store to buy milk.",                # 目的の不定詞
        "He is too young to drive.",                       # 結果の不定詞
        
        # 動名詞構文
        "I enjoy reading books.",                          # 動名詞構文
        
        # 仮定法
        "If I were you, I would accept the offer.",        # 仮定法過去
        
        # 受動態
        "The letter was written by John.",                 # 受動態
    ]
    
    print("🧪 Phase 5: 複合構文検出テスト")
    print("=" * 50)
    
    total_tests = len(test_cases)
    successful_detections = 0
    
    for i, test_sentence in enumerate(test_cases, 1):
        print(f"\n📝 テスト {i}: {test_sentence}")
        
        results = detector.detect_construction(test_sentence)
        
        if results:
            successful_detections += 1
            print("✅ 検出成功:")
            for result in results:
                print(f"   🎯 構文: {result.construction_type.value}")
                print(f"   📊 信頼度: {result.confidence:.2f}")
                print(f"   📋 分析: {result.analysis}")
                print(f"   🔧 スロット: {result.rephrase_slots}")
        else:
            print("❌ 検出失敗")
    
    print(f"\n📊 Phase 5テスト結果:")
    success_rate = (successful_detections / total_tests) * 100
    print(f"✅ 成功率: {success_rate:.1f}% ({successful_detections}/{total_tests})")
    print(f"🎯 新規構文: 10パターン実装")
    
    return success_rate >= 80

if __name__ == "__main__":
    test_phase5_constructions()
