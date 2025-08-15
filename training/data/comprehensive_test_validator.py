#!/usr/bin/env python3
"""
Comprehensive Test Validator for Unified Stanza-Rephrase Mapper
包括的テスト自動バリデーションシステム

全テストケースを自動実行し、期待結果と実際結果を比較分析。
アナログ確認作業を完全自動化。
"""

import sys
import logging
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import traceback

try:
    from unified_stanza_rephrase_mapper import UnifiedMapper
except ImportError:
    print("❌ unified_stanza_rephrase_mapper.py not found")
    sys.exit(1)

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class TestStatus(Enum):
    """テスト結果ステータス"""
    PASS = "✅ PASS"
    FAIL = "❌ FAIL"
    PARTIAL = "⚠️ PARTIAL"
    ERROR = "🚨 ERROR"

@dataclass
class TestCase:
    """単一テストケース定義"""
    id: str
    sentence: str
    expected_slots: Dict[str, str]
    expected_sub_slots: Dict[str, str]
    description: str = ""
    category: str = "general"

@dataclass
class TestResult:
    """テスト結果詳細"""
    test_id: str
    status: TestStatus
    actual_slots: Dict[str, str]
    actual_sub_slots: Dict[str, str]
    expected_slots: Dict[str, str]
    expected_sub_slots: Dict[str, str]
    mismatches: List[str]
    error_message: str = ""
    execution_time: float = 0.0

class ComprehensiveTestValidator:
    """包括的テストバリデーター"""
    
    def __init__(self):
        """初期化"""
        self.mapper = None
        self.test_cases = self._define_test_cases()
        self.results: List[TestResult] = []
        
    def _define_test_cases(self) -> List[TestCase]:
        """全テストケース定義"""
        return [
            # Phase 1: 基本5文型
            TestCase(
                id="Test01_SV",
                sentence="Birds fly.",
                expected_slots={"S": "Birds", "V": "fly"},
                expected_sub_slots={},
                description="第1文型 SV",
                category="basic_five_patterns"
            ),
            TestCase(
                id="Test02_SVO",
                sentence="I read books.",
                expected_slots={"S": "I", "V": "read", "O": "books"},
                expected_sub_slots={},
                description="第2文型 SVO",
                category="basic_five_patterns"
            ),
            TestCase(
                id="Test03_SVC",
                sentence="She is happy.",
                expected_slots={"S": "She", "V": "is", "C": "happy"},
                expected_sub_slots={},
                description="第3文型 SVC",
                category="basic_five_patterns"
            ),
            TestCase(
                id="Test04_SVOO",
                sentence="He gave me a book.",
                expected_slots={"S": "He", "V": "gave", "O": "me", "O2": "a book"},
                expected_sub_slots={},
                description="第4文型 SVOO",
                category="basic_five_patterns"
            ),
            TestCase(
                id="Test05_SVOC",
                sentence="We made him happy.",
                expected_slots={"S": "We", "V": "made", "O": "him", "C": "happy"},
                expected_sub_slots={},
                description="第5文型 SVOC",
                category="basic_five_patterns"
            ),
            
            # Phase 2: 関係節
            TestCase(
                id="Test10_RelativeClause",
                sentence="The man who lives here is kind.",
                expected_slots={"S": "", "V": "is", "C": "kind"},
                expected_sub_slots={"sub-m3": "The man who", "sub-s": "lives", "sub-v": "here"},
                description="関係代名詞節",
                category="relative_clauses"
            ),
            TestCase(
                id="Test12_ComplexRelative",
                sentence="The book that I bought yesterday was expensive.",
                expected_slots={"S": "", "V": "was", "C": "expensive"},
                expected_sub_slots={"sub-m3": "The book that", "sub-s": "I", "sub-v": "bought", "sub-m1": "yesterday"},
                description="複雑な関係節",
                category="relative_clauses"
            ),
            TestCase(
                id="Test26_ConsecutiveVerb",
                sentence="The door opened slowly creaked loudly.",
                expected_slots={"S": "", "V": "creaked", "M2": "loudly"},
                expected_sub_slots={"sub-v": "The door opened", "sub-m2": "slowly"},
                description="連続動詞パターン",
                category="consecutive_verbs"
            ),
            TestCase(
                id="Test30_WhereClause",
                sentence="The house where I was born is in Tokyo.",
                expected_slots={"S": "", "V": "is", "C2": "in Tokyo"},
                expected_sub_slots={"sub-m3": "The house where", "sub-s": "I", "sub-aux": "was", "sub-v": "born"},
                description="where構文（階層的解析）",
                category="hybrid_analysis"
            ),
            
            # Phase 3: 副詞・修飾語
            TestCase(
                id="Test15_Adverbs",
                sentence="She sings beautifully every day.",
                expected_slots={"S": "She", "V": "sings", "M2": "beautifully", "M1": "every day"},
                expected_sub_slots={},
                description="副詞修飾",
                category="adverbial_modifiers"
            ),
            TestCase(
                id="Test16_TimeAdverb",
                sentence="Yesterday, I went to school.",
                expected_slots={"S": "I", "V": "went", "M3": "to school", "M1": "Yesterday"},
                expected_sub_slots={},
                description="時間副詞",
                category="adverbial_modifiers"
            ),
            
            # Phase 4: 複合構造
            TestCase(
                id="Test20_CompoundSubject",
                sentence="Tom and Mary are students.",
                expected_slots={"S": "Tom and Mary", "V": "are", "C": "students"},
                expected_sub_slots={},
                description="複合主語",
                category="compound_structures"
            ),
            TestCase(
                id="Test21_PrepositionalPhrase",
                sentence="The cat is on the table.",
                expected_slots={"S": "The cat", "V": "is", "C2": "on the table"},
                expected_sub_slots={},
                description="前置詞句",
                category="prepositional_phrases"
            ),
            
            # Phase 5: エッジケース
            TestCase(
                id="Test25_Passive",
                sentence="The car was parked carefully.",
                expected_slots={"S": "The car", "V": "was parked", "M2": "carefully"},
                expected_sub_slots={},
                description="受動態",
                category="edge_cases"
            ),
        ]
    
    def initialize_mapper(self) -> bool:
        """マッパー初期化"""
        try:
            logger.info("🔧 Unified Stanza-Rephrase Mapper 初期化中...")
            self.mapper = UnifiedMapper()
            
            # 全ハンドラー追加
            self.mapper.add_handler('basic_five_pattern')
            self.mapper.add_handler('relative_clause')
            self.mapper.add_handler('adverbial_modifier')
            
            logger.info("✅ マッパー初期化完了")
            return True
            
        except Exception as e:
            logger.error(f"❌ マッパー初期化失敗: {e}")
            return False
    
    def run_single_test(self, test_case: TestCase) -> TestResult:
        """単一テスト実行"""
        import time
        start_time = time.time()
        
        try:
            # 文解析実行
            result = self.mapper.process_sentence(test_case.sentence)
            execution_time = time.time() - start_time
            
            # 結果抽出
            actual_slots = result.get('slots', {})
            actual_sub_slots = result.get('sub_slots', {})
            
            # 比較分析
            mismatches = []
            
            # メインスロット比較
            for expected_key, expected_value in test_case.expected_slots.items():
                actual_value = actual_slots.get(expected_key, "")
                if actual_value != expected_value:
                    mismatches.append(f"Slot {expected_key}: expected '{expected_value}', got '{actual_value}'")
            
            # 予期しないスロット検出
            for actual_key, actual_value in actual_slots.items():
                if actual_key not in test_case.expected_slots and actual_value:
                    mismatches.append(f"Unexpected slot {actual_key}: '{actual_value}'")
            
            # サブスロット比較
            for expected_key, expected_value in test_case.expected_sub_slots.items():
                actual_value = actual_sub_slots.get(expected_key, "")
                if actual_value != expected_value:
                    mismatches.append(f"Sub-slot {expected_key}: expected '{expected_value}', got '{actual_value}'")
            
            # 予期しないサブスロット検出
            for actual_key, actual_value in actual_sub_slots.items():
                if actual_key not in test_case.expected_sub_slots and actual_value:
                    mismatches.append(f"Unexpected sub-slot {actual_key}: '{actual_value}'")
            
            # ステータス判定
            if not mismatches:
                status = TestStatus.PASS
            elif len(mismatches) <= 2:  # 軽微な不一致
                status = TestStatus.PARTIAL
            else:
                status = TestStatus.FAIL
            
            return TestResult(
                test_id=test_case.id,
                status=status,
                actual_slots=actual_slots,
                actual_sub_slots=actual_sub_slots,
                expected_slots=test_case.expected_slots,
                expected_sub_slots=test_case.expected_sub_slots,
                mismatches=mismatches,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult(
                test_id=test_case.id,
                status=TestStatus.ERROR,
                actual_slots={},
                actual_sub_slots={},
                expected_slots=test_case.expected_slots,
                expected_sub_slots=test_case.expected_sub_slots,
                mismatches=[],
                error_message=str(e),
                execution_time=execution_time
            )
    
    def run_all_tests(self) -> Dict[str, Any]:
        """全テスト実行"""
        if not self.initialize_mapper():
            return {"error": "Mapper initialization failed"}
        
        logger.info(f"🚀 全テスト実行開始: {len(self.test_cases)} tests")
        
        self.results = []
        category_results = {}
        
        for test_case in self.test_cases:
            logger.info(f"🔍 実行中: {test_case.id} - {test_case.description}")
            result = self.run_single_test(test_case)
            self.results.append(result)
            
            # カテゴリ別集計
            if test_case.category not in category_results:
                category_results[test_case.category] = {"pass": 0, "fail": 0, "partial": 0, "error": 0, "total": 0}
            
            category_results[test_case.category]["total"] += 1
            if result.status == TestStatus.PASS:
                category_results[test_case.category]["pass"] += 1
            elif result.status == TestStatus.FAIL:
                category_results[test_case.category]["fail"] += 1
            elif result.status == TestStatus.PARTIAL:
                category_results[test_case.category]["partial"] += 1
            elif result.status == TestStatus.ERROR:
                category_results[test_case.category]["error"] += 1
        
        return self._generate_summary_report(category_results)
    
    def _generate_summary_report(self, category_results: Dict) -> Dict[str, Any]:
        """サマリーレポート生成"""
        total_tests = len(self.results)
        passed = sum(1 for r in self.results if r.status == TestStatus.PASS)
        failed = sum(1 for r in self.results if r.status == TestStatus.FAIL)
        partial = sum(1 for r in self.results if r.status == TestStatus.PARTIAL)
        errors = sum(1 for r in self.results if r.status == TestStatus.ERROR)
        
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        
        return {
            "summary": {
                "total_tests": total_tests,
                "passed": passed,
                "failed": failed,
                "partial": partial,
                "errors": errors,
                "success_rate": f"{success_rate:.1f}%"
            },
            "category_breakdown": category_results,
            "detailed_results": [
                {
                    "test_id": r.test_id,
                    "status": r.status.value,
                    "mismatches": r.mismatches,
                    "error": r.error_message,
                    "execution_time": f"{r.execution_time:.3f}s"
                }
                for r in self.results
            ]
        }
    
    def print_detailed_report(self):
        """詳細レポート出力"""
        print("\n" + "="*80)
        print("📊 COMPREHENSIVE TEST VALIDATION REPORT")
        print("="*80)
        
        summary = self._generate_summary_report({})
        
        # サマリー
        print(f"\n📈 Overall Summary:")
        print(f"   Total Tests: {summary['summary']['total_tests']}")
        print(f"   ✅ Passed: {summary['summary']['passed']}")
        print(f"   ❌ Failed: {summary['summary']['failed']}")
        print(f"   ⚠️ Partial: {summary['summary']['partial']}")
        print(f"   🚨 Errors: {summary['summary']['errors']}")
        print(f"   📊 Success Rate: {summary['summary']['success_rate']}")
        
        # 詳細結果
        print(f"\n📋 Detailed Results:")
        for result in self.results:
            print(f"\n{result.status.value} {result.test_id}")
            if result.mismatches:
                for mismatch in result.mismatches:
                    print(f"    🔸 {mismatch}")
            if result.error_message:
                print(f"    🚨 Error: {result.error_message}")
            print(f"    ⏱️ Execution: {result.execution_time:.3f}s")
        
        print("\n" + "="*80)

def main():
    """メイン実行"""
    print("🔧 Comprehensive Test Validator Starting...")
    
    validator = ComprehensiveTestValidator()
    
    try:
        # 全テスト実行
        results = validator.run_all_tests()
        
        # 詳細レポート出力
        validator.print_detailed_report()
        
        # JSON形式でも出力
        with open('test_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 結果をtest_results.jsonに保存しました")
        
    except Exception as e:
        print(f"❌ テスト実行中にエラーが発生: {e}")
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
