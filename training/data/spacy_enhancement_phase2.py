#!/usr/bin/env python3
"""
spaCy拡張機能 フェーズ2: 文構造拡張
=================================

フェーズ2では文構造をより深く解析する依存関係を実装します：
- nmod: 名詞修飾関係
- xcomp: オープン節補語  
- ccomp: 節補語
- auxpass: 受動態助動詞
- agent: 受動態の動作主
- pcomp: 前置詞補語
- dative: 与格（間接目的語）

これらの実装により、複雑な文構造の理解が大幅に向上します。
"""

import json
import os
from typing import Dict, List, Any

class SpacyRephraseExtensionPhase2:
    """フェーズ2: 文構造拡張依存関係の実装"""
    
    def __init__(self):
        self.existing_rules_file = "enhanced_rephrase_rules_phase1.json"
        self.output_file = "enhanced_rephrase_rules_phase2.json"
        
    def load_existing_rules(self) -> List[Dict[str, Any]]:
        """既存のフェーズ1ルールを読み込み"""
        if os.path.exists(self.existing_rules_file):
            with open(self.existing_rules_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('rules', [])
        return []
    
    def generate_nmod_rule(self) -> Dict[str, Any]:
        """nmod: 名詞修飾関係のルール生成"""
        return {
            "id": "noun-modifier-nmod-M1",
            "description": "名詞修飾関係の検出（nmod依存関係）",
            "trigger": {
                "dependency": ["nmod"],
                "priority": "high"
            },
            "action": {
                "slot": "M1",
                "type": "phrase",
                "extraction_method": "nmod_phrase_extraction"
            },
            "examples": [
                "the book on the table",
                "a man with a hat", 
                "the city of Tokyo"
            ],
            "confidence": 0.85
        }
    
    def generate_xcomp_rule(self) -> Dict[str, Any]:
        """xcomp: オープン節補語のルール生成"""
        return {
            "id": "open-clausal-complement-xcomp-O2",
            "description": "オープン節補語の検出（to不定詞など）",
            "trigger": {
                "dependency": ["xcomp"],
                "priority": "high"
            },
            "action": {
                "slot": "O2",
                "type": "clause",
                "extraction_method": "xcomp_clause_extraction"
            },
            "examples": [
                "I want to go home",
                "She decided to study",
                "We plan to visit Japan"
            ],
            "confidence": 0.9
        }
    
    def generate_ccomp_rule(self) -> Dict[str, Any]:
        """ccomp: 節補語のルール生成"""
        return {
            "id": "clausal-complement-ccomp-O2",
            "description": "節補語の検出（that節など）",
            "trigger": {
                "dependency": ["ccomp"],
                "priority": "high"
            },
            "action": {
                "slot": "O2", 
                "type": "clause",
                "extraction_method": "ccomp_clause_extraction"
            },
            "examples": [
                "I think that he is right",
                "She said she would come",
                "We know you are busy"
            ],
            "confidence": 0.9
        }
    
    def generate_auxpass_rule(self) -> Dict[str, Any]:
        """auxpass: 受動態助動詞のルール生成"""
        return {
            "id": "passive-auxiliary-auxpass-Aux",
            "description": "受動態助動詞の検出（be + 過去分詞）",
            "trigger": {
                "dependency": ["auxpass"],
                "priority": "high"
            },
            "action": {
                "slot": "Aux",
                "type": "auxiliary",
                "extraction_method": "auxpass_extraction"
            },
            "examples": [
                "The book was written by him",
                "The car is being repaired", 
                "The problem will be solved"
            ],
            "confidence": 0.95
        }
    
    def generate_agent_rule(self) -> Dict[str, Any]:
        """agent: 受動態の動作主のルール生成"""
        return {
            "id": "passive-agent-by-M3",
            "description": "受動態の動作主検出（by句）",
            "trigger": {
                "dependency": ["agent"],
                "pattern": r"(?i)\bby\s+[\s\S]+",
                "priority": "high"
            },
            "action": {
                "slot": "M3",
                "type": "phrase",
                "extraction_method": "agent_phrase_extraction"
            },
            "examples": [
                "written by Shakespeare",
                "designed by the architect",
                "discovered by scientists"
            ],
            "confidence": 0.9
        }
    
    def generate_pcomp_rule(self) -> Dict[str, Any]:
        """pcomp: 前置詞補語のルール生成"""
        return {
            "id": "prepositional-complement-pcomp-M2",
            "description": "前置詞補語の検出",
            "trigger": {
                "dependency": ["pcomp"],
                "priority": "medium"
            },
            "action": {
                "slot": "M2",
                "type": "complement",
                "extraction_method": "pcomp_extraction"
            },
            "examples": [
                "interested in learning",
                "good at playing",
                "afraid of flying"
            ],
            "confidence": 0.8
        }
    
    def generate_dative_rule(self) -> Dict[str, Any]:
        """dative: 与格（間接目的語）のルール生成"""
        return {
            "id": "dative-indirect-object-O2",
            "description": "与格・間接目的語の検出",
            "trigger": {
                "dependency": ["dative"],
                "priority": "high"
            },
            "action": {
                "slot": "O2",
                "type": "indirect_object",
                "extraction_method": "dative_extraction"
            },
            "examples": [
                "give him a book",
                "show her the way",
                "tell me the truth"
            ],
            "confidence": 0.85
        }
    
    def generate_phase2_rules(self) -> List[Dict[str, Any]]:
        """フェーズ2の全ルールを生成"""
        return [
            self.generate_nmod_rule(),
            self.generate_xcomp_rule(),
            self.generate_ccomp_rule(),
            self.generate_auxpass_rule(),
            self.generate_agent_rule(),
            self.generate_pcomp_rule(),
            self.generate_dative_rule()
        ]
    
    def create_enhanced_rules_phase2(self):
        """フェーズ2拡張ルールファイルの作成"""
        existing_rules = self.load_existing_rules()
        phase2_rules = self.generate_phase2_rules()
        
        all_rules = existing_rules + phase2_rules
        
        enhanced_data = {
            "version": "2.0",
            "description": "Rephrase文法解析ルール - フェーズ2拡張版（文構造拡張）",
            "phase": 2,
            "total_rules": len(all_rules),
            "phase1_rules": len(existing_rules),
            "phase2_rules": len(phase2_rules),
            "spacy_coverage": {
                "total_dependencies": 45,
                "covered_dependencies": len(all_rules) + 4,  # フェーズ1の4つ + フェーズ2の7つ
                "coverage_percentage": round(((len(all_rules) + 4) / 45) * 100, 1)
            },
            "rules": all_rules
        }
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(enhanced_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ フェーズ2拡張ルールファイル作成完了: {self.output_file}")
        print(f"📊 既存ルール: {len(existing_rules)}個")
        print(f"📊 新規ルール: {len(phase2_rules)}個") 
        print(f"📊 合計ルール: {len(all_rules)}個")
        print(f"📊 spaCy依存関係カバレッジ: {enhanced_data['spacy_coverage']['coverage_percentage']}%")
        
        return enhanced_data

if __name__ == "__main__":
    enhancer = SpacyRephraseExtensionPhase2()
    enhancer.create_enhanced_rules_phase2()
