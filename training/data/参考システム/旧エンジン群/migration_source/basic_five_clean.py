#!/usr/bin/env python3
"""
Basic Five Pattern Engine - Lightweight Integrated Version
Pure Stanza Engine V3.1縺九ｉ謚ｽ蜃ｺ縺励◆遏･隴倥・繝ｼ繧ｹ縺ｫ繧医ｋ霆ｽ驥丞渕譛ｬ5譁・梛繧ｨ繝ｳ繧ｸ繝ｳ

Features:
1. Pure Stanza Engine V3.1縺ｮ遏･隴倥・繝ｼ繧ｹ繧堤ｶ呎価
2. Grammar Master Controller邨ｱ蜷井ｻ墓ｧ俶ｺ匁侠
3. 繝上・繝峨さ繝ｼ繝・ぅ繝ｳ繧ｰ謗帝勁・育衍隴倥・繝ｼ繧ｹ鬧・虚・・4. 蝓ｺ譛ｬ5譁・梛 + 蜉ｩ蜍戊ｩ樊ｧ区枚縺ｫ迚ｹ蛹・"""

import stanza
from typing import Dict, List, Optional, Any
import time

class BasicFivePatternEngine:
    """蝓ｺ譛ｬ5譁・梛繧ｨ繝ｳ繧ｸ繝ｳ・育ｵｱ蜷亥梛霆ｽ驥冗沿・・""
    
    def __init__(self):
        """邨ｱ蜷井ｻ墓ｧ伜ｯｾ蠢懊・霆ｽ驥・譁・梛繧ｨ繝ｳ繧ｸ繝ｳ蛻晄悄蛹・""
        print("噫 Basic Five Pattern Engine 蛻晄悄蛹紋ｸｭ...")
        
        # Stanza NLP 繝代う繝励Λ繧､繝ｳ
        self.nlp = stanza.Pipeline('en', verbose=False)
        
        # Pure Stanza Engine V3.1縺九ｉ謚ｽ蜃ｺ縺励◆遏･隴倥・繝ｼ繧ｹ
        self.sentence_patterns = self._load_sentence_patterns()
        self.modifier_mappings = self._load_modifier_mappings()
        
        self.name = "BasicFivePatternEngine"
        self.version = "1.0"
        
        print("笨・蝓ｺ譛ｬ5譁・梛繧ｨ繝ｳ繧ｸ繝ｳ貅門ｙ螳御ｺ・)
    
    def _load_sentence_patterns(self) -> Dict[str, Any]:
        """Pure Stanza Engine V3.1縺九ｉ謚ｽ蜃ｺ・壼渕譛ｬ譁・梛繝代ち繝ｼ繝ｳ"""
        return {
            # 蝓ｺ譛ｬ5譁・梛・亥━蜈亥ｺｦ繧定ｪｿ謨ｴ・・            "SVOO": {
                "required_relations": ["nsubj", "iobj", "obj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "iobj": "O1", "obj": "O2", "root": "V"},
                "priority": 1  # 譛鬮伜━蜈亥ｺｦ・域怙繧ょ・菴鍋噪・・            },
            "SVOC": {
                "required_relations": ["nsubj", "obj", "xcomp", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "obj": "O1", "xcomp": "C2", "root": "V"},
                "priority": 2
            },
            "SVO": {
                "required_relations": ["nsubj", "obj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "obj": "O1", "root": "V"},
                "priority": 3
            },
            "SVC": {
                "required_relations": ["nsubj", "cop", "root"],
                "root_pos": ["ADJ", "NOUN"],
                "mapping": {"nsubj": "S", "cop": "V", "root": "C1"},
                "priority": 4
            },
            "SV": {
                "required_relations": ["nsubj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "root": "V"},
                "priority": 5  # 譛繧よｱ守畑逧・↑縺ｮ縺ｧ菴主━蜈亥ｺｦ
            },
            
            # 蜉ｩ蜍戊ｩ樊ｧ区枚・・ure Stanza Engine V3.1縺九ｉ邯呎価・・            "S_AUX_VO": {
                "required_relations": ["nsubj", "aux", "obj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "aux": "Aux", "obj": "O1", "root": "V"},
                "priority": 6
            },
            "S_AUX_VC": {
                "required_relations": ["nsubj", "aux", "cop", "root"],
                "root_pos": ["ADJ", "NOUN"],
                "mapping": {"nsubj": "S", "aux": "Aux", "cop": "V", "root": "C1"},
                "priority": 7
            },
            "S_AUX_V": {
                "required_relations": ["nsubj", "aux", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "aux": "Aux", "root": "V"},
                "priority": 8
            },
            
            # 蜿怜虚諷九ヱ繧ｿ繝ｼ繝ｳ
            "PASSIVE": {
                "required_relations": ["nsubj:pass", "aux:pass", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj:pass": "S", "aux:pass": "Aux", "root": "V"},
                "priority": 9
            }
        }
    
    def _load_modifier_mappings(self) -> Dict[str, str]:
        """Pure Stanza Engine V3.1縺九ｉ謚ｽ蜃ｺ・壻ｿｮ鬟ｾ隱槭・繝・ヴ繝ｳ繧ｰ・亥渕譛ｬ5譁・梛縺ｫ迚ｹ蛹厄ｼ・""
        return {
            # 蝓ｺ譛ｬ菫ｮ鬟ｾ隱橸ｼ域枚蝙区ｧ矩縺ｫ髢｢繧上ｋ繧ゅ・縺ｮ縺ｿ・・            "advmod": "M2",     # 蜑ｯ隧樔ｿｮ鬟ｾ隱橸ｼ・uickly, hard, etc.・・            "nmod": "M1",       # 蜷崎ｩ樔ｿｮ鬟ｾ隱・            "obl": "M3",        # 譁懈ｼ隱橸ｼ亥燕鄂ｮ隧槫唱縺ｪ縺ｩ・・            "tmod": "M3",       # 譎る俣菫ｮ鬟ｾ
            "neg": "M3",        # 蜷ｦ螳・            
            # 髯､螟悶☆繧倶ｿｮ鬟ｾ隱橸ｼ井ｻ悶お繝ｳ繧ｸ繝ｳ縺ｮ蠖ｹ蜑ｲ・・            # "det": 蜀隧槭・髯仙ｮ夊ｩ槭・蝓ｺ譛ｬ5譁・梛縺ｧ縺ｯ謇ｱ繧上↑縺・            # "case": 蜑咲ｽｮ隧槭・蜑咲ｽｮ隧槫唱繧ｨ繝ｳ繧ｸ繝ｳ縺ｮ蠖ｹ蜑ｲ
            # "aux": 蜉ｩ蜍戊ｩ槭・繝｢繝ｼ繝繝ｫ繧ｨ繝ｳ繧ｸ繝ｳ縺ｮ蠖ｹ蜑ｲ
            # "agent": 蜍穂ｽ應ｸｻ縺ｯ蜿怜虚諷九お繝ｳ繧ｸ繝ｳ縺ｮ蠖ｹ蜑ｲ
        }
    
    def process_sentence(self, sentence: str) -> Optional[Dict]:
        """邨ｱ蜷井ｻ墓ｧ俶ｺ匁侠縺ｮ繝｡繧､繝ｳ蜃ｦ逅・Γ繧ｽ繝・ラ"""
        if not sentence or len(sentence.strip()) < 2:
            return None
        
        start_time = time.time()
        
        try:
            # Stanza隗｣譫・            doc = self.nlp(sentence)
            sent = doc.sentences[0]
            
            # 蝓ｺ譛ｬ5譁・梛縺ｮ讀懷・縺ｨ蜃ｦ逅・            result = self._analyze_basic_patterns(sent)
            
            if result:
                processing_time = time.time() - start_time
                return {
                    "engine": self.name,
                    "version": self.version,
                    "pattern": result["pattern"],
                    "slots": result["slots"],
                    "confidence": result["confidence"],
                    "processing_time": processing_time,
                    "processed": True
                }
                
        except Exception as e:
            print(f"笞・・Basic Pattern Engine Error: {e}")
            return None
        
        return None
    
    def _analyze_basic_patterns(self, sent) -> Optional[Dict]:
        """遏･隴倥・繝ｼ繧ｹ鬧・虚縺ｮ蝓ｺ譛ｬ譁・梛隗｣譫・""
        
        # ROOT隱樊､懷・
        root_word = self._find_root_word(sent)
        if not root_word:
            return None
        
        # 萓晏ｭ倬未菫ゅ・繝・・讒狗ｯ・        dep_relations = {}
        for word in sent.words:
            if word.deprel not in dep_relations:
                dep_relations[word.deprel] = []
            dep_relations[word.deprel].append(word)
        
        # 繝代ち繝ｼ繝ｳ繝槭ャ繝√Φ繧ｰ・亥━蜈亥ｺｦ鬆・ｼ・        for pattern_name, pattern_info in sorted(
            self.sentence_patterns.items(), 
            key=lambda x: x[1]["priority"]
        ):
            if self._matches_pattern(pattern_info, dep_relations, root_word):
                slots = self._build_slots(pattern_info, dep_relations, sent)
                if slots:
                    return {
                        "pattern": pattern_name,
                        "slots": slots,
                        "confidence": self._calculate_confidence(pattern_name, slots)
                    }
        
        return None
    
    def _matches_pattern(self, pattern_info: Dict, dep_relations: Dict, root_word) -> bool:
        """繝代ち繝ｼ繝ｳ繝槭ャ繝√Φ繧ｰ蛻､螳・""
        # 蠢・ｦ√↑萓晏ｭ倬未菫ゅ・蟄伜惠遒ｺ隱・        required_relations = pattern_info["required_relations"]
        for rel in required_relations:
            if rel not in dep_relations:
                return False
        
        # ROOT隱槭・蜩∬ｩ槭メ繧ｧ繝・け
        root_pos_allowed = pattern_info["root_pos"]
        if root_word.pos not in root_pos_allowed:
            return False
        
        return True
    
    def _build_slots(self, pattern_info: Dict, dep_relations: Dict, sent) -> Dict[str, str]:
        """繧ｹ繝ｭ繝・ヨ讒狗ｯ会ｼ育衍隴倥・繝ｼ繧ｹ鬧・虚・・""
        slots = {}
        mapping = pattern_info["mapping"]
        
        # 繝｡繧､繝ｳ繧ｹ繝ｭ繝・ヨ讒狗ｯ・        for dep_rel, slot in mapping.items():
            if dep_rel in dep_relations:
                words = dep_relations[dep_rel]
                if words:
                    # 隍・焚縺ｮ隱槭′縺ゅｋ蝣ｴ蜷医・譛蛻昴・隱槭ｒ菴ｿ逕ｨ
                    target_word = words[0]
                    # 隱槫唱蠅・阜縺ｮ諡｡蠑ｵ
                    expanded_text = self._expand_phrase_boundary(target_word, sent)
                    slots[slot] = expanded_text
            elif dep_rel == "root":
                # ROOT隱槭・蜃ｦ逅・                root_word = self._find_root_word(sent)
                if root_word and slot in ["V"]:
                    slots[slot] = root_word.text
        
        # 菫ｮ鬟ｾ隱槭・蜃ｦ逅・        modifier_slots = {"M1": [], "M2": [], "M3": []}
        for word in sent.words:
            if word.deprel in self.modifier_mappings:
                slot = self.modifier_mappings[word.deprel]
                if slot.startswith("M"):  # M1, M2, M3繧ｹ繝ｭ繝・ヨ
                    expanded_text = self._expand_phrase_boundary(word, sent)
                    if expanded_text not in modifier_slots[slot]:
                        modifier_slots[slot].append(expanded_text)
        
        # 菫ｮ鬟ｾ隱槭せ繝ｭ繝・ヨ繧堤ｵｱ蜷・        for slot, values in modifier_slots.items():
            if values:
                slots[slot] = ", ".join(values)
        
        return slots
    
    def _find_root_word(self, sent):
        """ROOT隱樊､懷・"""
        for word in sent.words:
            if word.deprel == 'root':
                return word
        return None
    
    def _expand_phrase_boundary(self, word, sent) -> str:
        """蝓ｺ譛ｬ5譁・梛縺ｫ驕ｩ縺励◆隱槫唱蠅・阜諡｡蠑ｵ"""
        # 隱槫唱蠅・阜諡｡蠑ｵ縺ｮ萓晏ｭ倬未菫ゑｼ亥渕譛ｬ譁・梛讒矩縺ｫ蠢・ｦ√↑繧ゅ・縺ｮ縺ｿ・・        expand_deps = ['compound', 'amod', 'nummod']  # 隍・粋隱槭∝ｽ｢螳ｹ隧槭∵焚驥剰ｩ槭・縺ｿ
        
        words_to_include = [word]
        
        # 蟄占ｦ∫ｴ縺ｮ謗｢邏｢
        for other_word in sent.words:
            if (other_word.head == word.id and 
                other_word.deprel in expand_deps):
                words_to_include.append(other_word)
        
        # 蜀隧槭・髯仙ｮ夊ｩ槭・蝓ｺ譛ｬ譁・梛縺ｧ縺ｯ蜷ｫ繧√ｋ・医せ繝ｭ繝・ヨ縺ｫ縺ｯ險ｭ螳壹＠縺ｪ縺・ｼ・        for other_word in sent.words:
            if (other_word.head == word.id and 
                other_word.deprel == 'det'):
                words_to_include.append(other_word)
        
        # 菴咲ｽｮ鬆・〒繧ｽ繝ｼ繝・        words_to_include.sort(key=lambda w: w.id)
        
        return " ".join([w.text for w in words_to_include])
    
    def _calculate_confidence(self, pattern_name: str, slots: Dict) -> float:
        """菫｡鬆ｼ蠎ｦ險育ｮ・""
        base_confidence = 0.85
        
        # 繧ｹ繝ｭ繝・ヨ謨ｰ縺ｫ繧医ｋ繝懊・繝翫せ
        slot_bonus = len(slots) * 0.02
        
        # 繝代ち繝ｼ繝ｳ蝗ｺ譛峨・繝懊・繝翫せ
        pattern_bonus = {
            "SVO": 0.05,    # 譛繧ゆｸ闊ｬ逧・            "SV": 0.03,     # 繧ｷ繝ｳ繝励Ν
            "SVC": 0.04,    # 譏守｢ｺ縺ｪ讒矩
            "SVOO": 0.08,   # 隍・尅縺縺梧・遒ｺ
            "SVOC": 0.06    # 隍・尅讒矩
        }.get(pattern_name, 0.0)
        
        confidence = min(0.98, base_confidence + slot_bonus + pattern_bonus)
        return confidence

def test_basic_five_pattern_engine():
    """繝・せ繝磯未謨ｰ"""
    engine = BasicFivePatternEngine()
    
    test_sentences = [
        "I love programming.",
        "She is a teacher.",
        "He gave her a book.",
        "We consider him smart.",
        "The dog runs quickly.",
        "I can speak English.",
        "They are working hard.",
        "The book was written by John."
    ]
    
    print("\nｧｪ Testing Basic Five Pattern Engine")
    print("=" * 60)
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n笨・Test {i}: {sentence}")
        result = engine.process_sentence(sentence)
        if result:
            print(f"    Pattern: {result['pattern']}")
            print(f"    Slots: {result['slots']}")
            print(f"    Confidence: {result['confidence']:.3f}")
        else:
            print("    笶・No pattern detected")

if __name__ == "__main__":
    test_basic_five_pattern_engine()
