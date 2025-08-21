"""
Pattern Registry
文法パターンの動的登録・管理システム

統一されたパターン管理により、新しい文法パターンの
動的登録と適用順序の制御を実現
"""

from typing import Dict, List, Type, Optional
import logging
from .base_patterns import BasePattern, GrammarPattern, PositionPattern


class PatternRegistry:
    """
    文法パターンの動的登録・管理システム
    
    個別ハンドラーアプローチから統一システムへの移行において、
    全パターンの一元管理を実現
    """
    
    def __init__(self):
        self.logger = logging.getLogger("PatternRegistry")
        
        # 登録済みパターン
        self.registered_patterns: Dict[str, BasePattern] = {}
        
        # パターン優先順位（高い数値が優先）
        self.pattern_priorities: Dict[str, int] = {}
        
        # パターン依存関係
        self.pattern_dependencies: Dict[str, List[str]] = {}
        
        # パターン統計
        self.pattern_stats: Dict[str, Dict] = {}
        
        # 組み込みパターンを登録
        self._register_built_in_patterns()
        
    def _register_built_in_patterns(self):
        """組み込みパターンの登録"""
        # NOTE: 実際のパターンクラスは後で作成
        # ここでは構造のみ定義
        
        built_in_configs = {
            'whose_ambiguous_verb': {
                'priority': 90,
                'dependencies': [],
                'description': 'whose構文での動詞/名詞同形語修正'
            },
            'passive_voice': {
                'priority': 85,
                'dependencies': [],
                'description': '受動態パターン修正'
            },
            'complex_relative': {
                'priority': 80,
                'dependencies': ['whose_ambiguous_verb'],
                'description': '複合関係節修正'
            }
        }
        
        for pattern_name, config in built_in_configs.items():
            self.pattern_priorities[pattern_name] = config['priority']
            self.pattern_dependencies[pattern_name] = config['dependencies']
            self.pattern_stats[pattern_name] = {
                'description': config['description'],
                'registered_at': self._get_timestamp(),
                'usage_count': 0,
                'success_count': 0,
                'last_used': None
            }
            
        self.logger.debug(f"📝 組み込みパターン登録完了: {list(built_in_configs.keys())}")
        
    def register_pattern(self, pattern_name: str, pattern_instance: BasePattern, 
                        priority: int = 50, dependencies: List[str] = None) -> bool:
        """
        新しいパターンを登録
        
        Args:
            pattern_name: パターン名
            pattern_instance: パターンインスタンス
            priority: 優先順位 (0-100, 高い値が優先)
            dependencies: 依存パターンリスト
            
        Returns:
            登録成功フラグ
        """
        if dependencies is None:
            dependencies = []
            
        try:
            # 依存関係チェック
            if not self._validate_dependencies(dependencies):
                self.logger.error(f"❌ パターン登録失敗 [{pattern_name}]: 依存関係エラー")
                return False
                
            # 重複チェック
            if pattern_name in self.registered_patterns:
                self.logger.warning(f"⚠️ パターン上書き [{pattern_name}]")
                
            # パターン登録
            self.registered_patterns[pattern_name] = pattern_instance
            self.pattern_priorities[pattern_name] = priority
            self.pattern_dependencies[pattern_name] = dependencies
            
            # 統計初期化
            self.pattern_stats[pattern_name] = {
                'description': getattr(pattern_instance, 'description', ''),
                'registered_at': self._get_timestamp(),
                'usage_count': 0,
                'success_count': 0,
                'last_used': None
            }
            
            self.logger.debug(
                f"✅ パターン登録成功 [{pattern_name}]: "
                f"priority={priority}, deps={dependencies}"
            )
            return True
            
        except Exception as e:
            self.logger.error(f"❌ パターン登録エラー [{pattern_name}]: {str(e)}")
            return False
            
    def unregister_pattern(self, pattern_name: str) -> bool:
        """
        パターンの登録解除
        
        Args:
            pattern_name: 解除するパターン名
            
        Returns:
            解除成功フラグ
        """
        if pattern_name not in self.registered_patterns:
            self.logger.warning(f"⚠️ 未登録パターンの解除試行 [{pattern_name}]")
            return False
            
        # 依存チェック：他のパターンがこのパターンに依存していないか
        dependent_patterns = [
            name for name, deps in self.pattern_dependencies.items()
            if pattern_name in deps
        ]
        
        if dependent_patterns:
            self.logger.error(
                f"❌ パターン解除失敗 [{pattern_name}]: "
                f"依存パターンあり {dependent_patterns}"
            )
            return False
            
        # 解除実行
        del self.registered_patterns[pattern_name]
        del self.pattern_priorities[pattern_name]
        del self.pattern_dependencies[pattern_name]
        del self.pattern_stats[pattern_name]
        
        self.logger.debug(f"🗑️ パターン解除完了 [{pattern_name}]")
        return True
        
    def get_applicable_patterns(self, sentence: str) -> List[BasePattern]:
        """
        文に適用可能なパターンを優先順序で取得
        
        Args:
            sentence: 対象文
            
        Returns:
            適用可能パターンのリスト（優先順序付き）
        """
        applicable_patterns = []
        
        for pattern_name, pattern in self.registered_patterns.items():
            if pattern.is_applicable(sentence):
                applicable_patterns.append((pattern_name, pattern))
                self.logger.debug(f"🎯 適用可能パターン検出: {pattern_name}")
                
        # 優先順序でソート
        applicable_patterns.sort(
            key=lambda x: self.pattern_priorities.get(x[0], 0),
            reverse=True
        )
        
        # パターンのみ返す
        pattern_list = [pattern for _, pattern in applicable_patterns]
        
        self.logger.debug(
            f"📋 適用可能パターン (優先順): "
            f"{[name for name, _ in applicable_patterns]}"
        )
        
        return pattern_list
        
    def get_pattern_by_name(self, pattern_name: str) -> Optional[BasePattern]:
        """
        名前でパターンを取得
        
        Args:
            pattern_name: パターン名
            
        Returns:
            パターンインスタンス（存在しない場合はNone）
        """
        return self.registered_patterns.get(pattern_name)
        
    def update_pattern_stats(self, pattern_name: str, success: bool):
        """
        パターン統計更新
        
        Args:
            pattern_name: パターン名
            success: 成功フラグ
        """
        if pattern_name in self.pattern_stats:
            stats = self.pattern_stats[pattern_name]
            stats['usage_count'] += 1
            if success:
                stats['success_count'] += 1
            stats['last_used'] = self._get_timestamp()
            
            success_rate = stats['success_count'] / stats['usage_count']
            self.logger.debug(
                f"📊 パターン統計更新 [{pattern_name}]: "
                f"使用回数={stats['usage_count']}, "
                f"成功率={success_rate:.3f}"
            )
            
    def get_pattern_stats(self) -> Dict[str, Dict]:
        """
        全パターンの統計取得
        
        Returns:
            パターン統計辞書
        """
        # 成功率を追加した統計
        enhanced_stats = {}
        for pattern_name, stats in self.pattern_stats.items():
            enhanced_stats[pattern_name] = stats.copy()
            if stats['usage_count'] > 0:
                enhanced_stats[pattern_name]['success_rate'] = (
                    stats['success_count'] / stats['usage_count']
                )
            else:
                enhanced_stats[pattern_name]['success_rate'] = 0.0
                
        return enhanced_stats
        
    def get_pattern_dependency_order(self) -> List[str]:
        """
        依存関係を考慮したパターン適用順序を取得
        
        Returns:
            依存関係順のパターン名リスト
        """
        # トポロジカルソート実装
        visited = set()
        temp_visited = set()
        result = []
        
        def dfs_visit(pattern_name: str):
            if pattern_name in temp_visited:
                raise ValueError(f"循環依存検出: {pattern_name}")
            if pattern_name in visited:
                return
                
            temp_visited.add(pattern_name)
            
            # 依存パターンを先に処理
            for dep in self.pattern_dependencies.get(pattern_name, []):
                if dep in self.registered_patterns:
                    dfs_visit(dep)
                    
            temp_visited.remove(pattern_name)
            visited.add(pattern_name)
            result.append(pattern_name)
            
        # 全パターンに対してDFS実行
        for pattern_name in self.registered_patterns.keys():
            if pattern_name not in visited:
                dfs_visit(pattern_name)
                
        self.logger.debug(f"🔗 依存関係順序: {result}")
        return result
        
    def _validate_dependencies(self, dependencies: List[str]) -> bool:
        """
        依存関係の妥当性チェック
        
        Args:
            dependencies: 依存パターンリスト
            
        Returns:
            妥当性フラグ
        """
        for dep in dependencies:
            if dep not in self.registered_patterns and dep not in self.pattern_priorities:
                self.logger.error(f"❌ 未登録依存パターン: {dep}")
                return False
        return True
        
    def _get_timestamp(self) -> str:
        """タイムスタンプ取得"""
        from datetime import datetime
        return datetime.now().isoformat()
        
    def list_registered_patterns(self) -> List[str]:
        """登録済みパターン一覧取得"""
        return list(self.registered_patterns.keys())
        
    def get_pattern_info(self, pattern_name: str) -> Optional[Dict]:
        """
        パターン詳細情報取得
        
        Args:
            pattern_name: パターン名
            
        Returns:
            パターン詳細情報（存在しない場合はNone）
        """
        if pattern_name not in self.registered_patterns:
            return None
            
        return {
            'name': pattern_name,
            'instance': self.registered_patterns[pattern_name],
            'priority': self.pattern_priorities[pattern_name],
            'dependencies': self.pattern_dependencies[pattern_name],
            'stats': self.pattern_stats[pattern_name]
        }
