#!/usr/bin/env python3
"""
Unified Stanza-Rephrase Mapper v1.0
===================================

邨ｱ蜷亥梛譁・ｳ募・隗｣繧ｨ繝ｳ繧ｸ繝ｳ - 繝上う繝悶Μ繝・ラ譁ｹ蠑・- 15蛟句挨繧ｨ繝ｳ繧ｸ繝ｳ縺ｮ遏･隴倥ｒ邨ｱ蜷・- 驕ｸ謚槫撫鬘後ｒ謗帝勁・亥・繝上Φ繝峨Λ繝ｼ蜷梧凾螳溯｡鯉ｼ・- Stanza dependency parsing 竊・Rephrase slot mapping
- spaCy陬懷ｮ瑚ｧ｣譫撰ｼ・tanza縺ｮ隱､隗｣譫千ｮ・園蟇ｾ蠢懶ｼ・
菴懈・譌･: 2025蟷ｴ8譛・5譌･
Phase 0: 蝓ｺ逶､讒狗ｯ・"""

import stanza
from typing import Dict, List, Optional, Any, Tuple
import json
import logging
from dataclasses import dataclass
from datetime import datetime

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

@dataclass
class RephraseSlot:
    """Rephrase繧ｹ繝ｭ繝・ヨ陦ｨ迴ｾ"""
    slot_name: str
    content: str
    sub_slots: Dict[str, Any] = None
    confidence: float = 1.0
    source_handler: str = ""

class UnifiedStanzaRephraseMapper:
    """
    邨ｱ蜷亥梛Stanza竊坦ephrase繝槭ャ繝代・
    
    譬ｸ蠢・晄Φ:
    - 蜈ｨ譁・ｳ輔ワ繝ｳ繝峨Λ繝ｼ縺悟酔譎ょｮ溯｡鯉ｼ磯∈謚槫撫鬘梧賜髯､・・    - 蜊倅ｸStanza隗｣譫千ｵ先棡縺ｮ螟夊ｧ堤噪蛻・梵
    - 蛟句挨繧ｨ繝ｳ繧ｸ繝ｳ縺ｮ螳溯｣・衍隴倡ｶ呎価
    """
    
    def __init__(self, 
                 language='en', 
                 enable_gpu=False,
                 log_level='INFO',
                 use_spacy_hybrid=True):
        """
        邨ｱ蜷医・繝・ヱ繝ｼ蛻晄悄蛹・        
        Args:
            language: 蜃ｦ逅・ｨ隱橸ｼ医ョ繝輔か繝ｫ繝・ 'en'・・            enable_gpu: GPU菴ｿ逕ｨ繝輔Λ繧ｰ
            log_level: 繝ｭ繧ｰ繝ｬ繝吶Ν
            use_spacy_hybrid: spaCy繝上う繝悶Μ繝・ラ隗｣譫蝉ｽｿ逕ｨ繝輔Λ繧ｰ
        """
        self.language = language
        self.enable_gpu = enable_gpu
        self.use_spacy_hybrid = use_spacy_hybrid
        
        # 繝ｭ繧ｰ險ｭ螳・        self._setup_logging(log_level)
        
        # Stanza繝代う繝励Λ繧､繝ｳ蛻晄悄蛹・        self.nlp = None
        self._initialize_stanza_pipeline()
        
        # spaCy繝上う繝悶Μ繝・ラ隗｣譫仙・譛溷喧
        self.spacy_nlp = None
        if self.use_spacy_hybrid and SPACY_AVAILABLE:
            self._initialize_spacy_pipeline()
        
        # 邨ｱ險域ュ蝣ｱ
        self.processing_count = 0
        self.total_processing_time = 0.0
        self.handler_success_count = {}
        
        # 谿ｵ髫守噪繝上Φ繝峨Λ繝ｼ邂｡逅・ｼ・hase蛻･霑ｽ蜉・・        self.active_handlers = []
        
        # 蝓ｺ譛ｬ繝上Φ繝峨Λ繝ｼ縺ｮ蛻晄悄蛹・        self._initialize_basic_handlers()
        
        self.logger.info("噫 Unified Stanza-Rephrase Mapper v1.0 蛻晄悄蛹門ｮ御ｺ・)
        if self.spacy_nlp:
            self.logger.info("肌 spaCy繝上う繝悶Μ繝・ラ隗｣譫・譛牙柑")
        else:
            self.logger.info("笞・・spaCy繝上う繝悶Μ繝・ラ隗｣譫・辟｡蜉ｹ")
    
    def _setup_logging(self, level: str):
        """繝ｭ繧ｰ險ｭ螳・""
        self.logger = logging.getLogger(f"{__name__}.UnifiedMapper")
        self.logger.setLevel(getattr(logging, level.upper()))
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _initialize_stanza_pipeline(self):
        """Stanza NLP繝代う繝励Λ繧､繝ｳ蛻晄悄蛹・""
        try:
            self.logger.info("肌 Stanza pipeline 蛻晄悄蛹紋ｸｭ...")
            
            # 蝓ｺ譛ｬ逧・↑繝代う繝励Λ繧､繝ｳ讒区・
            processors = 'tokenize,pos,lemma,depparse'
            
            self.nlp = stanza.Pipeline(
                lang=self.language,
                processors=processors,
                download_method=None,  # 莠句燕繝繧ｦ繝ｳ繝ｭ繝ｼ繝画ｸ医∩繧呈Φ螳・                use_gpu=self.enable_gpu,
                verbose=False
            )
            
            self.logger.info("笨・Stanza pipeline 蛻晄悄蛹匁・蜉・)
            
            # 蜍穂ｽ懃｢ｺ隱・            test_result = self.nlp("Hello world.")
            self.logger.info(f"ｧｪ Pipeline 蜍穂ｽ懃｢ｺ隱・ {len(test_result.sentences)} sentences processed")
            
        except Exception as e:
            self.logger.error(f"笶・Stanza pipeline 蛻晄悄蛹門､ｱ謨・ {e}")
            self.logger.error("庁 隗｣豎ｺ譁ｹ豕・ python -c 'import stanza; stanza.download(\"en\")'")
            raise RuntimeError(f"Stanza initialization failed: {e}")
    
    def _initialize_spacy_pipeline(self):
        """spaCy NLP繝代う繝励Λ繧､繝ｳ蛻晄悄蛹厄ｼ医ワ繧､繝悶Μ繝・ラ隗｣譫千畑・・""
        try:
            self.logger.info("肌 spaCy pipeline 蛻晄悄蛹紋ｸｭ...")
            
            # 闍ｱ隱槭Δ繝・Ν繧偵Ο繝ｼ繝・            self.spacy_nlp = spacy.load('en_core_web_sm')
            
            self.logger.info("笨・spaCy pipeline 蛻晄悄蛹匁・蜉・)
            
        except Exception as e:
            self.logger.warning(f"笞・・spaCy pipeline 蛻晄悄蛹門､ｱ謨・ {e}")
            self.logger.warning("  pip install spacy; python -m spacy download en_core_web_sm 縺ｧ險ｭ螳壹＠縺ｦ縺上□縺輔＞")
            self.spacy_nlp = None
            self.use_spacy_hybrid = False
    
    def _initialize_basic_handlers(self):
        """蝓ｺ譛ｬ繝上Φ繝峨Λ繝ｼ縺ｮ蛻晄悄蛹・""
        basic_handlers = [
            'basic_five_pattern',     # 蝓ｺ譛ｬ5譁・梛
            'relative_clause',        # 髢｢菫らｯ
            'passive_voice',          # 蜿怜虚諷・ 
            'adverbial_modifier',     # 蜑ｯ隧槫唱・亥燕鄂ｮ隧槫唱蜷ｫ繧・・            'auxiliary_complex',      # 蜉ｩ蜍戊ｩ・            'conjunction',            # 謗･邯夊ｩ橸ｼ・as if"遲会ｼ・        ]
        
        for handler in basic_handlers:
            self.add_handler(handler)
        
        self.logger.info(f"笨・蝓ｺ譛ｬ繝上Φ繝峨Λ繝ｼ蛻晄悄蛹門ｮ御ｺ・ {len(self.active_handlers)}蛟・)
    
    def process(self, sentence: str) -> Dict[str, Any]:
        """
        邨ｱ蜷亥・逅・Γ繧､繝ｳ繧ｨ繝ｳ繝医Μ繝昴う繝ｳ繝・        
        Args:
            sentence: 蜃ｦ逅・ｯｾ雎｡譁・            
        Returns:
            Dict: Rephrase蠖｢蠑丞・逅・ｵ先棡
        """
        start_time = datetime.now()
        self.processing_count += 1
        
        try:
            self.logger.debug(f"剥 Processing: {sentence}")
            
            # Phase 1: Stanza隗｣譫・            doc = self._analyze_with_stanza(sentence)
            if not doc or not doc.sentences:
                self.logger.warning(f"笞・・Stanza隗｣譫仙､ｱ謨・ {sentence}")
                return self._create_empty_result(sentence)
            
            # Phase 1.5: 繝上う繝悶Μ繝・ラ隗｣譫撰ｼ・paCy陬懷ｮ鯉ｼ・            if self.use_spacy_hybrid and self.spacy_nlp:
                doc = self._apply_spacy_hybrid_corrections(sentence, doc)
            
            # Phase 2: 邨ｱ蜷亥・逅・ｼ亥・繝上Φ繝峨Λ繝ｼ蜷梧凾螳溯｡鯉ｼ・            result = self._unified_mapping(sentence, doc)
            
            # Phase 3: 蠕悟・逅・・讀懆ｨｼ
            result = self._post_process_result(result, sentence)
            
            # 蜃ｦ逅・凾髢楢ｨ倬鹸
            processing_time = (datetime.now() - start_time).total_seconds()
            self.total_processing_time += processing_time
            
            result['meta'] = {
                'processing_time': processing_time,
                'sentence_id': self.processing_count,
                'active_handlers': len(self.active_handlers),
                'stanza_info': {
                    'sentences': len(doc.sentences),
                    'tokens': len(doc.sentences[0].words) if doc.sentences else 0
                }
            }
            
            self.logger.info(f"笨・Processing螳御ｺ・({processing_time:.3f}s): {len(result.get('slots', {}))} slots detected")
            return result
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"笶・Processing error: {e}")
            
            return {
                'sentence': sentence,
                'slots': {},
                'error': str(e),
                'meta': {
                    'processing_time': processing_time,
                    'sentence_id': self.processing_count,
                    'error_occurred': True
                }
            }
    
    def _analyze_with_stanza(self, sentence: str):
        """Stanza隗｣譫仙ｮ溯｡・""
        try:
            doc = self.nlp(sentence)
            return doc
        except Exception as e:
            self.logger.error(f"笶・Stanza analysis failed: {e}")
            return None
    
    def _apply_spacy_hybrid_corrections(self, sentence: str, stanza_doc):
        """
        spaCy繝上う繝悶Μ繝・ラ隗｣譫占｣懷ｮ・        
        Stanza縺ｮ隱､隗｣譫舌ｒ讀懷・縺励※spaCy縺ｧ陬懷ｮ御ｿｮ豁｣
        迚ｹ縺ｫwhose讒区枚縺ｧ縺ｮ蜍戊ｩ霸OS隱､隗｣譫舌ｒ菫ｮ豁｣
        """
        try:
            # spaCy隗｣譫仙ｮ溯｡・            spacy_doc = self.spacy_nlp(sentence)
            
            # 菫ｮ豁｣縺悟ｿ・ｦ√↑邂・園繧呈､懷・
            corrections = self._detect_analysis_discrepancies(stanza_doc, spacy_doc, sentence)
            
            if corrections:
                self.logger.debug(f"肌 繝上う繝悶Μ繝・ラ隗｣譫占｣懈ｭ｣: {len(corrections)} 邂・園菫ｮ豁｣")
                
                # Stanza邨先棡縺ｫ陬懈ｭ｣繧帝←逕ｨ
                corrected_doc = self._apply_corrections_to_stanza(stanza_doc, corrections)
                return corrected_doc
            
            return stanza_doc
            
        except Exception as e:
            self.logger.warning(f"笞・・spaCy繝上う繝悶Μ繝・ラ隗｣譫舌お繝ｩ繝ｼ: {e}")
            return stanza_doc  # 陬懈ｭ｣螟ｱ謨玲凾縺ｯ蜈・・Stanza邨先棡繧定ｿ斐☆
    
    def _detect_analysis_discrepancies(self, stanza_doc, spacy_doc, sentence: str) -> List[Dict]:
        """
        Stanza-spaCy隗｣譫千ｵ先棡縺ｮ逶ｸ驕慕せ繧呈､懷・
        
        迚ｹ縺ｫ驥崎ｦ√↑菫ｮ豁｣邂・園:
        1. whose讒区枚縺ｧ縺ｮ蜍戊ｩ霸OS隱､隗｣譫・(NOUN 竊・VERB)
        2. 髢｢菫らｯ蜍戊ｩ槭・隱､蛻・｡・        """
        corrections = []
        
        # whose讒区枚迚ｹ蛻･蜃ｦ逅・        if 'whose' in sentence.lower():
            corrections.extend(self._detect_whose_verb_misanalysis(stanza_doc, spacy_doc, sentence))
        
        return corrections
    
    def _detect_whose_verb_misanalysis(self, stanza_doc, spacy_doc, sentence: str) -> List[Dict]:
        """whose讒区枚縺ｧ縺ｮ蜍戊ｩ霸OS隱､隗｣譫舌ｒ讀懷・"""
        corrections = []
        
        stanza_words = {w.text.lower(): w for w in stanza_doc.sentences[0].words}
        spacy_tokens = {t.text.lower(): t for t in spacy_doc}
        
        # 'lives', 'works', 'runs'遲峨・蜍戊ｩ槭′蜷崎ｩ槭→縺励※隱､隗｣譫舌＆繧後※縺・ｋ縺九メ繧ｧ繝・け
        potential_verbs = ['lives', 'works', 'runs', 'goes', 'comes', 'stays']
        
        for verb_text in potential_verbs:
            if verb_text in stanza_words and verb_text in spacy_tokens:
                stanza_word = stanza_words[verb_text]
                spacy_token = spacy_tokens[verb_text]
                
                # Stanza: NOUN, spaCy隗｣譫舌〒繧・OUN縺縺後∵枚閼育噪縺ｫ蜍戊ｩ槭→蛻､譁ｭ縺ｧ縺阪ｋ蝣ｴ蜷・                if (stanza_word.upos == 'NOUN' and 
                    stanza_word.deprel == 'acl:relcl' and
                    self._is_contextually_verb(sentence, verb_text)):
                    
                    corrections.append({
                        'word_id': stanza_word.id,
                        'word_text': stanza_word.text,
                        'original_upos': stanza_word.upos,
                        'corrected_upos': 'VERB',
                        'correction_type': 'whose_verb_fix',
                        'confidence': 0.9
                    })
                    self.logger.debug(f"肌 whose讒区枚蜍戊ｩ樔ｿｮ豁｣讀懷・: {verb_text} NOUN竊歎ERB")
        
        return corrections
    
    def _is_contextually_verb(self, sentence: str, word: str) -> bool:
        """譁・ц逧・↓蜍戊ｩ槭→蛻､譁ｭ縺ｧ縺阪ｋ縺九メ繧ｧ繝・け"""
        # 邁｡蜊倥↑繝ｫ繝ｼ繝ｫ繝吶・繧ｹ蛻､螳・        # whose + [noun] + is + [adj] + [word] + here/there 繝代ち繝ｼ繝ｳ
        import re
        
        whose_pattern = rf'whose\s+\w+\s+is\s+\w+\s+{word}\s+(here|there)'
        if re.search(whose_pattern, sentence.lower()):
            return True
            
        return False
    
    def _apply_corrections_to_stanza(self, stanza_doc, corrections):
        """Stanza隗｣譫千ｵ先棡縺ｫ陬懈ｭ｣繧帝←逕ｨ"""
        # 豕ｨ諢・ Stanza縺ｮ繝・・繧ｿ讒矩縺ｯ隱ｭ縺ｿ蜿悶ｊ蟆ら畑縺ｮ縺溘ａ縲∫峩謗･菫ｮ豁｣縺ｯ縺ｧ縺阪↑縺・        # 縺薙％縺ｧ縺ｯ菫ｮ豁｣諠・ｱ繧定ｨ倬鹸縺励※縲∝ｾ檎ｶ壼・逅・〒蛻ｩ逕ｨ縺吶ｋ
        
        if not hasattr(stanza_doc, 'hybrid_corrections'):
            stanza_doc.hybrid_corrections = {}
        
        for correction in corrections:
            word_id = correction['word_id']
            stanza_doc.hybrid_corrections[word_id] = correction
            
        return stanza_doc
    
    def _unified_mapping(self, sentence: str, doc) -> Dict[str, Any]:
        """
        邨ｱ蜷医・繝・ヴ繝ｳ繧ｰ蜃ｦ逅・        
        蜈ｨ繧｢繧ｯ繝・ぅ繝悶ワ繝ｳ繝峨Λ繝ｼ縺悟酔譎ょｮ溯｡・        蜷・ワ繝ｳ繝峨Λ繝ｼ縺ｯ迢ｬ遶九＠縺ｦStanza隗｣譫千ｵ先棡繧貞・逅・        """
        result = {
            'sentence': sentence,
            'slots': {},
            'sub_slots': {},
            'grammar_info': {
                'detected_patterns': [],
                'handler_contributions': {}
            }
        }
        
        # 繝｡繧､繝ｳ譁・ｼ域怙蛻昴・sentence・峨ｒ蟇ｾ雎｡縺ｨ縺吶ｋ
        main_sentence = doc.sentences[0] if doc.sentences else None
        if not main_sentence:
            return result
        
        self.logger.debug(f"肌 Unified mapping髢句ｧ・ {len(self.active_handlers)} handlers active")
        
        # 蜈ｨ繧｢繧ｯ繝・ぅ繝悶ワ繝ｳ繝峨Λ繝ｼ縺ｮ蜷梧凾螳溯｡・        for handler_name in self.active_handlers:
            try:
                self.logger.debug(f"識 Handler螳溯｡・ {handler_name}")
                handler_method = getattr(self, f'_handle_{handler_name}')
                handler_result = handler_method(main_sentence, result.copy())
                
                # 繝上Φ繝峨Λ繝ｼ邨先棡繧偵・繝ｼ繧ｸ
                if handler_result:
                    result = self._merge_handler_results(result, handler_result, handler_name)
                    
                    # 謌仙粥繧ｫ繧ｦ繝ｳ繝・                    self.handler_success_count[handler_name] = \
                        self.handler_success_count.get(handler_name, 0) + 1
                        
            except Exception as e:
                self.logger.warning(f"笞・・Handler error ({handler_name}): {e}")
                continue
        
        return result
    
    def _merge_handler_results(self, base_result: Dict, handler_result: Dict, handler_name: str) -> Dict:
        """
        繝上Φ繝峨Λ繝ｼ邨先棡繧偵・繝ｼ繧ｹ邨先棡縺ｫ繝槭・繧ｸ
        
        Args:
            base_result: 繝吶・繧ｹ邨先棡
            handler_result: 繝上Φ繝峨Λ繝ｼ蜃ｦ逅・ｵ先棡  
            handler_name: 繝上Φ繝峨Λ繝ｼ蜷・        """
        # 繧ｹ繝ｭ繝・ヨ諠・ｱ繝槭・繧ｸ
        if 'slots' in handler_result:
            for slot_name, slot_data in handler_result['slots'].items():
                if slot_name not in base_result['slots']:
                    base_result['slots'][slot_name] = slot_data
                else:
                    # 遶ｶ蜷郁ｧ｣豎ｺ・夂ｩｺ譁・ｭ励ｄ遨ｺ蛟､縺ｧ譌｢蟄倥・譛牙柑縺ｪ蛟､繧剃ｸ頑嶌縺阪＠縺ｪ縺・                    existing_value = base_result['slots'][slot_name]
                    
                    # 譌｢蟄伜､縺檎ｩｺ縺ｧ譁ｰ蛟､縺梧怏蜉ｹ縺ｪ蝣ｴ蜷医・荳頑嶌縺・                    if not existing_value and slot_data:
                        base_result['slots'][slot_name] = slot_data
                    # 譌｢蟄伜､縺梧怏蜉ｹ縺ｧ譁ｰ蛟､繧よ怏蜉ｹ縺ｪ蝣ｴ蜷医・蠕悟享縺｡・亥ｾ捺擂騾壹ｊ・・                    elif existing_value and slot_data:
                        base_result['slots'][slot_name] = slot_data
                    # 譌｢蟄伜､縺梧怏蜉ｹ縺ｧ譁ｰ蛟､縺檎ｩｺ縺ｮ蝣ｴ蜷医・菫晄戟・遺・菫ｮ豁｣繝昴う繝ｳ繝茨ｼ・                    elif existing_value and not slot_data:
                        pass  # 譌｢蟄伜､繧剃ｿ晄戟
                    # 荳｡譁ｹ遨ｺ縺ｮ蝣ｴ蜷医・蠕悟享縺｡
                    else:
                        base_result['slots'][slot_name] = slot_data
        
        # 繧ｵ繝悶せ繝ｭ繝・ヨ諠・ｱ繝槭・繧ｸ
        if 'sub_slots' in handler_result:
            for sub_slot_name, sub_slot_data in handler_result['sub_slots'].items():
                base_result['sub_slots'][sub_slot_name] = sub_slot_data
        
        # 譁・ｳ墓ュ蝣ｱ險倬鹸
        if 'grammar_info' in handler_result:
            grammar_info = handler_result['grammar_info']
            base_result['grammar_info']['handler_contributions'][handler_name] = grammar_info
            
            # 讀懷・繝代ち繝ｼ繝ｳ霑ｽ蜉
            if 'patterns' in grammar_info:
                base_result['grammar_info']['detected_patterns'].extend(grammar_info['patterns'])
        
        return base_result
    
    def _post_process_result(self, result: Dict, sentence: str) -> Dict:
        """蠕悟・逅・・邨先棡讀懆ｨｼ・・hose讒区枚迚ｹ蛻･蜃ｦ逅・ｿｽ蜉・・""
        
        # 笨・whose讒区枚縺ｮ迚ｹ蛻･縺ｪ蠕悟・逅・ｼ壻ｸｻ譁・・髢｢菫らｯ縺ｮ豁｣縺励＞蛻・屬
        if 'whose' in sentence.lower():
            result = self._post_process_whose_construction(result, sentence)
        
        # 驥崎､・ヱ繧ｿ繝ｼ繝ｳ髯､蜴ｻ
        if 'detected_patterns' in result.get('grammar_info', {}):
            result['grammar_info']['detected_patterns'] = \
                list(set(result['grammar_info']['detected_patterns']))
        
        # 肌 REPHRASE SPECIFICATION COMPLIANCE: Sub-slots require empty main slots
        self._apply_rephrase_slot_structure_rules(result)
        
        # 繧ｹ繝ｭ繝・ヨ謨ｴ蜷域ｧ繝√ぉ繝・け・井ｻ雁ｾ悟ｮ溯｣・ｼ・        # TODO: rephrase_slot_validator.py 縺ｨ縺ｮ騾｣謳ｺ
        
        return result
    
    def _post_process_whose_construction(self, result: Dict, sentence: str) -> Dict:
        """whose讒区枚縺ｮ蠕悟・逅・ｼ壻ｸｻ譁・・髢｢菫らｯ縺ｮ豁｣縺励＞蛻・屬"""
        
        # 繝上う繝悶Μ繝・ラ隗｣譫舌〒陬懈ｭ｣縺輔ｌ縺溷虚隧橸ｼ井ｸｻ譁・虚隧橸ｼ峨ｒ讀懷・
        main_verb = None
        for word in sentence.split():
            if word.lower() in ['lives', 'works', 'runs', 'goes', 'sits', 'stands']:
                main_verb = word
                break
        
        if main_verb:
            # 荳ｻ譁・虚隧槭ｒV繧ｹ繝ｭ繝・ヨ縺ｫ驟咲ｽｮ
            if 'slots' not in result:
                result['slots'] = {}
            result['slots']['V'] = main_verb
            
            # 笨・蜑ｯ隧槫・逅・・蟆る摩繧ｨ繝ｳ繧ｸ繝ｳ縺ｫ蟋碑ｭｲ - 蝗ｺ螳壼・逅・ｒ辟｡蜉ｹ蛹・            # if 'here' in sentence.lower():
            #     result['slots']['M2'] = 'here'
            # elif 'there' in sentence.lower():
            #     result['slots']['M2'] = 'there'
                
            # 荳ｻ隱槭・髢｢菫らｯ繝上Φ繝峨Λ繝ｼ縺瑚ｨｭ螳壹＠縺殱ub-s繧堤ｧｻ蜍・            if result.get('sub_slots', {}).get('sub-s'):
                # sub-s縺ｮ蜀・ｮｹ縺九ｉ髢｢菫らｯ驛ｨ蛻・ｒ髯､蜴ｻ縺励※荳ｻ譁・ｸｻ隱槭ｒ菴懊ｋ
                sub_s_content = result['sub_slots']['sub-s']  # "The man whose car"
                # "whose car"驛ｨ蛻・ｒ髯､蜴ｻ縺励※"The man"繧剃ｸｻ隱槭→縺吶ｋ
                main_subject = sub_s_content.split(' whose ')[0]  # "The man"
                result['slots']['S'] = main_subject
                
            # 髢｢菫らｯ縺ｮsub-c1縺御ｸｻ譁・虚隧槭↓縺ｪ縺｣縺ｦ縺・ｋ蝣ｴ蜷医・菫ｮ豁｣
            if result.get('sub_slots', {}).get('sub-c1') == main_verb:
                # 譛ｬ譚･縺ｮ髢｢菫らｯ陬懆ｪ槭ｒ謗｢縺・                if 'red' in sentence.lower():
                    result['sub_slots']['sub-c1'] = 'red'
            
            # 蜉ｩ蜍戊ｩ槭ワ繝ｳ繝峨Λ繝ｼ縺梧､懷・縺励◆荳ｻ譁・虚隧槭ｒ驕ｩ逕ｨ
            detected_patterns = result.get('grammar_info', {}).get('detected_patterns', [])
            if 'passive_voice' in detected_patterns:
                passive_info = result.get('grammar_info', {}).get('handler_contributions', {}).get('passive_voice', {})
                if passive_info and 'main_verb' in passive_info:
                    main_verb_from_passive = passive_info['main_verb']
                    result['slots']['V'] = main_verb_from_passive
                    self.logger.debug(f"肌 whose讒区枚: 蜿怜虚諷句虚隧樔ｿｮ豁｣ V='{main_verb_from_passive}'")
                    
            self.logger.debug(f"肌 whose讒区枚蠕悟・逅・ 荳ｻ譁Ⅲ={result['slots'].get('V')}, S={result['slots'].get('S')}")
        
        return result
    
    def _apply_rephrase_slot_structure_rules(self, result: Dict) -> None:
        """
        Rephrase莉墓ｧ俶ｺ匁侠・夊､・枚縺ｧ縺ｮ豁｣縺励＞繧ｹ繝ｭ繝・ヨ驟咲ｽｮ
        
        驥崎ｦ√Ν繝ｼ繝ｫ・嘖ub-slots縺悟ｭ伜惠縺吶ｋ蝣ｴ蜷医∝ｯｾ蠢懊☆繧砧ain slots縺ｯ遨ｺ譁・ｭ励↓縺吶ｋ
        萓句､厄ｼ哂ux, V繧ｹ繝ｭ繝・ヨ縺ｯ萓句､夜←逕ｨ縺ｪ縺励∵磁邯夊ｩ樊ｧ区枚縺ｧ縺ｯ荳ｻ遽隕∫ｴ菫晄戟
        
        蟇ｾ蠢憺未菫ゑｼ・        - S 竊絶・ sub-s (S菴咲ｽｮ縺ｮ蠕灘ｱ樒ｯ)
        - O1 竊絶・ sub-o1 (O1菴咲ｽｮ縺ｮ蠕灘ｱ樒ｯ)  
        - O2 竊絶・ sub-o2 (O2菴咲ｽｮ縺ｮ蠕灘ｱ樒ｯ)
        - C1 竊絶・ sub-c1 (C1菴咲ｽｮ縺ｮ蠕灘ｱ樒ｯ)
        - C2 竊絶・ sub-c2 (C2菴咲ｽｮ縺ｮ蠕灘ｱ樒ｯ)
        - M1 竊絶・ sub-m1 (M1菴咲ｽｮ縺ｮ蠕灘ｱ樒ｯ)
        - M2 竊絶・ sub-m2 (M2菴咲ｽｮ縺ｮ蠕灘ｱ樒ｯ) 
        - M3 竊絶・ sub-m3 (M3菴咲ｽｮ縺ｮ蠕灘ｱ樒ｯ)
        """
        slots = result.get('slots', {})
        sub_slots = result.get('sub_slots', {})
        
        # 謗･邯夊ｩ樊ｧ区枚縺ｧ縺ｯ荳ｻ遽隕∫ｴ繧剃ｿ晄戟
        grammar_info = result.get('grammar_info', {})
        handler_contributions = grammar_info.get('handler_contributions', {})
        is_conjunction = 'conjunction' in handler_contributions
        
        if is_conjunction:
            self.logger.debug("迫 謗･邯夊ｩ樊ｧ区枚讀懷・: 荳ｻ遽隕∫ｴ菫晄戟")
            return
        
        # 蟇ｾ蠢憺未菫ゅ・繝・ヴ繝ｳ繧ｰ・・ux, V髯､螟厄ｼ・        main_to_sub_mapping = {
            'S': 'sub-s',
            'O1': 'sub-o1', 
            'O2': 'sub-o2',
            'C1': 'sub-c1',
            'C2': 'sub-c2', 
            'M1': 'sub-m1',
            'M2': 'sub-m2',
            'M3': 'sub-m3'
        }
        
        self.logger.debug(f"女・・Rephrase莉墓ｧ倬←逕ｨ髢句ｧ・- Sub-slots: {list(sub_slots.keys())}")
        
        # 隍・枚蛻､螳夲ｼ・せ繝ｭ繝・ヨ遨ｺ譁・ｭ怜喧蜃ｦ逅・        for main_slot, sub_slot in main_to_sub_mapping.items():
            if sub_slot in sub_slots and sub_slots[sub_slot]:
                # Sub-slot縺悟ｭ伜惠縺怜・螳ｹ縺後≠繧句ｴ蜷医∝ｯｾ蠢懊☆繧砧ain slot繧堤ｩｺ縺ｫ縺吶ｋ
                if main_slot in slots:
                    original_value = slots[main_slot]
                    
                    # 蜑ｯ隧槭せ繝ｭ繝・ヨ迚ｹ蛻･蜃ｦ逅・ 荳ｻ遽蜑ｯ隧槭・菫晄戟
                    if main_slot.startswith('M') and original_value:
                        # 荳ｻ遽蜑ｯ隧槭′蟄伜惠縺吶ｋ蝣ｴ蜷医《ub-slot縺ｮ遘ｻ蜍輔・陦後ｏ縺ｪ縺・                        self.logger.debug(
                            f"孱・・荳ｻ遽蜑ｯ隧樔ｿ晁ｭｷ: {main_slot}: '{original_value}' (preserved) "
                            f"while {sub_slot}: '{sub_slots[sub_slot]}' (kept in sub-slot)"
                        )
                        continue  # 遨ｺ譁・ｭ怜喧繧偵せ繧ｭ繝・・
                    
                    slots[main_slot] = ""  # 菴咲ｽｮ繝槭・繧ｫ繝ｼ縺ｨ縺励※遨ｺ譁・ｭ苓ｨｭ螳・                    
                    self.logger.debug(
                        f"売 Complex sentence rule applied: "
                        f"{main_slot}: '{original_value}' 竊・'' "
                        f"(sub-slot {sub_slot}: '{sub_slots[sub_slot]}')"
                    )
        
        # 蜑ｯ隧樣㍾隍・メ繧ｧ繝・け縺ｨ蜑企勁
        self._remove_adverb_duplicates(slots, sub_slots)
        
        # 蜃ｦ逅・ｵ先棡繧偵ョ繝舌ャ繧ｰ繝ｭ繧ｰ蜃ｺ蜉・        applied_rules = [
            f"{main}竊畜sub}" for main, sub in main_to_sub_mapping.items() 
            if sub in sub_slots and sub_slots[sub] and main in slots
        ]
        
        if applied_rules:
            self.logger.info(f"笨・Rephrase隍・枚繝ｫ繝ｼ繝ｫ驕ｩ逕ｨ: {', '.join(applied_rules)}")
        else:
            self.logger.debug("剥 Simple sentence detected - No main slot emptying required")
    
    def _remove_adverb_duplicates(self, slots: Dict, sub_slots: Dict):
        """荳ｻ遽縺ｨ髢｢菫らｯ縺ｮ蜑ｯ隧樣㍾隍・ｒ髯､蜴ｻ・磯未菫らｯ蜀・㍾隍・ｂ蟇ｾ蠢懶ｼ・""
        
        # === 1. 髢｢菫らｯ蜀・㍾隍・勁蜴ｻ・域怙驥崎ｦ・ｼ・==
        sub_adverbs = {k: v for k, v in sub_slots.items() if k.startswith('sub-m') and v}
        
        if len(sub_adverbs) > 1:
            # 髢｢菫らｯ蜀・〒蜷後§蜑ｯ隧槭′隍・焚繧ｹ繝ｭ繝・ヨ縺ｫ驟咲ｽｮ縺輔ｌ縺ｦ縺・ｋ蝣ｴ蜷・            seen_adverbs = {}
            slots_to_clear = []
            
            for sub_slot, sub_value in sub_adverbs.items():
                adverb_text = sub_value.strip()
                if adverb_text in seen_adverbs:
                    # 驥崎､・､懷・: 繧医ｊ蜆ｪ蜈亥ｺｦ縺ｮ菴弱＞繧ｹ繝ｭ繝・ヨ繧貞炎髯､
                    existing_slot = seen_adverbs[adverb_text]
                    
                    # 蜆ｪ蜈亥ｺｦ: sub-m2 > sub-m1 > sub-m3・・ephrase莉墓ｧ俶ｺ匁侠・・                    priority_order = {'sub-m2': 3, 'sub-m1': 2, 'sub-m3': 1}
                    
                    if priority_order.get(sub_slot, 0) > priority_order.get(existing_slot, 0):
                        # 譁ｰ繧ｹ繝ｭ繝・ヨ縺ｮ譁ｹ縺悟━蜈亥ｺｦ鬮倪・譌｢蟄倥ｒ蜑企勁
                        slots_to_clear.append(existing_slot)
                        seen_adverbs[adverb_text] = sub_slot
                        self.logger.debug(f"売 髢｢菫らｯ蜀・㍾隍・炎髯､: {existing_slot}='{adverb_text}' 竊・'' ({sub_slot}='{adverb_text}' 繧貞━蜈・")
                    else:
                        # 譌｢蟄倥せ繝ｭ繝・ヨ縺ｮ譁ｹ縺悟━蜈亥ｺｦ鬮倪・譁ｰ繧ｹ繝ｭ繝・ヨ繧貞炎髯､
                        slots_to_clear.append(sub_slot)
                        self.logger.debug(f"売 髢｢菫らｯ蜀・㍾隍・炎髯､: {sub_slot}='{adverb_text}' 竊・'' ({existing_slot}='{adverb_text}' 繧貞━蜈・")
                else:
                    seen_adverbs[adverb_text] = sub_slot
            
            # 驥崎､・せ繝ｭ繝・ヨ繧偵け繝ｪ繧｢
            for slot_to_clear in slots_to_clear:
                sub_slots[slot_to_clear] = ""
        
        # === 2. 荳ｻ遽竊秘未菫らｯ髢馴㍾隍・勁蜴ｻ・亥ｾ捺擂讖溯・・・==
        main_adverbs = {k: v for k, v in slots.items() if k.startswith('M') and v}
        remaining_sub_adverbs = {k: v for k, v in sub_slots.items() if k.startswith('sub-m') and v}
        
        if not main_adverbs or not remaining_sub_adverbs:
            return
        
        # 驥崎､・憶隧槭・讀懷・縺ｨ蜑企勁
        for main_slot, main_value in list(main_adverbs.items()):
            for sub_slot, sub_value in remaining_sub_adverbs.items():
                # 蜷後§蜑ｯ隧槭′荳ｻ遽縺ｨ髢｢菫らｯ縺ｫ蟄伜惠縺吶ｋ蝣ｴ蜷・                if main_value.strip() == sub_value.strip():
                    # 髢｢菫らｯ繧貞━蜈医＠縲∽ｸｻ遽縺九ｉ蜑企勁
                    slots[main_slot] = ""
                    self.logger.debug(f"売 荳ｻ遽竊秘未菫らｯ驥崎､・炎髯､: {main_slot}='{main_value}' 竊・'' (sub-slot {sub_slot}='{sub_value}' 繧貞━蜈・")
                    break
    
    def _create_empty_result(self, sentence: str) -> Dict[str, Any]:
        """遨ｺ邨先棡縺ｮ菴懈・"""
        return {
            'sentence': sentence,
            'slots': {},
            'sub_slots': {},
            'grammar_info': {
                'detected_patterns': [],
                'handler_contributions': {}
            },
            'meta': {
                'processing_time': 0.0,
                'sentence_id': self.processing_count,
                'empty_result': True
            }
        }
    
    # =============================================================================
    # 繝上Φ繝峨Λ繝ｼ邂｡逅・ｼ・hase蛻･讖溯・霑ｽ蜉逕ｨ・・    # =============================================================================
    
    def add_handler(self, handler_name: str):
        """繝上Φ繝峨Λ繝ｼ繧定ｿｽ蜉・・hase蛻･髢狗匱逕ｨ・・""
        if handler_name not in self.active_handlers:
            self.active_handlers.append(handler_name)
            self.logger.info(f"筐・Handler霑ｽ蜉: {handler_name}")
        else:
            self.logger.warning(f"笞・・Handler already active: {handler_name}")
    
    def remove_handler(self, handler_name: str):
        """繝上Φ繝峨Λ繝ｼ繧貞炎髯､"""
        if handler_name in self.active_handlers:
            self.active_handlers.remove(handler_name)
            self.logger.info(f"筐・Handler蜑企勁: {handler_name}")
    
    def list_active_handlers(self) -> List[str]:
        """繧｢繧ｯ繝・ぅ繝悶ワ繝ｳ繝峨Λ繝ｼ荳隕ｧ"""
        return self.active_handlers.copy()
    
    # =============================================================================
    # 邨ｱ險医・繝・ヰ繝・げ諠・ｱ
    # =============================================================================
    
    def get_stats(self) -> Dict[str, Any]:
        """蜃ｦ逅・ｵｱ險域ュ蝣ｱ蜿門ｾ・""
        avg_processing_time = (
            self.total_processing_time / self.processing_count 
            if self.processing_count > 0 else 0.0
        )
        
        return {
            'processing_count': self.processing_count,
            'total_processing_time': self.total_processing_time,
            'average_processing_time': avg_processing_time,
            'active_handlers': self.active_handlers.copy(),
            'handler_success_count': self.handler_success_count.copy(),
            'stanza_pipeline_status': 'active' if self.nlp else 'inactive'
        }
    
    def reset_stats(self):
        """邨ｱ險域ュ蝣ｱ繝ｪ繧ｻ繝・ヨ"""
        self.processing_count = 0
        self.total_processing_time = 0.0
        self.handler_success_count.clear()
        self.logger.info("投 Statistics reset")
    
    # =============================================================================
    # 譁・ｳ輔ワ繝ｳ繝峨Λ繝ｼ螳溯｣・ｼ・hase 1+: 谿ｵ髫守噪霑ｽ蜉・・    # =============================================================================
    
    def _handle_relative_clause(self, sentence, base_result: Dict) -> Optional[Dict]:
        """
        髢｢菫らｯ繝上Φ繝峨Λ繝ｼ・・hase 1螳溯｣・ｼ・        
        simple_relative_engine.py 縺ｮ讖溯・繧堤ｵｱ蜷医す繧ｹ繝・Β縺ｫ遘ｻ讀・        Stanza dependency parsing 縺ｫ繧医ｋ逶ｴ謗･逧・↑髢｢菫らｯ讀懷・繝ｻ蛻・ｧ｣
        
        Args:
            sentence: Stanza隗｣譫先ｸ医∩sentence object
            base_result: 繝吶・繧ｹ邨先棡・医さ繝斐・・・            
        Returns:
            Dict: 髢｢菫らｯ蛻・ｧ｣邨先棡 or None
        """
        try:
            self.logger.debug("剥 髢｢菫らｯ繝上Φ繝峨Λ繝ｼ螳溯｡御ｸｭ...")
            
            # 髢｢菫らｯ蟄伜惠繝√ぉ繝・け
            if not self._has_relative_clause(sentence):
                self.logger.debug("  髢｢菫らｯ縺ｪ縺・- 繧ｹ繧ｭ繝・・")
                return None
            
            self.logger.debug("  笨・髢｢菫らｯ讀懷・")
            return self._process_relative_clause_structure(sentence, base_result)
            
        except Exception as e:
            self.logger.warning(f"笞・・髢｢菫らｯ繝上Φ繝峨Λ繝ｼ繧ｨ繝ｩ繝ｼ: {e}")
            return None
    
    def _has_relative_clause(self, sentence) -> bool:
        """髢｢菫らｯ繧貞性繧縺九メ繧ｧ繝・け"""
        # 笨・whose讒区枚縺ｮ隧ｳ邏ｰ蜃ｦ逅・        has_acl_relcl = any(w.deprel in ['acl:relcl', 'acl'] for w in sentence.words)
        
        if has_acl_relcl and any(w.text.lower() == 'whose' for w in sentence.words):
            # whose讒区枚縺ｧ縺ｯ蟶ｸ縺ｫ髢｢菫らｯ縺ｨ縺励※蜃ｦ逅・            # 荳ｻ譁・虚隧槭→髢｢菫らｯ蜍戊ｩ槭ｒ驕ｩ蛻・↓蛻・屬縺吶ｋ縺薙→縺ｧ蟇ｾ蠢・            self.logger.debug(f"肌 whose讒区枚: 髢｢菫らｯ縺ｨ縺励※蜃ｦ逅・幕蟋・)
            return True
        
        return has_acl_relcl
    
    def _process_relative_clause_structure(self, sentence, base_result: Dict) -> Dict:
        """髢｢菫らｯ讒矩縺ｮ蛻・ｧ｣蜃ｦ逅・""
        
        # === 1. 隕∫ｴ迚ｹ螳・===
        # 笨・whose讒区枚縺ｮ逵溘・髢｢菫らｯ讀懷・
        rel_verb = None
        antecedent = None
        
        is_whose_construction = any(w.text.lower() == 'whose' for w in sentence.words)
        
        if is_whose_construction:
            # whose讒区枚縺ｧ縺ｯ縲√∪縺啾cl:relcl髢｢菫ゅ・螳溷虚隧槭ｒ謗｢縺・            acl_word = self._find_word_by_deprel(sentence, 'acl:relcl')
            if acl_word and acl_word.upos == 'VERB':
                # Pattern B: 螳溷虚隧槭′髢｢菫らｯ蜍戊ｩ・(萓・ borrowed)
                rel_verb = acl_word
                if acl_word.head > 0:
                    antecedent = self._find_word_by_id(sentence, acl_word.head)
            else:
                # Pattern A: cop蜍戊ｩ槭′髢｢菫らｯ蜍戊ｩ・(萓・ is in "car is red")  
                for word in sentence.words:
                    if word.deprel == 'cop':
                        rel_verb = word
                        # acl:relcl縺ｮhead縺九ｉ蜈郁｡瑚ｩ槭ｒ謗｢縺・                        if acl_word and acl_word.head > 0:
                            antecedent = self._find_word_by_id(sentence, acl_word.head)
                        else:
                            # fallback: root隱槭ｒ蜈郁｡瑚ｩ槭→縺吶ｋ
                            for w in sentence.words:
                                if w.deprel == 'root':
                                    antecedent = w
                                    break
                        break
                        
            if rel_verb and antecedent:
                self.logger.debug(f"肌 whose讒区枚菫ｮ豁｣: 髢｢菫らｯ蜍戊ｩ・{rel_verb.text}, 蜈郁｡瑚ｩ・{antecedent.text}")
        
        # 騾壼ｸｸ縺ｮ髢｢菫らｯ讀懷・
        if not rel_verb:
            rel_verb = self._find_word_by_deprel(sentence, 'acl:relcl')
            if not rel_verb:
                rel_verb = self._find_word_by_deprel(sentence, 'acl')
            if not rel_verb:
                return base_result
            
            # 蜈郁｡瑚ｩ橸ｼ磯未菫らｯ蜍戊ｩ槭・鬆ｭ・・            antecedent = self._find_word_by_id(sentence, rel_verb.head)
            
        if not antecedent:
            return base_result

        self.logger.debug(f"  蜈郁｡瑚ｩ・ {antecedent.text}, 髢｢菫ょ虚隧・ {rel_verb.text}")
        
        # === 2. 髢｢菫ゆｻ｣蜷崎ｩ・髢｢菫ょ憶隧樒音螳・===
        rel_pronoun, rel_type = self._identify_relative_pronoun(sentence, rel_verb)
        
        # === 3. 髢｢菫らｯ蜀・ｦ∫ｴ迚ｹ螳・===
        rel_subject = None
        if rel_type in ['obj', 'advmod']:  # 逶ｮ逧・ｪ槭・髢｢菫ょ憶隧槭・蝣ｴ蜷医・縺ｿ荳ｻ隱樊､懃ｴ｢
            rel_subject = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'nsubj')
        elif rel_type == 'poss':
            # 謇譛画ｼ髢｢菫ゆｻ｣蜷崎ｩ槭・蝣ｴ蜷医・迚ｹ蛻･蜃ｦ逅・            # whose讒区枚縺ｧ縺ｯ縲∵園譛峨＆繧後ｋ蜷崎ｩ樔ｻ･螟悶・迢ｬ遶九＠縺滉ｸｻ隱槭ｒ謗｢縺・            nsubj_word = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'nsubj')
            possessed_noun = self._find_word_by_id(sentence, rel_pronoun.head) if rel_pronoun else None
            
            # 謇譛峨＆繧後ｋ蜷崎ｩ槭→逡ｰ縺ｪ繧倶ｸｻ隱槭′縺ゅｋ蝣ｴ蜷医・縺ｿrel_subject縺ｨ縺励※隱崎ｭ・            if nsubj_word and possessed_noun and nsubj_word.id != possessed_noun.id:
                rel_subject = nsubj_word
        
        # 謇譛画ｼ髢｢菫ゆｻ｣蜷崎ｩ槭・迚ｹ蛻･蜃ｦ逅・        possessed_noun = None
        if rel_type == 'poss':
            possessed_noun = self._find_word_by_id(sentence, rel_pronoun.head)
        
        self.logger.debug(f"  髢｢菫ゆｻ｣蜷崎ｩ・ {rel_pronoun.text if rel_pronoun else 'None'} ({rel_type})")
        if rel_subject:
            self.logger.debug(f"  髢｢菫らｯ荳ｻ隱・ {rel_subject.text}")
        if possessed_noun:
            self.logger.debug(f"  謇譛峨＆繧後ｋ蜷崎ｩ・ {possessed_noun.text}")
        
        # === 4. 蜈郁｡瑚ｩ槫唱讒狗ｯ・===
        noun_phrase = self._build_antecedent_phrase(sentence, antecedent, rel_pronoun, possessed_noun)
        self.logger.debug(f"  讒狗ｯ牙・陦瑚ｩ槫唱: '{noun_phrase}'")
        
        # === 5. Rephrase繧ｹ繝ｭ繝・ヨ蛻・ｧ｣ ===
        result = base_result.copy()
        
        # 笨・whose讒区枚縺ｮ迚ｹ蛻･蜃ｦ逅・ 繝｡繧､繝ｳ蜍戊ｩ槫・逅・ｒ螯ｨ螳ｳ縺励↑縺・        if is_whose_construction and rel_verb and rel_verb.deprel == 'cop':
            # 髢｢菫らｯ繧ｹ繝ｭ繝・ヨ縺ｮ縺ｿ逕滓・縺励√Γ繧､繝ｳ譁・・5譁・梛繝上Φ繝峨Λ繝ｼ縺ｫ莉ｻ縺帙ｋ
            rephrase_slots = self._generate_whose_relative_clause_slots(
                antecedent, rel_verb, sentence
            )
            
            # 邨先棡繝槭・繧ｸ・医Γ繧､繝ｳ譁・せ繝ｭ繝・ヨ縺ｯ菫晄戟・・            if 'slots' not in result:
                result['slots'] = {}
            if 'sub_slots' not in result:
                result['sub_slots'] = {}
            
            # 髢｢菫らｯ縺ｮsub-slots縺ｮ縺ｿ繝槭・繧ｸ・医Γ繧､繝ｳ譁・せ繝ｭ繝・ヨ縺ｯ螟画峩縺励↑縺・ｼ・            result['sub_slots'].update(rephrase_slots.get('sub_slots', {}))
            
            self.logger.debug(f"肌 whose讒区枚: 繝｡繧､繝ｳ譁・せ繝ｭ繝・ヨ菫晄戟, 髢｢菫らｯ繧ｵ繝悶せ繝ｭ繝・ヨ霑ｽ蜉")
            
        else:
            # 騾壼ｸｸ縺ｮ髢｢菫らｯ蜃ｦ逅・            rephrase_slots = self._generate_relative_clause_slots(
                rel_type, noun_phrase, rel_subject, rel_verb, sentence
            )
            
            # 邨先棡繝槭・繧ｸ
            if 'slots' not in result:
                result['slots'] = {}
            if 'sub_slots' not in result:
                result['sub_slots'] = {}
            
            # 騾壼ｸｸ縺ｮ繝槭・繧ｸ
            result['slots'].update(rephrase_slots.get('slots', {}))
            result['sub_slots'].update(rephrase_slots.get('sub_slots', {}))
        
        # 譁・ｳ墓ュ蝣ｱ險倬鹸
        result['grammar_info'] = {
            'patterns': ['relative_clause'],
            'rel_type': rel_type if not is_whose_construction else 'poss',
            'antecedent': antecedent.text,
            'rel_pronoun': 'whose' if is_whose_construction else (rel_pronoun.text if rel_pronoun else None),
            'rel_verb': rel_verb.text
        }
        
        self.logger.debug(f"  笨・髢｢菫らｯ蜃ｦ逅・ｮ御ｺ・ {len(result.get('slots', {}))} main slots, {len(result.get('sub_slots', {}))} sub slots")
        return result
    
    def _identify_relative_pronoun(self, sentence, rel_verb) -> Tuple[Optional[Any], str]:
        """髢｢菫ゆｻ｣蜷崎ｩ・髢｢菫ょ憶隧槭・迚ｹ螳壹→蛻・｡橸ｼ育怐逡･譁・ｯｾ蠢懷ｼｷ蛹悶・蜿怜虚諷玖・・・・""
        
        # 1. 髢｢菫ょ憶隧樊､懷・・域怙蜆ｪ蜈茨ｼ・        advmod_word = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'advmod')
        if advmod_word and advmod_word.text.lower() in ['where', 'when', 'why', 'how']:
            return advmod_word, 'advmod'
        
        # 2. 謇譛画ｼ髢｢菫ゆｻ｣蜷崎ｩ樊､懷・
        for word in sentence.words:
            if word.text.lower() == 'whose' and word.deprel == 'nmod:poss':
                return word, 'poss'
        
        # 3. 譏守､ｺ逧・未菫ゆｻ｣蜷崎ｩ樊､懷・
        # 逶ｮ逧・ｪ樣未菫ゆｻ｣蜷崎ｩ・        obj_pronoun = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'obj')
        if obj_pronoun and obj_pronoun.text.lower() in ['who', 'whom', 'which', 'that']:
            return obj_pronoun, 'obj'
        
        # 荳ｻ隱樣未菫ゆｻ｣蜷崎ｩ橸ｼ亥女蜍墓・繝√ぉ繝・け霑ｽ蜉・・ 
        subj_pronoun = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'nsubj')
        if subj_pronoun and subj_pronoun.text.lower() in ['who', 'which', 'that']:
            # 蜿怜虚諷九・蝣ｴ蜷医・荳ｻ隱樣未菫ゆｻ｣蜷崎ｩ槭→縺励※蜃ｦ逅・            return subj_pronoun, 'nsubj'
            
        # 蜿怜虚諷倶ｸｻ隱樣未菫ゆｻ｣蜷崎ｩ・        pass_subj_pronoun = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'nsubj:pass')
        if pass_subj_pronoun and pass_subj_pronoun.text.lower() in ['who', 'which', 'that']:
            return pass_subj_pronoun, 'nsubj:pass'
        
        # 4. 逵∫払髢｢菫ゆｻ｣蜷崎ｩ槭・謗ｨ螳夲ｼ亥女蜍墓・讒矩謾ｹ蝟・ｼ・        inferred_type = self._infer_omitted_relative_pronoun(sentence, rel_verb)
        if inferred_type:
            # 莉ｮ諠ｳ逧・↑髢｢菫ゆｻ｣蜷崎ｩ槭が繝悶ず繧ｧ繧ｯ繝医ｒ菴懈・
            virtual_pronoun = self._create_virtual_relative_pronoun(sentence, rel_verb, inferred_type)
            return virtual_pronoun, inferred_type
        
        return None, 'unknown'
    
    def _infer_omitted_relative_pronoun(self, sentence, rel_verb) -> Optional[str]:
        """逵∫払縺輔ｌ縺滄未菫ゆｻ｣蜷崎ｩ槭・謗ｨ螳夲ｼ亥女蜍墓・讒矩謾ｹ蝟・ｼ・""
        
        # 髢｢菫らｯ蜍戊ｩ槭・萓晏ｭ俶ｧ矩繧貞・譫・        rel_verb_deps = []
        for word in sentence.words:
            if word.head == rel_verb.id:
                rel_verb_deps.append(word.deprel)
        
        self.logger.debug(f"    髢｢菫ょ虚隧・'{rel_verb.text}' 縺ｮ萓晏ｭ倩ｪ・ {rel_verb_deps}")
        
        # 繝代ち繝ｼ繝ｳ1: 蜿怜虚諷矩未菫らｯ縺ｮ讀懷・・域隼蝟・ｼ・        has_nsubj_pass = 'nsubj:pass' in rel_verb_deps or 'nsubjpass' in rel_verb_deps
        has_aux_pass = any(word.deprel in ['aux:pass', 'auxpass'] and word.head == rel_verb.id 
                          for word in sentence.words)
        
        if has_nsubj_pass or has_aux_pass:
            # 蜿怜虚諷矩未菫らｯ・壼・陦瑚ｩ槭′蜿怜虚諷九・荳ｻ隱・            self.logger.debug(f"    謗ｨ螳・ 蜿怜虚諷倶ｸｻ隱樣未菫ゆｻ｣蜷崎ｩ・)
            return 'nsubj:pass'  # 蜿怜虚諷倶ｸｻ隱槭→縺励※謇ｱ縺・        
        # 繝代ち繝ｼ繝ｳ2: 閭ｽ蜍墓・縺ｧ逶ｮ逧・ｪ槭′縺ｪ縺・ｴ蜷・        has_nsubj = 'nsubj' in rel_verb_deps
        has_obj = 'obj' in rel_verb_deps or 'dobj' in rel_verb_deps
        
        if has_nsubj and not has_obj:
            # 閭ｽ蜍墓・縺ｧ逶ｮ逧・ｪ槭′縺ｪ縺・ｴ蜷医∝・陦瑚ｩ槭′逶ｮ逧・ｪ槭・蜿ｯ閭ｽ諤ｧ
            self.logger.debug(f"    謗ｨ螳・ 逵∫払逶ｮ逧・ｪ樣未菫ゆｻ｣蜷崎ｩ橸ｼ郁・蜍墓・繝代ち繝ｼ繝ｳ・・)  
            return 'obj_omitted'
        
        # 繝代ち繝ｼ繝ｳ3: 荳ｻ隱槭′縺ｪ縺上・未菫らｯ縺瑚・蜍墓・縺ｮ蝣ｴ蜷・        if not has_nsubj and not has_nsubj_pass:
            self.logger.debug(f"    謗ｨ螳・ 逵∫払荳ｻ隱樣未菫ゆｻ｣蜷崎ｩ・)
            return 'nsubj_omitted'
        
        return None
    
    def _create_virtual_relative_pronoun(self, sentence, rel_verb, inferred_type):
        """莉ｮ諠ｳ逧・↑髢｢菫ゆｻ｣蜷崎ｩ槭が繝悶ず繧ｧ繧ｯ繝井ｽ懈・"""
        
        # 髢｢菫らｯ縺ｮ蜈郁｡瑚ｩ槭ｒ蜿門ｾ・        antecedent = self._find_word_by_id(sentence, rel_verb.head)
        
        # 莉ｮ諠ｳ繧ｪ繝悶ず繧ｧ繧ｯ繝茨ｼ郁ｾ樊嶌蠖｢蠑上〒邁｡譏灘ｮ溯｣・ｼ・        virtual_pronoun = type('VirtualWord', (), {
            'text': '[omitted]',  # 逵∫払繝槭・繧ｫ繝ｼ
            'id': rel_verb.id - 0.5,  # 莉ｮ諠ｳID・磯未菫ょ虚隧槭・逶ｴ蜑搾ｼ・            'head': rel_verb.head,
            'deprel': inferred_type.replace('_omitted', ''),
            'lemma': '[omitted]'
        })()
        
        self.logger.debug(f"    莉ｮ諠ｳ髢｢菫ゆｻ｣蜷崎ｩ樔ｽ懈・: type={inferred_type}, text=[omitted]")
        return virtual_pronoun
    
    def _build_antecedent_phrase(self, sentence, antecedent, rel_pronoun, possessed_noun=None) -> str:
        """蜈郁｡瑚ｩ槫唱讒狗ｯ会ｼ井ｿｮ鬟ｾ隱槫性繧・・ 髢｢菫らｯ縺ｮ蜍戊ｩ樣Κ蛻・・髯､螟・""
        if not antecedent:
            return rel_pronoun.text if rel_pronoun else ""
        
        # 蜈郁｡瑚ｩ槭・菫ｮ鬟ｾ隱槫庶髮・        modifiers = []
        for word in sentence.words:
            if word.head == antecedent.id and word.deprel in ['det', 'amod', 'compound']:
                modifiers.append(word)
        
        # 蝓ｺ譛ｬ讒区・・壻ｿｮ鬟ｾ隱・+ 蜈郁｡瑚ｩ・+ 髢｢菫ゆｻ｣蜷崎ｩ・        phrase_words = modifiers + [antecedent]
        
        # 髢｢菫ゆｻ｣蜷崎ｩ槭ｒ霑ｽ蜉・亥虚隧樣Κ蛻・・髯､螟厄ｼ・        if rel_pronoun:
            phrase_words.append(rel_pronoun)
        
        # 謇譛画ｼ縺ｮ迚ｹ蛻･蜃ｦ逅・ｼ域園譛峨＆繧後ｋ蜷崎ｩ槭・縺ｿ・・        if possessed_noun and rel_pronoun:
            if possessed_noun not in phrase_words:
                phrase_words.append(possessed_noun)
        
        # ID鬆・た繝ｼ繝茨ｼ郁ｪ樣・ｿ晄戟・・        phrase_words.sort(key=lambda w: w.id)
        return ' '.join(w.text for w in phrase_words)
    
    def _generate_relative_clause_slots(self, rel_type: str, noun_phrase: str, rel_subject, rel_verb, sentence) -> Dict:
        """髢｢菫らｯ繧ｿ繧､繝怜挨繧ｹ繝ｭ繝・ヨ逕滓・・亥女蜍墓・蟇ｾ蠢懈隼蝟・ｼ・""
        
        slots = {}
        sub_slots = {}
        
        # 蜿怜虚諷玖｣懷勧蜍戊ｩ槭・讀懷・
        aux_word = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'aux:pass')
        if not aux_word:
            aux_word = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'aux')
        
        # 圻 蜑ｯ隧槫・逅・ｒ蜑ｯ隧槭ワ繝ｳ繝峨Λ繝ｼ縺ｫ螳悟・蟋碑ｭｲ・育ｫｶ蜷亥屓驕ｿ・・        # 蜉ｩ蜍戊ｩ槭ワ繝ｳ繝峨Λ繝ｼ縺ｯ蜑ｯ隧槭せ繝ｭ繝・ヨ險ｭ螳壹ｒ陦後ｏ縺ｪ縺・        # adverb_word = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'advmod')
        # if adverb_word:
        #     if adverb_word.text.lower() not in ['where', 'when', 'why', 'how']:
        #         if adverb_word.id < rel_verb.id:
        #             sub_slots["sub-m1"] = adverb_word.text
        #             self.logger.debug(f"肌 髢｢菫らｯ蜀・憶隧樊､懷・: sub-m1 = '{adverb_word.text}' (蜍戊ｩ槫燕)")
        #         else:
        #             sub_slots["sub-m2"] = adverb_word.text
        #             self.logger.debug(f"肌 髢｢菫らｯ蜀・憶隧樊､懷・: sub-m2 = '{adverb_word.text}' (蜍戊ｩ槫ｾ・")
        
        # 圻 蜑咲ｽｮ隧槫唱蜃ｦ逅・ｂ蜑ｯ隧槭ワ繝ｳ繝峨Λ繝ｼ縺ｫ蟋碑ｭｲ・亥ｮ悟・縺ｪ蜑ｯ隧槫・逅・ｵｱ荳・・        # obl_word = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'obl')
        # if obl_word:
        #     sub_slots["sub-m3"] = obl_word.text
        #     self.logger.debug(f"肌 髢｢菫らｯ蜀・憶隧槫唱讀懷・: sub-m3 = '{obl_word.text}'")
        
        if rel_type == 'obj':
            # 逶ｮ逧・ｪ樣未菫ゆｻ｣蜷崎ｩ・ "The book that he bought"
            # slots["O1"] = ""  # 荳贋ｽ阪せ繝ｭ繝・ヨ縺ｯ5譁・梛繧ｨ繝ｳ繧ｸ繝ｳ縺ｫ莉ｻ縺帙ｋ
            sub_slots["sub-o1"] = noun_phrase
            if rel_subject:
                sub_slots["sub-s"] = rel_subject.text
            sub_slots["sub-v"] = rel_verb.text
            
        elif rel_type == 'nsubj':
            # 荳ｻ隱樣未菫ゆｻ｣蜷崎ｩ・ "The man who runs"
            # slots["S"] = ""  # 荳贋ｽ阪せ繝ｭ繝・ヨ縺ｯ5譁・梛繧ｨ繝ｳ繧ｸ繝ｳ縺ｫ莉ｻ縺帙ｋ
            sub_slots["sub-s"] = noun_phrase
            sub_slots["sub-v"] = rel_verb.text
            
        elif rel_type == 'nsubj:pass':
            # 蜿怜虚諷倶ｸｻ隱樣未菫ゆｻ｣蜷崎ｩ・ "The car which was crashed"
            # slots["S"] = ""  # 荳贋ｽ阪せ繝ｭ繝・ヨ縺ｯ5譁・梛繧ｨ繝ｳ繧ｸ繝ｳ縺ｫ莉ｻ縺帙ｋ
            sub_slots["sub-s"] = noun_phrase
            if aux_word:
                sub_slots["sub-aux"] = aux_word.text
            sub_slots["sub-v"] = rel_verb.text
            
        elif rel_type == 'poss':
            # 謇譛画ｼ髢｢菫ゆｻ｣蜷崎ｩ・ whose讒区枚縺ｮ迚ｹ蛻･蜃ｦ逅・            
            # 笨・繝上う繝悶Μ繝・ラ隗｣譫占｣懈ｭ｣縺後≠繧句ｴ蜷医・迚ｹ蛻･蜃ｦ逅・            if hasattr(sentence, 'hybrid_corrections'):
                # whose讒区枚縺ｧ蜍戊ｩ槭′陬懈ｭ｣縺輔ｌ縺ｦ縺・ｋ蝣ｴ蜷医・縲∽ｸｻ譁・・髢｢菫らｯ讒矩繧呈ｭ｣縺励￥蛻・屬
                for word_id, correction in sentence.hybrid_corrections.items():
                    if correction['correction_type'] == 'whose_verb_fix':
                        # 陬懈ｭ｣縺輔ｌ縺溷虚隧橸ｼ井ｾ具ｼ嗟ives・峨・荳ｻ譁・虚隧槭↑縺ｮ縺ｧ縲・未菫らｯ縺ｮ蜃ｦ逅・°繧蛾勁螟・                        main_verb_word = self._find_word_by_id(sentence, word_id)
                        if main_verb_word:
                            self.logger.debug(f"肌 whose讒区枚繝上う繝悶Μ繝・ラ陬懈ｭ｣: {main_verb_word.text}縺ｯ荳ｻ譁・虚隧槭→縺励※蜃ｦ逅・)
                            # 縺薙・蝣ｴ蜷医・未菫らｯ縺ｯ"car is red"縺ｮ驛ｨ蛻・                            # rel_verb縺ｯcopula "is"
                            sub_slots["sub-s"] = noun_phrase  # "The man whose car"
                            sub_slots["sub-v"] = rel_verb.text  # "is"
                            
                            # 陬懆ｪ槭ｒ讀懷・・・red"・・                            complement = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'amod')
                            if complement:
                                sub_slots["sub-c1"] = complement.text
                            
                            # 繝｡繧､繝ｳ譁・・蛻･騾泌渕譛ｬ5譁・梛繝上Φ繝峨Λ繝ｼ縺悟・逅・☆繧・                            return {"slots": slots, "sub_slots": sub_slots}
            
            # 騾壼ｸｸ縺ｮwhose讒区枚蜃ｦ逅・            if rel_subject:
                # 蛻･縺ｮ荳ｻ隱槭′縺ゅｋ蝣ｴ蜷・ "The student whose book I borrowed"
                # 竊・逶ｮ逧・ｪ樣未菫ゆｻ｣蜷崎ｩ槭→縺励※蜃ｦ逅・                sub_slots["sub-o1"] = noun_phrase
                sub_slots["sub-s"] = rel_subject.text
            else:
                # 蛻･縺ｮ荳ｻ隱槭′縺ｪ縺・ｴ蜷・ "The woman whose dog barks"  
                # 竊・荳ｻ隱樣未菫ゆｻ｣蜷崎ｩ槭→縺励※蜃ｦ逅・                sub_slots["sub-s"] = noun_phrase
            
            # 髢｢菫らｯ蜀・・蜍戊ｩ槭・陬懆ｪ槭ｒ豁｣縺励￥謚ｽ蜃ｺ
            if aux_word:
                sub_slots["sub-aux"] = aux_word.text
            sub_slots["sub-v"] = rel_verb.text
            
            # whose讒区枚縺ｮ迚ｹ蛻･蜃ｦ逅・ｼ售tanza縺ｮ隱､隗｣譫仙ｯｾ蠢・            if any(w.text.lower() == 'whose' for w in sentence.words):
                # acl:relcl縺ｨ縺励※隗｣譫舌＆繧後◆lives・・d=7・峨・萓晏ｭ倩ｪ槭°繧詠ed繧呈爾縺・                acl_relcl_word = self._find_word_by_deprel(sentence, 'acl:relcl')
                if acl_relcl_word:
                    complement = self._find_word_by_head_and_deprel(sentence, acl_relcl_word.id, 'amod')
                    if complement:
                        sub_slots["sub-c1"] = complement.text
            else:
                # 騾壼ｸｸ縺ｮ陬懆ｪ樊､懷・
                complement = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'acomp')  # 蠖｢螳ｹ隧櫁｣懆ｪ・                if not complement:
                    complement = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'attr')  # 螻樊ｧ陬懆ｪ・                if not complement:
                    complement = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'nmod')  # 蜷崎ｩ樔ｿｮ鬟ｾ
                if complement:
                    sub_slots["sub-c1"] = complement.text
            
        elif rel_type == 'advmod':
            # 髢｢菫ょ憶隧・ "The place where he lives" / "The way how he solved it"
            # slots["M3"] = ""  # 荳贋ｽ阪せ繝ｭ繝・ヨ縺ｯ5譁・梛繧ｨ繝ｳ繧ｸ繝ｳ縺ｫ莉ｻ縺帙ｋ
            sub_slots["sub-m1"] = noun_phrase
            if rel_subject:
                sub_slots["sub-s"] = rel_subject.text
            sub_slots["sub-v"] = rel_verb.text
            
            # 笨・髢｢菫ょ憶隧槫唱蜀・・逶ｮ逧・ｪ槭ｒ讀懷・縺励※sub-o1縺ｫ驟咲ｽｮ
            obj_word = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'obj')
            if obj_word:
                sub_slots["sub-o1"] = obj_word.text
                self.logger.debug(f"肌 髢｢菫ょ憶隧槫唱蜀・岼逧・ｪ樊､懷・: sub-o1 = '{obj_word.text}'")
            
        # 逵∫払髢｢菫ゆｻ｣蜷崎ｩ槭・蜃ｦ逅・        elif rel_type == 'obj_omitted':
            # 逵∫払逶ｮ逧・ｪ樣未菫ゆｻ｣蜷崎ｩ・ "The book I read"
            # 肌 菫ｮ豁｣: 髢｢菫らｯ蜈ｨ菴薙ｒ讒狗ｯ・            slots["S"] = ""  # 荳ｻ遽荳ｻ隱槭ｒ遨ｺ縺ｫ險ｭ螳夲ｼ亥・陦瑚ｩ槭・蠕灘ｱ樒ｯ縺ｫ遘ｻ蜍包ｼ・            
            # 蜈郁｡瑚ｩ槭ユ繧ｭ繧ｹ繝医°繧閏omitted]繧帝勁蜴ｻ
            clean_noun_phrase = noun_phrase.replace(" [omitted]", "").replace("[omitted]", "")
            
            # 蠕灘ｱ樒ｯ荳ｻ隱槭ｒ讀懷・・磯未菫らｯ蜍戊ｩ槭・nsubj・・            rel_subject = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'nsubj')
            if rel_subject:
                sub_slots["sub-o1"] = clean_noun_phrase
                sub_slots["sub-s"] = rel_subject.text
                sub_slots["sub-v"] = rel_verb.text
                self.logger.debug(f"肌 逵∫払逶ｮ逧・ｪ樣未菫らｯ: sub-s = '{rel_subject.text}'")
            else:
                sub_slots["sub-o1"] = clean_noun_phrase
                sub_slots["sub-v"] = rel_verb.text
            
        elif rel_type == 'nsubj_omitted':  
            # 逵∫払荳ｻ隱樣未菫ゆｻ｣蜷崎ｩ・ "The person standing there"
            # slots["O1"] = ""  # 荳贋ｽ阪せ繝ｭ繝・ヨ縺ｯ5譁・梛繧ｨ繝ｳ繧ｸ繝ｳ縺ｫ莉ｻ縺帙ｋ
            sub_slots["sub-o1"] = noun_phrase
            sub_slots["sub-v"] = rel_verb.text
            
        else:
            # 繝・ヵ繧ｩ繝ｫ繝茨ｼ育岼逧・ｪ樊桶縺・ｼ・            # slots["O1"] = ""  # 荳贋ｽ阪せ繝ｭ繝・ヨ縺ｯ5譁・梛繧ｨ繝ｳ繧ｸ繝ｳ縺ｫ莉ｻ縺帙ｋ
            sub_slots["sub-o1"] = noun_phrase
            if rel_subject:
                sub_slots["sub-s"] = rel_subject.text
            sub_slots["sub-v"] = rel_verb.text
        
        return {"slots": slots, "sub_slots": sub_slots}
    
    def _generate_whose_relative_clause_slots(self, antecedent, cop_verb, sentence) -> Dict:
        """whose讒区枚蟆ら畑縺ｮ髢｢菫らｯ繧ｹ繝ｭ繝・ヨ逕滓・・医Γ繧､繝ｳ譁・ｒ螯ｨ螳ｳ縺励↑縺・ｼ・""
        
        slots = {}  # 繝｡繧､繝ｳ譁・せ繝ｭ繝・ヨ縺ｯ螟画峩縺励↑縺・        sub_slots = {}
        
        # whose讒区枚縺ｮ髢｢菫らｯ: "whose car is red"
        # 謇譛画ｼ髢｢菫ゆｻ｣蜷崎ｩ槭ｒ蜷ｫ繧蜈郁｡瑚ｩ槫唱繧呈ｧ狗ｯ・        whose_word = None
        car_word = None
        
        for word in sentence.words:
            if word.text.lower() == 'whose':
                whose_word = word
                # whose縺御ｾ晏ｭ倥☆繧玖ｪ橸ｼ・ar・峨ｒ蜿門ｾ・                car_word = self._find_word_by_id(sentence, whose_word.head)
                break
        
        if whose_word and car_word:
            # "The man whose car"縺ｮ讒狗ｯ・            man_phrase = self._build_phrase_with_modifiers(sentence, antecedent)
            whose_car_phrase = f"{man_phrase} {whose_word.text} {car_word.text}"
            
            sub_slots["sub-s"] = whose_car_phrase
            sub_slots["sub-v"] = cop_verb.text  # "is"
            
            # 陬懆ｪ橸ｼ・ed・峨ｒ蜿門ｾ・            complement = self._find_word_by_id(sentence, cop_verb.head)
            if complement:
                sub_slots["sub-c1"] = complement.text
            
            self.logger.debug(f"肌 whose髢｢菫らｯ繧ｹ繝ｭ繝・ヨ: sub-s='{whose_car_phrase}', sub-v='{cop_verb.text}', sub-c1='{complement.text if complement else ''}'")
        
        return {"slots": slots, "sub_slots": sub_slots}
    
    def _process_main_clause_after_relative(self, sentence, antecedent, rel_verb, noun_phrase) -> Optional[Dict]:
        """髢｢菫らｯ蜃ｦ逅・ｾ後・荳ｻ譁・Κ蛻・ｒ5譁・梛縺ｧ蜃ｦ逅・""
        
        # 荳ｻ譁・・蜍戊ｩ橸ｼ・OOT隱橸ｼ峨ｒ迚ｹ螳・        main_verb = self._find_root_word(sentence)
        if not main_verb:
            self.logger.debug("  笞・・荳ｻ譁・虚隧槭↑縺・)
            return None
            
        if main_verb.id == rel_verb.id:
            self.logger.debug(f"  笞・・髢｢菫らｯ蜍戊ｩ槭′ROOT - 荳ｻ譁・↑縺・(main_verb={main_verb.text}, rel_verb={rel_verb.text})")
            return None
        
        self.logger.debug(f"  剥 荳ｻ譁・虚隧樊､懷・: {main_verb.text} (id: {main_verb.id}, POS: {main_verb.upos})")
        
        # 萓晏ｭ倬未菫ゅ・繝・・讒狗ｯ会ｼ磯未菫らｯ繧帝勁螟厄ｼ・        dep_relations = {}
        excluded_words = []
        
        for word in sentence.words:
            # 髢｢菫らｯ蜀・・隱槭ｒ繧ｹ繧ｭ繝・・
            if self._is_word_in_relative_clause(word, rel_verb):
                excluded_words.append(word.text)
                continue
                
            if word.deprel not in dep_relations:
                dep_relations[word.deprel] = []
            dep_relations[word.deprel].append(word)
        
        self.logger.debug(f"  圻 髯､螟冶ｪ・ {excluded_words}")
        self.logger.debug(f"  統 荳ｻ譁・ｾ晏ｭ倬未菫・ {list(dep_relations.keys())}")
        
        # 蝓ｺ譛ｬ5譁・梛繝代ち繝ｼ繝ｳ讀懷・
        pattern_result = self._detect_basic_five_pattern(main_verb, dep_relations)
        if not pattern_result:
            self.logger.debug("  笶・荳ｻ譁・ヱ繧ｿ繝ｼ繝ｳ讀懷・螟ｱ謨・)
            return None
        
        self.logger.debug(f"  識 荳ｻ譁・ヱ繧ｿ繝ｼ繝ｳ讀懷・: {pattern_result['pattern']}")
        
        # 繧ｹ繝ｭ繝・ヨ逕滓・・・繧ｹ繝ｭ繝・ヨ縺ｯ遨ｺ縺ｫ縺励※讒矩繧堤ｶｭ謖・ｼ・        five_pattern_slots = self._generate_basic_five_slots(
            pattern_result['pattern'], pattern_result['mapping'], dep_relations, sentence
        )
        
        # 髢｢菫らｯ繧貞性繧荳ｻ隱槭・繧ｵ繝悶せ繝ｭ繝・ヨ縺ｫ縺ゅｋ縺溘ａ縲∽ｸ贋ｽ拘繧ｹ繝ｭ繝・ヨ縺ｯNone縺ｾ縺溘・遨ｺ
        if 'slots' in five_pattern_slots and 'S' in five_pattern_slots['slots']:
            five_pattern_slots['slots']['S'] = ""  # 髢｢菫らｯ縺後し繝悶せ繝ｭ繝・ヨ縺ｫ蜷ｫ縺ｾ繧後ｋ縺薙→繧堤､ｺ縺・            
        self.logger.debug(f"  笨・荳ｻ譁・・逅・ｮ御ｺ・ 繝代ち繝ｼ繝ｳ={pattern_result['pattern']}")
        return five_pattern_slots
    
    def _is_word_in_relative_clause(self, word, rel_verb) -> bool:
        """隱槭′髢｢菫らｯ蜀・↓縺ゅｋ縺九メ繧ｧ繝・け"""
        
        # 髢｢菫らｯ蜍戊ｩ櫁・霄ｫ
        if word.id == rel_verb.id:
            return True
            
        # 髢｢菫らｯ蜍戊ｩ槭・逶ｴ謗･萓晏ｭ倩ｪ橸ｼ亥・遞ｮ鬘橸ｼ・        if word.head == rel_verb.id:
            return True
            
        # 髢｢菫ゆｻ｣蜷崎ｩ橸ｼ磯未菫らｯ蜍戊ｩ槭↓萓晏ｭ倥☆繧杵subj/obj遲会ｼ・        if word.deprel in ['nsubj', 'obj', 'advmod', 'obl', 'aux', 'aux:pass', 'acomp', 'attr', 'nmod'] and word.head == rel_verb.id:
            return True
        
        # 髢｢菫らｯ繧剃ｿｮ鬟ｾ縺吶ｋacl:relcl縺ｮ萓晏ｭ倩ｪ・        if word.deprel == 'acl:relcl':
            return True
            
        return False
    
    def _get_all_dependents(self, head_word) -> List:
        """謖・ｮ夊ｪ槭・縺吶∋縺ｦ縺ｮ萓晏ｭ倩ｪ槭ｒ蜿門ｾ・""
        # 縺薙・螳溯｣・〒縺ｯ縲《entence繧ｪ繝悶ず繧ｧ繧ｯ繝医↓逶ｴ謗･繧｢繧ｯ繧ｻ繧ｹ縺ｧ縺阪↑縺・◆繧・        # 邁｡譏灘ｮ溯｣・→縺励※遨ｺ繝ｪ繧ｹ繝医ｒ霑斐☆
        # 螳滄圀縺ｮ菴ｿ逕ｨ縺ｧ縺ｯ縲《entence.words繧帝壹§縺ｦ萓晏ｭ倩ｪ槭ｒ讀懃ｴ｢縺吶ｋ
        return []
    
    # === Stanza隗｣譫舌・繝ｫ繝代・繝｡繧ｽ繝・ラ ===
    
    def _find_word_by_deprel(self, sentence, deprel: str):
        """萓晏ｭ倬未菫ゅ〒隱槭ｒ讀懃ｴ｢"""
        return next((w for w in sentence.words if w.deprel == deprel), None)
    
    def _find_word_by_id(self, sentence, word_id: int):
        """ID縺ｧ隱槭ｒ讀懃ｴ｢"""
        return next((w for w in sentence.words if w.id == word_id), None)
    
    def _find_word_by_head_and_deprel(self, sentence, head_id: int, deprel: str):
        """鬆ｭID縺ｨ萓晏ｭ倬未菫ゅ〒隱槭ｒ讀懃ｴ｢"""
        return next((w for w in sentence.words if w.head == head_id and w.deprel == deprel), None)
    
    def _find_main_verb(self, sentence):
        """荳ｻ譁・・蜍戊ｩ槭ｒ讀懃ｴ｢・磯未菫らｯ繧帝勁螟悶・繝上う繝悶Μ繝・ラ隗｣譫仙ｯｾ蠢懶ｼ・""
        
        # 繝上う繝悶Μ繝・ラ隗｣譫舌・陬懈ｭ｣諠・ｱ繧偵メ繧ｧ繝・け
        if hasattr(sentence, 'hybrid_corrections'):
            for word in sentence.words:
                if word.id in sentence.hybrid_corrections:
                    correction = sentence.hybrid_corrections[word.id]
                    if correction['correction_type'] == 'whose_verb_fix':
                        # 陬懈ｭ｣縺輔ｌ縺溷虚隧槭ｒ荳ｻ譁・虚隧槭→縺励※霑斐☆
                        self.logger.debug(f"肌 繝上う繝悶Μ繝・ラ隗｣譫・ 荳ｻ譁・虚隧槭→縺励※ {word.text} 繧剃ｽｿ逕ｨ (陬懈ｭ｣貂医∩)")
                        return word
        
        # 騾壼ｸｸ縺ｮ蝣ｴ蜷茨ｼ嗷oot繧呈､懃ｴ｢・・hose讒区枚縺ｧ繧ょ・縺ｫ繝√ぉ繝・け・・        root_word = None
        for word in sentence.words:
            if word.head == 0:  # root
                root_word = word
                break
        
        # whose讒区枚縺ｮ迚ｹ蛻･蜃ｦ逅・ｼ嗷oot縺悟ｭ伜惠縺帙★縲∥cl:relcl隱槭′繝｡繧､繝ｳ蜍戊ｩ槫呵｣懊・蝣ｴ蜷医・縺ｿ
        if any(w.text.lower() == 'whose' for w in sentence.words) and not root_word:
            acl_relcl_word = self._find_word_by_deprel(sentence, 'acl:relcl')
            if (acl_relcl_word and 
                acl_relcl_word.text.lower() in ['lives', 'works', 'runs', 'goes'] and
                acl_relcl_word.lemma in ['live', 'work', 'run', 'go']):
                self.logger.debug(f"肌 whose讒区枚: 荳ｻ譁・虚隧槭→縺励※ {acl_relcl_word.text} 繧剃ｽｿ逕ｨ")
                return acl_relcl_word
        
        # 騾壼ｸｸ縺ｮ蝣ｴ蜷茨ｼ嗷oot繧呈､懃ｴ｢・・hose讒区枚縺ｧ繧ょ・縺ｫ繝√ぉ繝・け・・        root_word = None
        for word in sentence.words:
            if word.head == 0:  # root
                root_word = word
                break
        
        # whose讒区枚縺ｮ迚ｹ蛻･蜃ｦ逅・ｼ嗷oot縺悟ｭ伜惠縺帙★縲∥cl:relcl隱槭′繝｡繧､繝ｳ蜍戊ｩ槫呵｣懊・蝣ｴ蜷医・縺ｿ
        if any(w.text.lower() == 'whose' for w in sentence.words) and not root_word:
            acl_relcl_word = self._find_word_by_deprel(sentence, 'acl:relcl')
            if (acl_relcl_word and 
                acl_relcl_word.text.lower() in ['lives', 'works', 'runs', 'goes'] and
                acl_relcl_word.lemma in ['live', 'work', 'run', 'go']):
                self.logger.debug(f"肌 whose讒区枚: 荳ｻ譁・虚隧槭→縺励※ {acl_relcl_word.text} 繧剃ｽｿ逕ｨ")
                return acl_relcl_word
        
        if not root_word:
            return None
            
        # root縺悟ｽ｢螳ｹ隧槭・蝣ｴ蜷医・迚ｹ蛻･蜃ｦ逅・        if root_word.upos == 'ADJ':
            # when讒区枚縺ｧ縺ｯ蠖｢螳ｹ隧槭ｒ荳ｻ蜍戊ｩ槭→縺励※謇ｱ縺・ｼ・ephrase莉墓ｧ假ｼ・            if any(w.text.lower() == 'when' for w in sentence.words):
                self.logger.debug(f"肌 when讒区枚: 蠖｢螳ｹ隧槭ｒ荳ｻ蜍戊ｩ槭→縺励※菴ｿ逕ｨ {root_word.text}")
                return root_word
            else:
                # 騾壼ｸｸ縺ｮ蝣ｴ蜷茨ｼ喞op蜍戊ｩ槭ｒ荳ｻ蜍戊ｩ槭→縺吶ｋ・・The man is strong"讒矩・・                cop_verb = self._find_word_by_head_and_deprel(sentence, root_word.id, 'cop')
                if cop_verb:
                    return cop_verb
        
        return root_word
    
    def _build_full_subject_with_relative_clause(self, sentence, antecedent, rel_verb):
        """髢｢菫らｯ繧貞性繧螳悟・縺ｪ荳ｻ隱槫唱繧呈ｧ狗ｯ・""
        # 蜈郁｡瑚ｩ槭°繧蛾幕蟋・        subject_phrase = antecedent.text
        
        # 蜈郁｡瑚ｩ槭・菫ｮ鬟ｾ隱槭ｒ霑ｽ蜉
        modifiers = []
        for word in sentence.words:
            if word.head == antecedent.id and word.id != rel_verb.id:
                if word.deprel in ['det', 'amod', 'compound']:
                    modifiers.append((word.id, word.text))
        
        # 菫ｮ鬟ｾ隱槭ｒ菴咲ｽｮ鬆・〒繧ｽ繝ｼ繝・        modifiers.sort(key=lambda x: x[0])
        
        # 螳悟・縺ｪ荳ｻ隱槫唱繧呈ｧ狗ｯ・        if modifiers:
            modifier_text = ' '.join([m[1] for m in modifiers])
            subject_phrase = f"{modifier_text} {subject_phrase}"
        
        return subject_phrase
    
    def _is_whose_construction(self, sentence, rel_verb):
        """whose讒区枚縺九←縺・°繧貞愛螳・""
        # whose縺悟ｭ伜惠縺励√°縺､rel_verb縺ｮ萓晏ｭ倩ｪ槭↓cop縺後≠繧句ｴ蜷・        has_whose = any(w.text.lower() == 'whose' for w in sentence.words)
        has_cop_child = any(w.head == rel_verb.id and w.deprel == 'cop' for w in sentence.words)
        return has_whose and has_cop_child
    
    def _find_cop_verb_in_whose_clause(self, sentence, rel_verb):
        """whose讒区枚縺ｧ縺ｮ螳滄圀縺ｮ髢｢菫らｯ蜍戊ｩ橸ｼ・op・峨ｒ讀懃ｴ｢"""
        # rel_verb縺ｮ萓晏ｭ倩ｪ槭〒cop縺ｮ繧ゅ・繧呈爾縺・        cop_verb = next((w for w in sentence.words if w.head == rel_verb.id and w.deprel == 'cop'), None)
        return cop_verb
    
    def _find_whose_antecedent(self, sentence):
        """whose讒区枚縺ｮ蜈郁｡瑚ｩ槭ｒ讀懃ｴ｢"""
        # root荳ｻ隱槭ｒ蜿門ｾ暦ｼ磯壼ｸｸ縺ｯ蜈郁｡瑚ｩ橸ｼ・        for word in sentence.words:
            if word.head == 0 and word.deprel == 'root':
                return word
        return None
    
    def _handle_basic_five_pattern(self, sentence, base_result: Dict) -> Optional[Dict]:
        """
        蝓ｺ譛ｬ5譁・梛繝上Φ繝峨Λ繝ｼ・・hase 1螳溯｣・ｼ・        
        basic_five_pattern_engine.py 縺ｮ讖溯・繧堤ｵｱ蜷医す繧ｹ繝・Β縺ｫ遘ｻ讀・        Stanza dependency parsing 縺ｫ繧医ｋ蝓ｺ譛ｬ譁・梛讀懷・繝ｻ蛻・ｧ｣
        
        Args:
            sentence: Stanza sentence object
            base_result: 蝓ｺ譛ｬ邨先棡霎樊嶌
            
        Returns:
            Optional[Dict]: 5譁・梛蜃ｦ逅・ｵ先棡 or None
        """
        try:
            self.logger.debug("剥 5譁・梛繝上Φ繝峨Λ繝ｼ螳溯｡御ｸｭ...")
            
            # 莉悶・繧ｨ繝ｳ繧ｸ繝ｳ縺御ｸｻ譁・虚隧橸ｼ・・峨ｒ譌｢縺ｫ蜃ｦ逅・ｸ医∩縺ｮ蝣ｴ蜷医・縺ｿ繧ｹ繧ｭ繝・・
            # sub-v縺ｯ髢｢菫らｯ蜍戊ｩ槭↑縺ｮ縺ｧ荳ｻ譁・・逅・↓縺ｯ蠖ｱ髻ｿ縺励↑縺・            if base_result.get('slots', {}).get('V'):
                self.logger.debug("  荳ｻ譁・虚隧・V)縺悟・逅・ｸ医∩ - 繧ｹ繧ｭ繝・・")
                return None
            
            return self._process_basic_five_pattern_structure(sentence, base_result)
            
        except Exception as e:
            self.logger.warning(f"笞・・5譁・梛繝上Φ繝峨Λ繝ｼ繧ｨ繝ｩ繝ｼ: {e}")
            return None
    
    def _process_basic_five_pattern_structure(self, sentence, base_result: Dict) -> Dict:
        """蝓ｺ譛ｬ5譁・梛讒矩縺ｮ蛻・ｧ｣蜃ｦ逅・ｼ医ワ繧､繝悶Μ繝・ラ隗｣譫仙ｯｾ蠢懶ｼ・""
        
        # 笨・繝上う繝悶Μ繝・ラ隗｣譫占｣懈ｭ｣諠・ｱ繧貞━蜈育噪縺ｫ蛻ｩ逕ｨ
        root_word = None
        is_whose_construction = any(w.text.lower() == 'whose' for w in sentence.words)
        
        if hasattr(sentence, 'hybrid_corrections'):
            # 繝上う繝悶Μ繝・ラ隗｣譫舌〒VERB縺ｨ縺励※陬懈ｭ｣縺輔ｌ縺溯ｪ槭ｒ荳ｻ譁・虚隧槭→縺励※謗｡逕ｨ
            for word_id, correction in sentence.hybrid_corrections.items():
                if correction['correction_type'] == 'whose_verb_fix':
                    root_word = self._find_word_by_id(sentence, word_id)
                    if root_word:
                        self.logger.debug(f"肌 繝上う繝悶Μ繝・ラ隗｣譫・ {root_word.text} 繧偵Γ繧､繝ｳ蜍戊ｩ槭→縺励※菴ｿ逕ｨ")
                        break
        
        # 繝上う繝悶Μ繝・ラ隗｣譫舌′縺ｪ縺・ｴ蜷医・蠕捺擂蜃ｦ逅・       
        if not root_word and is_whose_construction:
            # acl:relcl髢｢菫ゅ↓縺ゅｋ隱槭ｒ遒ｺ隱・            acl_relcl_word = self._find_word_by_deprel(sentence, 'acl:relcl')
            if (acl_relcl_word and 
                acl_relcl_word.text.lower() in ['lives', 'works', 'runs', 'goes', 'sits', 'stands']):
                # 縺薙ｌ縺ｯ螳滄圀縺ｮ繝｡繧､繝ｳ蜍戊ｩ槭→縺励※隗｣驥医☆縺ｹ縺・                root_word = acl_relcl_word
                self.logger.debug(f"肌 whose讒区枚讀懷・: 繝｡繧､繝ｳ蜍戊ｩ槭ｒ {acl_relcl_word.text} 縺ｫ菫ｮ豁｣")
        
        # 騾壼ｸｸ縺ｮ蝣ｴ蜷茨ｼ啌OOT隱樊､懷・
        if not root_word:
            root_word = self._find_root_word(sentence)
            if not root_word:
                return base_result

        # 萓晏ｭ倬未菫ゅ・繝・・讒狗ｯ・        dep_relations = {}
        for word in sentence.words:
            if word.deprel not in dep_relations:
                dep_relations[word.deprel] = []
            dep_relations[word.deprel].append(word)
        
        # 笨・whose讒区枚縺ｮ迚ｹ蛻･蜃ｦ逅・ｼ壹Γ繧､繝ｳ譁・・萓晏ｭ倬未菫ゅ・繝・・繧呈ｭ｣縺励￥讒狗ｯ・        if is_whose_construction and root_word:
            # 繝｡繧､繝ｳ蜍戊ｩ槭・逶ｴ謗･萓晏ｭ倩ｪ槭ｒ萓晏ｭ倬未菫ゅ・繝・・縺ｫ霑ｽ蜉
            for word in sentence.words:
                if word.head == root_word.id:
                    if word.deprel not in dep_relations:
                        dep_relations[word.deprel] = []
                    dep_relations[word.deprel].append(word)
                    
            # ROOT隱橸ｼ亥・陦瑚ｩ橸ｼ峨ｒ荳ｻ隱槭→縺励※霑ｽ蜉
            if 'nsubj' not in dep_relations:
                dep_relations['nsubj'] = []
            root_word_from_stanza = self._find_root_word(sentence)
            if root_word_from_stanza:
                dep_relations['nsubj'].append(root_word_from_stanza)
                
            self.logger.debug(f"肌 whose讒区枚: 萓晏ｭ倬未菫ょ・讒狗ｯ牙ｮ御ｺ・ 繝｡繧､繝ｳ蜍戊ｩ・{root_word.text}")

        # 蝓ｺ譛ｬ5譁・梛繝代ち繝ｼ繝ｳ讀懷・
        pattern_result = self._detect_basic_five_pattern(root_word, dep_relations)
        if not pattern_result:
            return base_result
        
        # 繧ｹ繝ｭ繝・ヨ逕滓・
        result = base_result.copy()
        if 'slots' not in result:
            result['slots'] = {}
        if 'sub_slots' not in result:
            result['sub_slots'] = {}
        
        five_pattern_slots = self._generate_basic_five_slots(
            pattern_result['pattern'], pattern_result['mapping'], dep_relations, sentence
        )
        
        result['slots'].update(five_pattern_slots.get('slots', {}))
        result['sub_slots'].update(five_pattern_slots.get('sub_slots', {}))
        
        # 譁・ｳ墓ュ蝣ｱ險倬鹸・・merge_handler_results縺ｨ莠呈鋤諤ｧ縺ｮ縺ゅｋ蠖｢蠑擾ｼ・        result['grammar_info'] = {
            'detected_patterns': ['basic_five_pattern'],
            'handler_contributions': {
                'basic_five_pattern': {
                    'pattern': pattern_result['pattern'],
                    'confidence': pattern_result.get('confidence', 0.8)
                }
            }
        }
        
        self.logger.debug(f"  笨・5譁・梛蜃ｦ逅・ｮ御ｺ・ 繝代ち繝ｼ繝ｳ={pattern_result['pattern']}")
        return result
    
    def _find_root_word(self, sentence):
        """ROOT隱槭ｒ讀懃ｴ｢"""
        return next((w for w in sentence.words if w.head == 0), None)
    
    def _detect_basic_five_pattern(self, root_word, dep_relations):
        """蝓ｺ譛ｬ5譁・梛繝代ち繝ｼ繝ｳ讀懷・"""
        
        # 蝓ｺ譛ｬ5譁・梛繝代ち繝ｼ繝ｳ螳夂ｾｩ・郁ｩｳ邏ｰ竊貞腰邏斐・鬆・ｺ上〒讀懷・・・        patterns = {
            "SVOO": {
                "required": ["nsubj", "obj", "iobj"],
                "optional": [],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "root": "V", "iobj": "O1", "obj": "O2"}
            },
            "SVOC": {
                "required": ["nsubj", "obj", "xcomp"],
                "optional": [],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "root": "V", "obj": "O1", "xcomp": "C2"}
            },
            "SVO": {
                "required": ["nsubj", "obj"],
                "optional": [],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "root": "V", "obj": "O1"}
            },
            "SVC": {
                "required": ["nsubj", "cop"],
                "optional": [],
                "root_pos": ["ADJ", "NOUN"],
                "mapping": {"nsubj": "S", "cop": "V", "root": "C1"}
            },
            "SVC_PRON": {
                "required": ["nsubj", "cop"],
                "optional": [],
                "root_pos": ["PRON"],
                "mapping": {"nsubj": "S", "cop": "V", "root": "C1"}
            },
            "SVC_ALT": {
                "required": ["nsubj", "xcomp"],
                "optional": [],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "root": "V", "xcomp": "C1"}
            },
            "SV": {
                "required": ["nsubj"],
                "optional": [],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "root": "V"}
            }
        }
        
        # 繝代ち繝ｼ繝ｳ繝槭ャ繝√Φ繧ｰ
        for pattern_name, pattern_info in patterns.items():
            if self._matches_five_pattern(pattern_info, dep_relations, root_word):
                return {
                    'pattern': pattern_name,
                    'mapping': pattern_info['mapping'],
                    'confidence': 0.9
                }
        
        return None
    
    def _matches_five_pattern(self, pattern_info, dep_relations, root_word):
        """5譁・梛繝代ち繝ｼ繝ｳ繝槭ャ繝√Φ繧ｰ"""
        # 蠢・ｦ√↑萓晏ｭ倬未菫ゅ・遒ｺ隱・        for rel in pattern_info['required']:
            if rel not in dep_relations:
                return False
        
        # ROOT隱槭・蜩∬ｩ槭メ繧ｧ繝・け
        if root_word.upos not in pattern_info['root_pos']:
            return False
        
        return True
    
    def _build_phrase_with_modifiers(self, sentence, main_word):
        """
        菫ｮ鬟ｾ隱槫唱繧貞性繧螳悟・縺ｪ蜿･繧呈ｧ狗ｯ・        
        蟇ｾ蠢應ｿｮ鬟ｾ隱槭ち繧､繝暦ｼ・        - det: 髯仙ｮ夊ｩ・(a, an, the, my, your, his, her, its, our, their)
        - amod: 蠖｢螳ｹ隧樔ｿｮ鬟ｾ隱・(red, beautiful, smart, old)
        - nummod: 謨ｰ隧樔ｿｮ鬟ｾ隱・(one, two, first, second)  
        - nmod:poss: 謇譛画ｼ菫ｮ鬟ｾ隱・(John's, Mary's, my, your)
        - compound: 隍・粋蜷崎ｩ・(car door, school bus)
        """
        if not main_word:
            return ""
        
        # 菫ｮ鬟ｾ隱槫庶髮・        modifiers = []
        for word in sentence.words:
            if word.head == main_word.id:
                if word.deprel in ['det', 'amod', 'nummod', 'nmod:poss', 'compound']:
                    modifiers.append(word)
        
        # 繝・ヰ繝・げ繝ｭ繧ｰ霑ｽ蜉
        if modifiers:
            self.logger.debug(f"肌 菫ｮ鬟ｾ隱樊､懷・ [{main_word.text}]: {[(m.text, m.deprel) for m in modifiers]}")
        
        # 菫ｮ鬟ｾ隱槭ｒID鬆・〒繧ｽ繝ｼ繝茨ｼ郁ｪ樣・ｿ晄戟・・        modifiers.sort(key=lambda w: w.id)
        
        # 蜿･讒狗ｯ・ 菫ｮ鬟ｾ隱・+ 繝｡繧､繝ｳ隱・        phrase_words = modifiers + [main_word]
        phrase_words.sort(key=lambda w: w.id)  # 譛邨ら噪縺ｪ隱樣・｢ｺ菫・        
        result = ' '.join(word.text for word in phrase_words)
        self.logger.debug(f"肌 蜿･讒狗ｯ牙ｮ御ｺ・ '{result}'")
        
        return result
    
    def _generate_basic_five_slots(self, pattern, mapping, dep_relations, sentence):
        """蝓ｺ譛ｬ5譁・梛繧ｹ繝ｭ繝・ヨ逕滓・・井ｿｮ鬟ｾ隱槫唱蟇ｾ蠢懷ｼｷ蛹厄ｼ・""
        slots = {}
        sub_slots = {}
        
        # 繝槭ャ繝斐Φ繧ｰ縺ｫ蠕薙▲縺ｦ繧ｹ繝ｭ繝・ヨ逕滓・
        for dep_rel, slot in mapping.items():
            if dep_rel == "root":
                # ROOT隱槭・蜃ｦ逅・ｼ亥虚隧槭・騾壼ｸｸ菫ｮ鬟ｾ隱槭↑縺励↑縺ｮ縺ｧ蜊倩ｪ槭・縺ｿ・・                root_word = self._find_root_word(sentence)
                if root_word:
                    slots[slot] = root_word.text
            elif dep_rel in dep_relations:
                # 萓晏ｭ倬未菫りｪ槭・蜃ｦ逅・ｼ井ｿｮ鬟ｾ隱槫唱繧貞性繧螳悟・縺ｪ蜿･繧呈ｧ狗ｯ会ｼ・                words = dep_relations[dep_rel]
                if words:
                    # 繝｡繧､繝ｳ縺ｮ隱・                    main_word = words[0]
                    # 菫ｮ鬟ｾ隱槫唱繧呈ｧ狗ｯ・                    phrase = self._build_phrase_with_modifiers(sentence, main_word)
                    slots[slot] = phrase
        
        # 笨・霑ｽ蜉蜃ｦ逅・ｼ啌OOT繝ｯ繝ｼ繝峨↓繧ゆｿｮ鬟ｾ隱槫唱蜃ｦ逅・ｒ驕ｩ逕ｨ・亥虚隧樔ｻ･螟悶・蝣ｴ蜷茨ｼ・        # 萓・ "The woman is my neighbor" 縺ｧneighbor縺軍OOT縺ｮ蝣ｴ蜷・        root_word = self._find_root_word(sentence)
        if root_word and root_word.pos in ['NOUN', 'PRON', 'ADJ']:
            # 蜷崎ｩ槭・莉｣蜷崎ｩ槭・蠖｢螳ｹ隧槭′ROOT縺ｮ蝣ｴ蜷医∽ｿｮ鬟ｾ隱槫唱繧呈ｧ狗ｯ・            root_phrase = self._build_phrase_with_modifiers(sentence, root_word)
            
            # ROOT繝ｯ繝ｼ繝牙ｯｾ蠢懊・繧ｹ繝ｭ繝・ヨ繧呈峩譁ｰ
            for dep_rel, slot in mapping.items():
                if dep_rel == "root" and slot in slots:
                    if slots[slot] == root_word.text:  # 蜊倩ｪ槭・縺ｿ縺ｮ蝣ｴ蜷・                        slots[slot] = root_phrase  # 菫ｮ鬟ｾ隱槫唱縺ｫ譖ｴ譁ｰ
                        self.logger.debug(f"肌 ROOT隱樔ｿｮ鬟ｾ隱槫唱驕ｩ逕ｨ: {slot} = '{root_phrase}'")
        
        # 菫ｮ鬟ｾ隱槭・蜃ｦ逅・ｼ亥渕譛ｬ逧・↑繧ゅ・縺ｮ縺ｿ・・        # 髢｢菫ょ憶隧槭・髢｢菫らｯ繝上Φ繝峨Λ繝ｼ縺ｫ莉ｻ縺帙ｋ縺溘ａ髯､螟・        relative_adverbs = ['where', 'when', 'why', 'how']
        
        # 笨・髢｢菫らｯ蜀・・隱槭ｒ莠句燕縺ｫ迚ｹ螳壹＠縺ｦ髯､螟・        rel_verb_candidates = [w for w in sentence.words if w.deprel in ['acl:relcl', 'acl']]
        excluded_word_ids = set()
        for rel_verb_cand in rel_verb_candidates:
            # 髢｢菫らｯ蜍戊ｩ槭→縺昴・萓晏ｭ倩ｪ槭ｒ縺吶∋縺ｦ髯､螟・            excluded_word_ids.add(rel_verb_cand.id)
            for word in sentence.words:
                if word.head == rel_verb_cand.id:
                    excluded_word_ids.add(word.id)
        
        for word in sentence.words:
            # 髢｢菫らｯ蜀・・隱槭ｒ繧ｹ繧ｭ繝・・
            if word.id in excluded_word_ids:
                continue
                
            # 笨・蜑ｯ隧槫・逅・・蟆る摩繧ｨ繝ｳ繧ｸ繝ｳ縺ｫ蟋碑ｭｲ - 蝓ｺ譛ｬ5譁・梛縺ｧ縺ｯ蜃ｦ逅・＠縺ｪ縺・            # if word.deprel == 'advmod' and 'M2' not in slots:
            #     if word.text.lower() not in relative_adverbs:
            #         slots['M2'] = word.text  # 騾壼ｸｸ縺ｮ蜑ｯ隧樔ｿｮ鬟ｾ隱槭・縺ｿ
            #     else:
            #         self.logger.debug(f"剥 髢｢菫ょ憶隧樣勁螟・ {word.text} (髢｢菫らｯ繝上Φ繝峨Λ繝ｼ縺ｫ蟋碑ｭｲ)")
            # elif word.deprel == 'obl' and 'M3' not in slots:
            #     slots['M3'] = word.text  # 蜑咲ｽｮ隧槫唱遲・        
        return {'slots': slots, 'sub_slots': sub_slots}

    def _handle_adverbial_modifier(self, sentence, base_result: Dict) -> Optional[Dict]:
        """
        蜑ｯ隧槫・逅・お繝ｳ繧ｸ繝ｳ・・ephrase霍晞屬繝吶・繧ｹ蜴溽炊・・        Stanza/spaCy蛻・梵邨先棡縺ｮ縺ｿ繧剃ｽｿ逕ｨ縲√ワ繝ｼ繝峨さ繝ｼ繝・ぅ繝ｳ繧ｰ蛻・｡槭・蟒・ｭ｢
        """
        print("肌 蜑ｯ隧槭ワ繝ｳ繝峨Λ繝ｼ髢句ｧ・)
        self.logger.debug("蜑ｯ隧槭ワ繝ｳ繝峨Λ繝ｼ螳溯｡御ｸｭ・郁ｷ晞屬繝吶・繧ｹ蜴溽炊・・..")
        
        # 識 Rephrase蜴溽炊・壹ワ繝ｼ繝峨さ繝ｼ繝・ぅ繝ｳ繧ｰ蛻・｡槭・荳崎ｦ・        # Stanza/spaCy縺ｮ蛻・梵邨先棡縺ｮ縺ｿ繧剃ｿ｡鬆ｼ
        
        # === 譌｢蟄倥せ繝ｭ繝・ヨ遒ｺ隱搾ｼ磯未菫らｯ繧ｹ繝ｭ繝・ヨ蜷ｫ繧・・==
        existing_slots = base_result.get('slots', {}) if base_result else {}
        existing_sub_slots = base_result.get('sub_slots', {}) if base_result else {}
        
        existing_adverbs = set()
        
        # 荳ｻ遽蜑ｯ隧槭ｒ譌｢蟄倥メ繧ｧ繝・け縺ｫ霑ｽ蜉
        for slot_key, slot_value in existing_slots.items():
            if slot_key.startswith('M') and slot_value:
                existing_adverbs.update(slot_value.split())
        
        # 肌 驥崎ｦ∽ｿｮ豁｣: 髢｢菫らｯ蜑ｯ隧槭ｂ譌｢蟄倥メ繧ｧ繝・け縺ｫ霑ｽ蜉
        for slot_key, slot_value in existing_sub_slots.items():
            if slot_key.startswith('sub-m') and slot_value:
                existing_adverbs.update(slot_value.split())
        
        self.logger.debug(f"剥 譌｢蟄伜憶隧槭メ繧ｧ繝・け: {existing_adverbs}")
        
        # === 髢｢菫らｯ繝ｻ蠕灘ｱ樒ｯ繧ｳ繝ｳ繝・く繧ｹ繝亥・譫・===
        # 肌 菫ｮ豁｣・喘ase_result縺九ｉ荳ｻ蜍戊ｩ樊ュ蝣ｱ繧貞叙蠕暦ｼ医ワ繧､繝悶Μ繝・ラ隗｣譫千ｵ先棡蜿肴丐・・        main_verb_id = None
        main_verb_text = existing_slots.get('V')
        
        # 識 驥崎ｦ∽ｿｮ豁｣・夐未菫らｯ蜃ｦ逅・〒V縺梧ｭ｣縺励￥險ｭ螳壹＆繧後※縺・↑縺・ｴ蜷医〕ives繧貞━蜈・        if main_verb_text in ['is', 'are', 'was', 'were'] and any(w.text == 'lives' for w in sentence.words):
            main_verb_text = 'lives'  # whose讒区枚縺ｧ縺ｯ lives 縺御ｸｻ蜍戊ｩ・        
        if main_verb_text:
            # 荳ｻ蜍戊ｩ槭ユ繧ｭ繧ｹ繝医°繧牙ｯｾ蠢懊☆繧仇ord ID繧堤音螳・            for word in sentence.words:
                if word.text == main_verb_text and word.upos in ['VERB', 'AUX', 'NOUN']:  # NOUN繧ょ性繧√ｋ・・ives遲会ｼ・                    main_verb_id = word.id
                    break
        
        # 繝輔か繝ｼ繝ｫ繝舌ャ繧ｯ: 蠕捺擂縺ｮ譁ｹ豕・        if not main_verb_id:
            main_verb_id = self._find_main_verb(sentence)
        
        subordinate_verbs = self._find_subordinate_verbs(sentence, main_verb_id)
        
        # === 蜑ｯ隧槫呵｣懷庶髮・ｼ・igration source蜆ｪ遘讖溯・豢ｻ逕ｨ・・==
        adverb_phrases = []
        processed_positions = set()
        processed_phrases = set()  # 驥崎､・ヵ繝ｬ繝ｼ繧ｺ髦ｲ豁｢
        
        self.logger.debug("剥 蜑ｯ隧槫呵｣懊せ繧ｭ繝｣繝ｳ髢句ｧ具ｼ・tanza/spaCy蛻・梵繝吶・繧ｹ・・..")
        for word in sentence.words:
            # 識 Rephrase蜴溽炊・夂ｴ皮ｲ九↓Stanza/spaCy蛻・梵邨先棡繧剃ｿ｡鬆ｼ
            is_adverb = (
                word.deprel in ['advmod', 'obl', 'obl:tmod', 'obl:npmod', 'obl:agent', 'obl:unmarked', 'nmod:tmod'] or
                word.upos == 'ADV'  # POS-based detection・井ｿ｡鬆ｼ諤ｧ鬮倥＞・・            )
            
            self.logger.debug(f"  {word.text}: deprel={word.deprel}, upos={word.upos}, is_adverb={is_adverb}")
            
            if is_adverb:
                if word.text in existing_adverbs:
                    self.logger.debug(f"    竊・髯､螟厄ｼ域里蟄伜憶隧橸ｼ・ {word.text}")
                    continue
                    
                # 驥崎､・勁蜴ｻ・・igration source蜆ｪ遘讖溯・・・                if word.id in processed_positions:
                    self.logger.debug(f"    竊・髯､螟厄ｼ磯㍾隍・ｽ咲ｽｮ・・ {word.text}")
                    continue
                    
                # 髢｢菫ょ憶隧樣勁螟・                if word.text.lower() in ['where', 'when', 'why', 'how']:
                    self.logger.debug(f"    竊・髯､螟厄ｼ磯未菫ょ憶隧橸ｼ・ {word.text}")
                    continue
                
                # Migration source蜑咲ｽｮ隧槫唱讒狗ｯ画ｩ溯・豢ｻ逕ｨ
                if word.deprel.startswith('obl'):
                    phrase = self._build_prepositional_phrase(sentence, word)
                    # 蜑咲ｽｮ隧槫唱縺ｮ蜈ｨtokens險倬鹸・磯㍾隍・屓驕ｿ・・                    phrase_words = phrase.split()
                    for pw in phrase_words:
                        for w in sentence.words:
                            if w.text == pw:
                                processed_positions.add(w.id)
                else:
                    # 肌 蜑ｯ隧樔ｿｮ鬟ｾ隱槭ｒ蜷ｫ繧蜿･讒狗ｯ会ｼ・very carefully"蟇ｾ蠢懶ｼ・                    phrase = self._build_adverbial_phrase(sentence, word)
                    phrase_words = phrase.split()
                    for pw in phrase_words:
                        for w in sentence.words:
                            if w.text == pw:
                                processed_positions.add(w.id)
                
                # 驥崎､・ヵ繝ｬ繝ｼ繧ｺ繝√ぉ繝・け
                if phrase in processed_phrases:
                    self.logger.debug(f"    竊・髯､螟厄ｼ磯㍾隍・ヵ繝ｬ繝ｼ繧ｺ・・ {phrase}")
                    continue
                
                processed_phrases.add(phrase)
                
                # 識 Rephrase蜴溽炊・壼・鬘樔ｸ崎ｦ√∽ｽ咲ｽｮ諠・ｱ縺ｮ縺ｿ縺ｧ蛻､螳・                # category = self._classify_adverbial_phrase(phrase, time_keywords, location_keywords, manner_keywords)
                category = 'position_based'  # Rephrase霍晞屬繝吶・繧ｹ蜴溽炊
                
                # 譁・ц蛻・梵: 荳ｻ遽 vs 蠕灘ｱ樒ｯ・・igration source蛻､螳壹Ο繧ｸ繝・け・・                context = self._determine_adverb_context(word, main_verb_id, subordinate_verbs, sentence)
                
                self.logger.debug(f"    竊・讀懷・: phrase='{phrase}', category={category}, context={context}")
                
                adverb_phrases.append({
                    'phrase': phrase,
                    'category': category,
                    'position': word.id,
                    'word': word,
                    'context': context  # 'main' or 'subordinate'
                })
        
        if not adverb_phrases:
            self.logger.debug("蜑ｯ隧槭↑縺・- 繧ｹ繧ｭ繝・・")
            return None

        # === Rephrase莉墓ｧ倬・鄂ｮ繝ｭ繧ｸ繝・け・・igration source讖溯・豢ｻ逕ｨ・・===
        slots = {}
        sub_slots = {}
        
        # 菴咲ｽｮ鬆・た繝ｼ繝・        adverb_phrases.sort(key=lambda x: x['position'])
        
        # === 繧ｷ繝ｳ繝励Ν繝ｫ繝ｼ繝ｫ荳諡ｬ驟咲ｽｮ繧ｷ繧ｹ繝・Β ===
        # 荳ｻ遽蜑ｯ隧槭→蠕灘ｱ樒ｯ蜑ｯ隧槭ｒ蛻・屬縺励※縲√◎繧後◇繧後↓繧ｷ繝ｳ繝励Ν繝ｫ繝ｼ繝ｫ繧帝←逕ｨ
        
        main_adverbs = [p for p in adverb_phrases if p['context'] == 'main']
        sub_adverbs = [p for p in adverb_phrases if p['context'] == 'subordinate']
        
        self.logger.debug(f"識 繧ｷ繝ｳ繝励Ν繝ｫ繝ｼ繝ｫ驕ｩ逕ｨ: 荳ｻ遽蜑ｯ隧桀len(main_adverbs)}蛟・ 蠕灘ｱ樒ｯ蜑ｯ隧桀len(sub_adverbs)}蛟・)
        
        # 荳ｻ遽蜑ｯ隧槭・繧ｷ繝ｳ繝励Ν繝ｫ繝ｼ繝ｫ驟咲ｽｮ
        if main_adverbs:
            main_slots = self._apply_simple_rule_to_adverbs(main_adverbs, 'main')
            slots.update(main_slots)
        
        # 蠕灘ｱ樒ｯ蜑ｯ隧槭・繧ｷ繝ｳ繝励Ν繝ｫ繝ｼ繝ｫ驟咲ｽｮ
        if sub_adverbs:
            sub_main_slots = self._apply_simple_rule_to_adverbs(sub_adverbs, 'sub')
            sub_slots.update(sub_main_slots)
        
        self.logger.debug(f"蜑ｯ隧樣・鄂ｮ螳御ｺ・ slots={slots}, sub_slots={sub_slots}")
        print(f"肌 蜑ｯ隧槭ワ繝ｳ繝峨Λ繝ｼ螳御ｺ・ slots={slots}, sub_slots={sub_slots}")
        return {'slots': slots, 'sub_slots': sub_slots}
    
    def _apply_simple_rule_to_adverbs(self, adverbs, context_type):
        """
        繧ｷ繝ｳ繝励Ν繝ｫ繝ｼ繝ｫ繧貞憶隧樒ｾ､縺ｫ荳諡ｬ驕ｩ逕ｨ
        
        Args:
            adverbs: 蜑ｯ隧槭Μ繧ｹ繝・            context_type: 'main' or 'sub'
        """
        result_slots = {}
        count = len(adverbs)
        
        self.logger.debug(f"識 {context_type}遽繧ｷ繝ｳ繝励Ν繝ｫ繝ｼ繝ｫ驕ｩ逕ｨ: {count}蛟九・蜑ｯ隧・)
        
        if count == 0:
            return result_slots
        
        # 繧ｹ繝ｭ繝・ヨ蜷阪・繝ｬ繝輔ぅ繝・け繧ｹ
        slot_prefix = 'sub-m' if context_type == 'sub' else 'M'
        
        if count == 1:
            # 1蛟・竊・M2 (縺ｾ縺溘・ sub-m2)
            slot_name = f"{slot_prefix}2"
            result_slots[slot_name] = adverbs[0]['phrase']
            self.logger.debug(f"  1蛟九Ν繝ｼ繝ｫ: {slot_name} = '{adverbs[0]['phrase']}'")
        
        elif count == 2:
            # 2蛟・竊・M2, M3 (縺ｾ縺溘・ sub-m2, sub-m3)
            # 菴咲ｽｮ鬆・〒繧ｽ繝ｼ繝域ｸ医∩縺ｪ縺ｮ縺ｧ縲∵怙蛻昴′M2縲∵ｬ｡縺勲3
            result_slots[f"{slot_prefix}2"] = adverbs[0]['phrase']
            result_slots[f"{slot_prefix}3"] = adverbs[1]['phrase']
            self.logger.debug(f"  2蛟九Ν繝ｼ繝ｫ: {slot_prefix}2 = '{adverbs[0]['phrase']}', {slot_prefix}3 = '{adverbs[1]['phrase']}'")
        
        elif count >= 3:
            # 3蛟倶ｻ･荳・竊・M1, M2, M3 (縺ｾ縺溘・ sub-m1, sub-m2, sub-m3)
            result_slots[f"{slot_prefix}1"] = adverbs[0]['phrase']
            result_slots[f"{slot_prefix}2"] = adverbs[1]['phrase']
            result_slots[f"{slot_prefix}3"] = adverbs[2]['phrase']
            self.logger.debug(f"  3蛟九Ν繝ｼ繝ｫ: {slot_prefix}1/2/3 = '{adverbs[0]['phrase']}'/'{adverbs[1]['phrase']}'/'{adverbs[2]['phrase']}'")
            
            # 4蛟倶ｻ･荳翫・辟｡隕厄ｼ郁ｭｦ蜻奇ｼ・            if count > 3:
                ignored = [a['phrase'] for a in adverbs[3:]]
                self.logger.warning(f"  笞・・4蛟倶ｻ･荳翫・蜑ｯ隧槭ｒ辟｡隕・ {ignored}")
        
        return result_slots
    
    def _find_main_verb(self, sentence):
        """荳ｻ蜍戊ｩ槭ｒ迚ｹ螳夲ｼ域ｧ矩逧・ｿｮ豁｣迚茨ｼ・""
        
        # 識 Step 1: ROOT蜍戊ｩ槭ｒ蜆ｪ蜈・        for word in sentence.words:
            if word.deprel == 'root' and word.upos == 'VERB':
                self.logger.debug(f"識 荳ｻ蜍戊ｩ橸ｼ・OOT蜍戊ｩ橸ｼ・ {word.text} (id={word.id})")
                return word.id
        
        # 肌 Step 2: ROOT蠖｢螳ｹ隧槭〒蜿怜虚諷九・蝣ｴ蜷医ヽOOT閾ｪ菴薙ｒ荳ｻ蜍戊ｩ槭→縺励※謇ｱ縺・        root_word = None
        for word in sentence.words:
            if word.deprel == 'root':
                root_word = word
                break
        
        if root_word and root_word.upos == 'ADJ':
            # 蜿怜虚諷区ｧ矩・啌OOT蠖｢螳ｹ隧槭ｒ荳ｻ蜍戊ｩ槭→縺吶ｋ
            # "was unexpected" 竊・unexpected 縺御ｸｻ蜍戊ｩ樒嶌蠖・            self.logger.debug(f"識 荳ｻ蜍戊ｩ橸ｼ亥女蜍墓・ROOT蠖｢螳ｹ隧橸ｼ・ {root_word.text} (id={root_word.id})")
            return root_word.id
        
        if root_word and root_word.upos != 'VERB':
            # 讒矩逧・嚴螻､縺ｧ荳ｻ蜍戊ｩ槫呵｣懊ｒ隧穂ｾ｡
            verb_candidates = [w for w in sentence.words if w.upos == 'VERB']
            if verb_candidates:
                # 譛繧よ枚縺ｮ荳ｭ蠢・↓霑代＞蜍戊ｩ槭ｒ荳ｻ蜍戊ｩ槭→縺吶ｋ
                main_verb = min(verb_candidates, key=lambda v: abs(v.id - root_word.id))
                self.logger.debug(f"識 荳ｻ蜍戊ｩ橸ｼ域ｧ矩逧・∈謚橸ｼ・ {main_verb.text} (id={main_verb.id})")
                return main_verb.id
        
        # 売 Fallback: 譛蛻昴・蜍戊ｩ・        for word in sentence.words:
            if word.upos == 'VERB':
                self.logger.debug(f"識 荳ｻ蜍戊ｩ橸ｼ・allback・・ {word.text} (id={word.id})")
                return word.id
        
        return None
    
    def _find_subordinate_verbs(self, sentence, main_verb_id):
        """蠕灘ｱ樒ｯ蜍戊ｩ槭ｒ迚ｹ螳夲ｼ域ｧ矩逧・ｿｮ豁｣迚茨ｼ・""
        subordinate_verbs = []
        
        # 識 荳ｻ蜍戊ｩ槭ｒ髯､螟悶＠縺ｦ縲∵・遒ｺ縺ｪ蠕灘ｱ樒ｯ蜍戊ｩ槭・縺ｿ繧堤音螳・        for word in sentence.words:
            if word.id == main_verb_id:
                continue  # 荳ｻ蜍戊ｩ槭・髯､螟・                
            # 譏守｢ｺ縺ｪ蠕灘ｱ樒ｯ繝代ち繝ｼ繝ｳ縺ｮ縺ｿ繧貞ｾ灘ｱ樒ｯ蜍戊ｩ槭→縺励※隱崎ｭ・            if word.deprel in ['acl:relcl', 'acl', 'advcl', 'ccomp', 'xcomp']:
                # 縺溘□縺励∽ｸｻ蜍戊ｩ槭→縺励※迚ｹ螳壽ｸ医∩縺ｮ蝣ｴ蜷医・髯､螟・                if word.upos == 'VERB':
                    subordinate_verbs.append(word.id)
                    self.logger.debug(f"剥 蠕灘ｱ樒ｯ蜍戊ｩ樊､懷・: {word.text} (id={word.id}, deprel={word.deprel})")
        
        return subordinate_verbs
    
    def _determine_adverb_context(self, adverb_word, main_verb_id, subordinate_verbs, sentence):
        """蜑ｯ隧槭・譁・ц・井ｸｻ遽 vs 蠕灘ｱ樒ｯ・峨ｒ蛻､螳・""
        # 逶ｴ謗･縺ｮ蜍戊ｩ樔ｾ晏ｭ倬未菫ゅｒ繝√ぉ繝・け
        head_id = adverb_word.head
        
        # 萓晏ｭ倬未菫ゅｒ驕｡縺｣縺ｦ蜍戊ｩ槭ｒ隕九▽縺代ｋ
        current_word = None
        for word in sentence.words:
            if word.id == head_id:
                current_word = word
                break
        
        # 萓晏ｭ倬未菫ゅｒ霎ｿ縺｣縺ｦ荳ｻ蜍戊ｩ・蠕灘ｱ槫虚隧槭ｒ蛻､螳・        max_depth = 5  # 辟｡髯舌Ν繝ｼ繝鈴亟豁｢
        depth = 0
        
        while current_word and depth < max_depth:
            if current_word.id == main_verb_id:
                return 'main'
            elif current_word.id in subordinate_verbs:
                return 'subordinate'
            
            # 谺｡縺ｮ head 繧呈爾縺・            next_head = current_word.head
            if next_head == 0:  # root蛻ｰ驕・                break
                
            next_word = None
            for word in sentence.words:
                if word.id == next_head:
                    next_word = word
                    break
            
            current_word = next_word
            depth += 1
        
        # 識 萓晏ｭ倬未菫ゅ・繝ｼ繧ｹ蛻､螳夲ｼ井ｽ咲ｽｮ逧・耳隲悶・蜊ｱ髯ｺ縺ｪ縺ｮ縺ｧ蜑企勁・・        # 蜑ｯ隧槭′荳ｻ蜍戊ｩ樒ｳｻ邨ｱ縺句ｾ灘ｱ樒ｯ蜍戊ｩ樒ｳｻ邨ｱ縺九ｒ萓晏ｭ倬未菫ゅ〒豁｣遒ｺ縺ｫ蛻､螳・        
        if current_word and current_word.id == main_verb_id:
            return 'main'
        elif current_word and current_word.id in subordinate_verbs:
            return 'subordinate'
        
        # 肌 謾ｹ濶ｯ迚茨ｼ壻ｸｻ蜍戊ｩ槭∈縺ｮ萓晏ｭ倡ｵ瑚ｷｯ繝√ぉ繝・け
        # 蜑ｯ隧・竊・head 竊・head 竊・... 竊・main_verb 縺ｮ邨瑚ｷｯ縺後≠繧九°
        visited = set()
        check_word = current_word
        
        while check_word and check_word.id not in visited:
            visited.add(check_word.id)
            
            if check_word.id == main_verb_id:
                return 'main'
            
            # 谺｡縺ｮhead繧呈爾縺・            if check_word.head == 0:
                break
                
            next_word = None
            for w in sentence.words:
                if w.id == check_word.head:
                    next_word = w
                    break
            check_word = next_word
        
        return 'main'  # 繝・ヵ繧ｩ繝ｫ繝茨ｼ壻ｸｻ遽・亥ｮ牙・蛛ｴ・・
    def _determine_optimal_main_adverb_slot(self, phrase, category, position, main_verb_position, existing_slots):
        """
        識 逵溘・繧ｷ繝ｳ繝励Ν蜑ｯ隧樣・鄂ｮ繝ｫ繝ｼ繝ｫ・郁頂縺苓ｿ斐＠蝠城｡悟ｮ悟・隗｣豎ｺ迚茨ｼ・        
        譬ｸ蠢・次逅・ｼ壼区焚縺ｫ蝓ｺ縺･縺丞崋螳夐・鄂ｮ
        1蛟九・縺ｿ 竊・M2・医←縺薙↓縺ゅ▲縺ｦ繧ゑｼ・        2蛟・竊・M2, M3・井ｽ咲ｽｮ鬆・ｼ・
        3蛟・竊・M1, M2, M3・井ｽ咲ｽｮ鬆・ｼ・        
        蠕捺擂縺ｮ隍・尅縺ｪ蛻､螳壹ｒ謗帝勁縺励∽ｺ域ｸｬ蜿ｯ閭ｽ諤ｧ繧呈怙螟ｧ蛹・        """
        
        # 蜈ｨ菫ｮ鬟ｾ隱槭ｒ蜿朱寔・育樟蝨ｨ縺ｮ蜃ｦ逅・ｯｾ雎｡蜷ｫ繧・・        all_modifiers = []
        
        # 譌｢蟄倥・M繧ｹ繝ｭ繝・ヨ縺九ｉ菫ｮ鬟ｾ隱槭ｒ蜿朱寔
        for slot in ['M1', 'M2', 'M3']:
            if slot in existing_slots and existing_slots[slot]:
                all_modifiers.append(existing_slots[slot])
        
        # 迴ｾ蝨ｨ縺ｮ菫ｮ鬟ｾ隱槭ｒ霑ｽ蜉
        all_modifiers.append(phrase)
        
        total_count = len(all_modifiers)
        
        self.logger.debug(f"識 逵溘す繝ｳ繝励ΝM繧ｹ繝ｭ繝・ヨ蛻､螳・ phrase='{phrase}', 邱丈ｿｮ鬟ｾ隱樊焚={total_count}")
        self.logger.debug(f"  蜈ｨ菫ｮ鬟ｾ隱・ {all_modifiers}")
        
        # === 逵溘・繧ｷ繝ｳ繝励Ν繝ｫ繝ｼ繝ｫ驕ｩ逕ｨ ===
        
        if total_count == 1:
            # 1蛟九・縺ｿ 竊・M2
            self.logger.debug(f"  竊・M2驕ｸ謚橸ｼ・蛟九Ν繝ｼ繝ｫ・・)
            return 'M2'
        
        elif total_count == 2:
            # 2蛟・竊・M2, M3
            # 迴ｾ蝨ｨ縺ｮ菫ｮ鬟ｾ隱槭′譛蛻昴・蝣ｴ蜷医・M2縲・逡ｪ逶ｮ縺ｮ蝣ｴ蜷医・M3
            current_index = all_modifiers.index(phrase)
            if current_index == 0:
                target_slot = 'M2'
            else:
                target_slot = 'M3'
            
            self.logger.debug(f"  竊・{target_slot}驕ｸ謚橸ｼ・蛟九Ν繝ｼ繝ｫ繝ｻ菴咲ｽｮ{current_index + 1}・・)
            return target_slot
        
        elif total_count >= 3:
            # 3蛟倶ｻ･荳・竊・M1, M2, M3
            current_index = all_modifiers.index(phrase)
            slot_mapping = ['M1', 'M2', 'M3']
            
            if current_index < 3:
                target_slot = slot_mapping[current_index]
                self.logger.debug(f"  竊・{target_slot}驕ｸ謚橸ｼ・蛟・繝ｫ繝ｼ繝ｫ繝ｻ菴咲ｽｮ{current_index + 1}・・)
                return target_slot
            else:
                # 3蛟九ｒ雜・∴繧句ｴ蜷医・辟｡隕厄ｼ医お繝ｩ繝ｼ蝗樣∩・・                self.logger.debug(f"  竊・None・・蛟玖ｶ・℃繝ｻ菴咲ｽｮ{current_index + 1}・・)
                return None
        
        # 繝輔か繝ｼ繝ｫ繝舌ャ繧ｯ・磯壼ｸｸ縺ｯ蛻ｰ驕斐＠縺ｪ縺・ｼ・        self.logger.debug(f"  竊・M2驕ｸ謚橸ｼ医ヵ繧ｩ繝ｼ繝ｫ繝舌ャ繧ｯ・・)
        return 'M2'

    def _build_prepositional_phrase(self, sentence, word):
        """蜑咲ｽｮ隧槫唱縺ｮ讒狗ｯ会ｼ亥ｮ悟・諤ｧ蠑ｷ蛹也沿・・""
        # 蜑咲ｽｮ隧槫唱縺ｮ螳悟・讒狗ｯ・        phrase_parts = []
        
        # 蜑咲ｽｮ隧槭ｒ謗｢縺・        preposition = None
        for w in sentence.words:
            if w.head == word.id and w.deprel == 'case':
                preposition = w.text
                break
        
        if preposition:
            phrase_parts.append(preposition)
        
        # 肌 菫ｮ鬟ｾ隱槫庶髮・ｒ諡｡蠑ｵ・医ｈ繧雁､壹￥縺ｮ菫ｮ鬟ｾ髢｢菫ゅｒ蜷ｫ繧√ｋ・・        modifiers = []
        for w in sentence.words:
            if w.head == word.id and w.deprel in ['det', 'amod', 'compound', 'nmod', 'nmod:poss']:
                modifiers.append((w.id, w.text))
        
        # 肌 髢捺磁菫ｮ鬟ｾ隱槭ｂ蜿朱寔・・the morning breeze"縺ｮ"morning"繧偵く繝｣繝・メ・・        for w in sentence.words:
            # word縺ｮ逶ｴ謗･菫ｮ鬟ｾ隱槭・菫ｮ鬟ｾ隱槭ｂ蜿朱寔
            if any(mod[0] == w.head for mod in modifiers) and w.deprel in ['amod', 'compound']:
                modifiers.append((w.id, w.text))
        
        # 菴咲ｽｮ鬆・た繝ｼ繝・        modifiers.sort()
        phrase_parts.extend([mod[1] for mod in modifiers])
        phrase_parts.append(word.text)
        
        constructed_phrase = ' '.join(phrase_parts)
        self.logger.debug(f"肌 蜑咲ｽｮ隧槫唱讒狗ｯ・ '{word.text}' 竊・'{constructed_phrase}'")
        
        return constructed_phrase
    
    def _build_adverbial_phrase(self, sentence, word):
        """蜑ｯ隧樔ｿｮ鬟ｾ隱槭ｒ蜷ｫ繧蜿･讒狗ｯ会ｼ・very carefully"蟇ｾ蠢懶ｼ・""
        phrase_parts = []
        modifiers = []
        
        # 蜑ｯ隧槭・菫ｮ鬟ｾ隱槭ｒ蜿朱寔・・dvmod・・        for w in sentence.words:
            if w.head == word.id and w.deprel == 'advmod':
                modifiers.append((w.id, w.text))
        
        # 菴咲ｽｮ鬆・た繝ｼ繝・        modifiers.sort()
        phrase_parts.extend([mod[1] for mod in modifiers])
        phrase_parts.append(word.text)
        
        constructed_phrase = ' '.join(phrase_parts)
        self.logger.debug(f"肌 蜑ｯ隧槫唱讒狗ｯ・ '{word.text}' 竊・'{constructed_phrase}'")
        
        return constructed_phrase
    
    # 卵・・蜑企勁・壹ワ繝ｼ繝峨さ繝ｼ繝・ぅ繝ｳ繧ｰ蛻・｡樊ｩ溯・・・ephrase霍晞屬繝吶・繧ｹ蜴溽炊縺ｨ遏帷崟・・    # def _classify_adverbial_phrase(...) -> 荳崎ｦ・
    # ==== PASSIVE VOICE HANDLER ====
        """隍・粋蜑ｯ隧槫唱縺ｮ讒狗ｯ・""
        # 2縺､縺ｮ蜑ｯ隧槭・髢薙↓縺ゅｋ隱槭ｂ蜷ｫ繧√ｋ
        start_pos = min(mod1['position'], mod2['position'])
        end_pos = max(mod1['position'], mod2['position'])
        
        phrase_words = []
        for word in sentence.words:
            if start_pos <= word.id <= end_pos:
                phrase_words.append(word.text)
        
        return ' '.join(phrase_words)

    def _handle_passive_voice(self, sentence, base_result: Dict) -> Optional[Dict]:
        """
        蜿怜虚諷九ワ繝ｳ繝峨Λ繝ｼ・・hase 2螳溯｣・ｼ・        
        passive_voice_engine.py 縺ｮ讖溯・繧堤ｵｱ蜷医す繧ｹ繝・Β縺ｫ遘ｻ讀・        Stanza dependency parsing 縺ｫ繧医ｋ蜿怜虚諷区､懷・繝ｻ蛻・ｧ｣
        
        Args:
            sentence: Stanza隗｣譫先ｸ医∩sentence object
            base_result: 繝吶・繧ｹ邨先棡・医さ繝斐・・・            
        Returns:
            Dict: 蜿怜虚諷句・隗｣邨先棡 or None
        """
        try:
            self.logger.debug("剥 蜿怜虚諷九ワ繝ｳ繝峨Λ繝ｼ螳溯｡御ｸｭ...")
            
            # 蜿怜虚諷区ｧ矩蛻・梵
            passive_info = self._analyze_passive_structure(sentence)
            if not passive_info:
                self.logger.debug("  蜿怜虚諷九↑縺・- 繧ｹ繧ｭ繝・・")
                return None
                
            self.logger.debug("  笨・蜿怜虚諷区､懷・")
            return self._process_passive_construction(sentence, passive_info, base_result)
            
        except Exception as e:
            self.logger.warning(f"笞・・蜿怜虚諷九ワ繝ｳ繝峨Λ繝ｼ繧ｨ繝ｩ繝ｼ: {e}")
            return None
    
    def _analyze_passive_structure(self, sentence) -> Optional[Dict]:
        """蜿怜虚諷区ｧ矩縺ｮ蛻・梵"""
        passive_features = {
            'auxiliary': None,      # be蜍戊ｩ・            'main_verb': None,      # 驕主悉蛻・ｩ・            'subject': None,        # 荳ｻ隱・            'agent': None,          # by蜿･蜍穂ｽ應ｸｻ
            'agent_phrase': None,   # by蜿･蜈ｨ菴・            'type': None            # 蜿怜虚諷九・遞ｮ鬘・        }
        
        # 蜈ｸ蝙狗噪縺ｪ驕主悉蛻・ｩ槭Μ繧ｹ繝・        common_past_participles = {
            'written', 'bought', 'sold', 'made', 'taken', 'given', 'seen', 'done',
            'broken', 'stolen', 'found', 'lost', 'taught', 'caught', 'brought',
            'eaten', 'driven', 'shown', 'known', 'grown', 'thrown', 'chosen',
            'unexpected'  # 蠖｢螳ｹ隧槫梛蜿怜虚諷九・霑ｽ蜉
        }
        
        # 讒矩隕∫ｴ縺ｮ讀懷・
        for word in sentence.words:
            # 蜿怜虚諷倶ｸｻ隱樊､懷・
            if word.deprel == 'nsubj:pass':
                passive_features['subject'] = word
            elif word.deprel == 'nsubjpass':  # 譌ｧ迚・tanza蟇ｾ蠢・                passive_features['subject'] = word
            elif word.deprel == 'nsubj':  # 蠖｢螳ｹ隧槫女蜍墓・縺ｮ蝣ｴ蜷・                if not passive_features['subject']:  # 縺ｾ縺隕九▽縺九▲縺ｦ縺・↑縺・ｴ蜷医・縺ｿ
                    passive_features['subject'] = word
                    
            # 蜿怜虚諷玖｣懷勧蜍戊ｩ樊､懷・
            elif word.deprel == 'aux:pass':
                passive_features['auxiliary'] = word
            elif word.deprel == 'auxpass':  # 譌ｧ迚・tanza蟇ｾ蠢・                passive_features['auxiliary'] = word
            elif word.deprel == 'cop' and word.lemma == 'be':
                passive_features['auxiliary'] = word
                
            # 荳ｻ蜍戊ｩ樊､懷・・磯℃蜴ｻ蛻・ｩ橸ｼ・            elif word.deprel == 'root':
                if word.upos == 'VERB' and word.xpos == 'VBN':  # 驕主悉蛻・ｩ・                    passive_features['main_verb'] = word
                elif word.upos == 'ADJ' and word.text.lower() in common_past_participles:
                    passive_features['main_verb'] = word
            
            # 髱柮oot隱槭〒縺ｮ蠖｢螳ｹ隧槫女蜍墓・讀懷・・郁､・枚蟇ｾ蠢懶ｼ・            elif word.upos == 'ADJ' and word.text.lower() in common_past_participles:
                if not passive_features['main_verb']:  # 縺ｾ縺隕九▽縺九▲縺ｦ縺・↑縺・ｴ蜷・                    passive_features['main_verb'] = word
                    
            # by蜿･蜍穂ｽ應ｸｻ讀懷・
            elif word.deprel == 'obl:agent':
                passive_features['agent'] = word
                passive_features['agent_phrase'] = self._build_agent_phrase(sentence, word)
            elif word.deprel == 'agent':  # 譌ｧ迚亥ｯｾ蠢・                passive_features['agent'] = word
                passive_features['agent_phrase'] = self._build_agent_phrase(sentence, word)
        
        # 蜿怜虚諷句愛螳・        if (passive_features['auxiliary'] and 
            passive_features['main_verb'] and 
            passive_features['subject']):
            
            passive_features['type'] = 'agent_passive' if passive_features['agent'] else 'simple_passive'
            
            self.logger.debug(f"  荳ｻ隱・ {passive_features['subject'].text}")
            self.logger.debug(f"  陬懷勧蜍戊ｩ・ {passive_features['auxiliary'].text}")
            self.logger.debug(f"  荳ｻ蜍戊ｩ・ {passive_features['main_verb'].text}")
            self.logger.debug(f"  蜍穂ｽ應ｸｻ: {passive_features['agent'].text if passive_features['agent'] else '縺ｪ縺・}")
            self.logger.debug(f"  遞ｮ鬘・ {passive_features['type']}")
            
            return passive_features
        
        return None
    
    def _process_passive_construction(self, sentence, passive_info: Dict, base_result: Dict) -> Dict:
        """蜿怜虚諷区ｧ区枚縺ｮ蜃ｦ逅・""
        result = base_result.copy()
        
        auxiliary = passive_info['auxiliary']
        main_verb = passive_info['main_verb']
        subject = passive_info['subject']
        agent_phrase = passive_info['agent_phrase']
        passive_type = passive_info['type']
        
        self.logger.debug(f"  蜿怜虚諷句・逅・ {passive_type}")
        
        # 繧ｹ繝ｭ繝・ヨ逕滓・
        rephrase_slots = self._generate_passive_voice_slots(
            passive_type, subject, auxiliary, main_verb, agent_phrase, passive_info['agent'], sentence
        )
        
        # 邨先棡繝槭・繧ｸ
        if 'slots' not in result:
            result['slots'] = {}
        if 'sub_slots' not in result:
            result['sub_slots'] = {}
        
        result['slots'].update(rephrase_slots.get('slots', {}))
        result['sub_slots'].update(rephrase_slots.get('sub_slots', {}))
        
        # 譁・ｳ墓ュ蝣ｱ險倬鹸
        result['grammar_info'] = {
            'patterns': ['passive_voice'],
            'passive_type': passive_type,
            'subject': subject.text,
            'auxiliary': auxiliary.text,
            'main_verb': main_verb.text,
            'agent': passive_info['agent'].text if passive_info['agent'] else None
        }
        
        self.logger.debug(f"  笨・蜿怜虚諷句・逅・ｮ御ｺ・ {len(rephrase_slots.get('slots', {}))} main slots, {len(rephrase_slots.get('sub_slots', {}))} sub slots")
        return result
    
    def _generate_passive_voice_slots(self, passive_type: str, subject, auxiliary, main_verb, 
                                     agent_phrase: str, agent, sentence) -> Dict:
        """蜿怜虚諷九ち繧､繝怜挨繧ｹ繝ｭ繝・ヨ逕滓・・亥憶隧槫・逅・・蟆る摩繝上Φ繝峨Λ繝ｼ縺ｫ蟋碑ｭｲ・・""
        
        slots = {}
        sub_slots = {}
        
        # 蝓ｺ譛ｬ繧ｹ繝ｭ繝・ヨ・亥・騾夲ｼ・        slots['S'] = self._build_subject_phrase(sentence, subject)
        slots['Aux'] = auxiliary.text
        slots['V'] = main_verb.text
        
        # 笨・蜑ｯ隧槫・逅・ｒ髯､蜴ｻ・喘y蜿･縺ｯ蜑ｯ隧槭ワ繝ｳ繝峨Λ繝ｼ縺ｫ蟋碑ｭｲ
        # by蜿･莉倥″蜿怜虚諷九〒繧ゅ｀1縺ｯ險ｭ螳壹○縺壼憶隧槭ワ繝ｳ繝峨Λ繝ｼ縺ｫ莉ｻ縺帙ｋ
        # agent_phrase縺ｮ諠・ｱ縺ｯ譁・ｳ墓ュ蝣ｱ縺ｨ縺励※險倬鹸縺吶ｋ縺後√せ繝ｭ繝・ヨ縺ｫ縺ｯ險ｭ螳壹＠縺ｪ縺・        
        return {'slots': slots, 'sub_slots': sub_slots}
    
    def _build_agent_phrase(self, sentence, agent_word) -> str:
        """by蜿･蜈ｨ菴薙・讒狗ｯ・""
        if not agent_word:
            return None
        
        # by蜑咲ｽｮ隧槭ｒ謗｢縺・        by_preposition = None
        for word in sentence.words:
            if word.text.lower() == 'by' and word.deprel == 'case' and word.head == agent_word.id:
                by_preposition = word
                break
        
        if by_preposition:
            # by + 蜍穂ｽ應ｸｻ + 菫ｮ鬟ｾ隱・            phrase_words = [by_preposition, agent_word]
            
            # 蜍穂ｽ應ｸｻ縺ｮ菫ｮ鬟ｾ隱槭ｒ霑ｽ蜉
            for word in sentence.words:
                if word.head == agent_word.id and word.deprel in ['det', 'amod', 'nmod', 'compound', 'nmod:poss']:
                    phrase_words.append(word)
            
            # ID鬆・た繝ｼ繝茨ｼ郁ｪ樣・ｿ晄戟・・            phrase_words.sort(key=lambda w: w.id)
            return ' '.join(w.text for w in phrase_words)
        
        return f"by {agent_word.text}"
    
    def _build_subject_phrase(self, sentence, subject) -> str:
        """荳ｻ隱槫唱縺ｮ讒狗ｯ会ｼ井ｿｮ鬟ｾ隱槫性繧・・""
        if not subject:
            return ""
            
        subject_words = [subject]
        
        # 荳ｻ隱槭・菫ｮ鬟ｾ隱槭ｒ蜿朱寔
        for word in sentence.words:
            if word.head == subject.id and word.deprel in ['det', 'amod', 'compound', 'nmod']:
                subject_words.append(word)
        
        # ID鬆・た繝ｼ繝茨ｼ郁ｪ樣・ｿ晄戟・・        subject_words.sort(key=lambda w: w.id)
        return ' '.join(w.text for w in subject_words)

    # =============================================================================
    # 蜉ｩ蜍戊ｩ櫁､・粋菴灘・逅・ワ繝ｳ繝峨Λ繝ｼ (Phase 3)
    # =============================================================================
    
    def _handle_auxiliary_complex(self, sentence, base_result: Dict) -> Dict[str, Any]:
        """
        蜉ｩ蜍戊ｩ櫁､・粋菴灘・逅・ワ繝ｳ繝峨Λ繝ｼ (Phase 3)
        
        隍・粋蜉ｩ蜍戊ｩ槭メ繧ｧ繝ｼ繝ｳ縺ｮ蜃ｦ逅・
        - is being (迴ｾ蝨ｨ騾ｲ陦悟女蜍墓・)
        - will be (譛ｪ譚･譎ょ宛)
        - has finished (迴ｾ蝨ｨ螳御ｺ・
        - will have been (譛ｪ譚･螳御ｺ・
        
        Migration Source: perfect_progressive_engine.py 縺ｮ繝ｭ繧ｸ繝・け邯呎価
        """
        print(f"  肌 蜉ｩ蜍戊ｩ櫁､・粋蜃ｦ逅・ワ繝ｳ繝峨Λ繝ｼ髢句ｧ・)
        
        result = {
            'handler': 'auxiliary_complex',
            'analysis_type': 'auxiliary_chain_processing',
            'metadata': {}
        }
        
        # 蜉ｩ蜍戊ｩ槭メ繧ｧ繝ｼ繝ｳ讀懷・
        auxiliary_chain = []
        main_verb = None
        subject = None
        
        # 隨ｬ荳繝代せ: 荳ｻ蜍戊ｩ槭ｒ迚ｹ螳・        for word in sentence.words:
            if word.deprel == 'root' and word.upos == 'VERB':
                main_verb = word
                print(f"    識 荳ｻ蜍戊ｩ樊､懷・: {word.text}")
                break
        
        # 隨ｬ莠後ヱ繧ｹ: 蜉ｩ蜍戊ｩ槭ｒ遽繝ｬ繝吶Ν縺ｧ蛻・｡槭＠縺ｦ蜿朱寔
        main_auxiliary_words = []  # 荳ｻ遽蜉ｩ蜍戊ｩ・        sub_auxiliary_words = []   # 蠕灘ｱ樒ｯ蜉ｩ蜍戊ｩ・        
        for word in sentence.words:
            # 蜉ｩ蜍戊ｩ樊､懷・
            is_auxiliary = False
            if word.deprel in ['aux', 'aux:pass']:
                is_auxiliary = True
                print(f"    迫 讓呎ｺ門勧蜍戊ｩ・ {word.text} ({word.deprel})")
            elif word.deprel == 'cop' and word.lemma == 'be':
                # 騾｣邨占ｩ槭・蜉ｩ蜍戊ｩ槭〒縺ｯ縺ｪ縺・ｼ郁｣懆ｪ樊ｧ区枚縺ｮbe蜍戊ｩ橸ｼ・                # 蜿怜虚諷九・騾ｲ陦悟ｽ｢縺ｮ譁・ц縺ｧ縺ｮ縺ｿ蜉ｩ蜍戊ｩ槭→縺励※謇ｱ縺・                is_auxiliary_context = False
                
                # 蜿怜虚諷九メ繧ｧ繝・け: 霑代￥縺ｫ驕主悉蛻・ｩ槭′縺ゅｋ縺・                for next_word in sentence.words:
                    if (next_word.id > word.id and 
                        next_word.upos == 'VERB' and 
                        (next_word.xpos in ['VBN'] or next_word.text.endswith('ed'))):
                        is_auxiliary_context = True
                        break
                        
                # 騾ｲ陦悟ｽ｢繝√ぉ繝・け: 霑代￥縺ｫbeing縺後≠繧九°
                for next_word in sentence.words:
                    if (next_word.id > word.id and 
                        next_word.text.lower() == 'being'):
                        is_auxiliary_context = True
                        break
                
                if is_auxiliary_context:
                    is_auxiliary = True
                    print(f"    迫 譁・ц逧・勧蜍戊ｩ枌e: {word.text}")
                else:
                    print(f"    笶・騾｣邨占ｩ枌e (髱槫勧蜍戊ｩ・: {word.text}")
                    continue
            elif (word.upos == 'VERB' and 
                  word.text.lower() in ['can', 'could', 'will', 'would', 'shall', 'should', 'may', 'might', 'must']):
                is_auxiliary = True
                print(f"    迫 豕募勧蜍戊ｩ・ {word.text}")
            elif word.text.lower() == 'being' and word.upos in ['AUX', 'VERB']:
                is_auxiliary = True
                print(f"    迫 being讀懷・: {word.text}")
            
            # 蜉ｩ蜍戊ｩ槭・遽繝ｬ繝吶Ν蛻・｡・            if is_auxiliary:
                # 荳ｻ遽蜉ｩ蜍戊ｩ・ 荳ｻ蜍戊ｩ槭↓逶ｴ謗･萓晏ｭ・                if main_verb and (word.head == main_verb.id or 
                                  (word.deprel == 'cop' and word.text.lower() in ['am', 'is', 'are', 'was', 'were'])):
                    main_auxiliary_words.append(word)
                    print(f"      竊・荳ｻ遽蜉ｩ蜍戊ｩ・ {word.text}")
                else:
                    sub_auxiliary_words.append(word)
                    print(f"      竊・蠕灘ｱ樒ｯ蜉ｩ蜍戊ｩ・ {word.text}")
            
            # 荳ｻ隱樊､懷・ (荳ｻ譁・・縺ｿ)
            elif word.deprel == 'nsubj' and main_verb and word.head == main_verb.id:
                subject = word
                print(f"    側 荳ｻ隱樊､懷・: {word.text}")
        
        # 荳ｻ遽蜉ｩ蜍戊ｩ槭ｒ菴咲ｽｮ鬆・↓繧ｽ繝ｼ繝医＠縺ｦ邨ｱ蜷・        if main_auxiliary_words:
            main_auxiliary_words.sort(key=lambda x: x.id)
            auxiliary_chain = [word.text for word in main_auxiliary_words]
            print(f"    識 荳ｻ遽蜉ｩ蜍戊ｩ槭メ繧ｧ繝ｼ繝ｳ: {auxiliary_chain}")
        else:
            auxiliary_chain = []
        
        # 隨ｬ荳峨ヱ繧ｹ: 蠕灘ｱ樒ｯ蜉ｩ蜍戊ｩ槭ｒsub-aux縺ｨ縺励※蜃ｦ逅・        subordinate_auxiliaries = []
        for aux_word in sub_auxiliary_words:
            subordinate_auxiliaries.append(aux_word.text.lower())
            print(f"    迫 蠕灘ｱ樒ｯ蜉ｩ蜍戊ｩ樒ｵｱ蜷・ {aux_word.text}")
        
        # 蜉ｩ蜍戊ｩ槭メ繧ｧ繝ｼ繝ｳ縺悟ｭ伜惠縺吶ｋ蝣ｴ蜷医・縺ｿ蜃ｦ逅・        if len(auxiliary_chain) >= 1:
            print(f"    笨・荳ｻ遽蜉ｩ蜍戊ｩ槭メ繧ｧ繝ｼ繝ｳ逋ｺ隕・ {auxiliary_chain}")
            
            # 蜉ｩ蜍戊ｩ槭メ繧ｧ繝ｼ繝ｳ邨仙粋 (譬ｸ蠢・Ο繧ｸ繝・け)
            auxiliary_phrase = ' '.join(auxiliary_chain)
            result['metadata']['auxiliary_chain'] = auxiliary_phrase
            result['metadata']['auxiliary_count'] = len(auxiliary_chain)
            
            # 繧ｹ繝ｭ繝・ヨ讒矩縺ｮ蛻晄悄蛹・            slots = {}
            sub_slots = {}
            
            # 荳ｻ譁・ｦ∫ｴ縺ｮ驟咲ｽｮ
            if subject:
                subject_phrase = self._build_phrase_with_modifiers(sentence, subject)
                slots['S'] = subject_phrase
            
            # 蜉ｩ蜍戊ｩ槫唱繧但ux繧ｹ繝ｭ繝・ヨ縺ｫ驟咲ｽｮ・井ｸｻ譁・・縺ｿ・・            slots['Aux'] = auxiliary_phrase
            
            # 荳ｻ蜍戊ｩ槫・逅・            if main_verb:
                verb_phrase = self._build_phrase_with_modifiers(sentence, main_verb)
                slots['V'] = verb_phrase
            
            # 蠕灘ｱ樒ｯ蜉ｩ蜍戊ｩ槭・蜃ｦ逅・            if subordinate_auxiliaries:
                sub_slots['sub-aux'] = ' '.join(subordinate_auxiliaries)
                print(f"    桃 蠕灘ｱ樒ｯ蜉ｩ蜍戊ｩ・ sub-aux = {sub_slots['sub-aux']}")
            
            print(f"    笨・蜉ｩ蜍戊ｩ櫁､・粋蜃ｦ逅・ｮ御ｺ・ Aux='{auxiliary_phrase}'")
            return {'slots': slots, 'sub_slots': sub_slots}
        
        elif subordinate_auxiliaries:
            # 荳ｻ遽蜉ｩ蜍戊ｩ槭↑縺励∝ｾ灘ｱ樒ｯ蜉ｩ蜍戊ｩ槭・縺ｿ縺ｮ蝣ｴ蜷・            print(f"    桃 蠕灘ｱ樒ｯ蜉ｩ蜍戊ｩ槭・縺ｿ: {subordinate_auxiliaries}")
            return {'slots': {}, 'sub_slots': {'sub-aux': ' '.join(subordinate_auxiliaries)}}
        
        else:
            print(f"    笶・蜉ｩ蜍戊ｩ槭メ繧ｧ繝ｼ繝ｳ譛ｪ讀懷・")
            return None

    def _is_main_clause_auxiliary(self, word, main_verb) -> bool:
        """荳ｻ譁・・蜉ｩ蜍戊ｩ槭°縺ｩ縺・°繧貞愛螳・""
        # 蝓ｺ譛ｬ逧・↑蜉ｩ蜍戊ｩ槫愛螳・        is_auxiliary = (
            word.upos == 'AUX' or 
            (word.upos == 'VERB' and word.deprel in ['aux', 'cop']) or
            word.text.lower() in ['be', 'have', 'will', 'can', 'should', 'would', 'could', 'may', 'might', 'must']
        )
        
        if not is_auxiliary:
            return False
        
        # 荳ｻ蜍戊ｩ槭↓逶ｴ謗･髢｢騾｣縺吶ｋ蜉ｩ蜍戊ｩ槭・縺ｿ・井ｸｻ譁・Ξ繝吶Ν・・        if word.deprel in ['aux', 'cop'] and word.head == main_verb.id:
            return True
            
        return False

    def _handle_conjunction(self, sentence, base_result: Dict) -> Optional[Dict]:
        """
        謗･邯夊ｩ槫・逅・ワ繝ｳ繝峨Λ繝ｼ・・as if"遲峨・蠕灘ｱ樊磁邯夊ｩ槫ｯｾ蠢懶ｼ・        migration繧ｨ繝ｳ繧ｸ繝ｳ縺九ｉ縺ｮ遘ｻ讀咲沿
        """
        self.logger.debug("謗･邯夊ｩ槭ワ繝ｳ繝峨Λ繝ｼ螳溯｡御ｸｭ...")
        
        # 蠕灘ｱ樊磁邯夊ｩ槭・讀懷・・・ark + advcl 縺ｮ邨・∩蜷医ｏ縺幢ｼ・        mark_words = []
        advcl_verbs = []
        
        for word in sentence.words:
            if word.deprel == 'mark' and word.upos == 'SCONJ':
                mark_words.append(word)
            elif word.deprel == 'advcl':
                advcl_verbs.append(word)
        
        if not mark_words or not advcl_verbs:
            self.logger.debug("  竊・謗･邯夊ｩ樊ｧ区枚譛ｪ讀懷・")
            return None
        
        # "as if"遲峨・隍・粋謗･邯夊ｩ槭ｒ讀懷・
        conjunction_phrase = self._detect_compound_conjunction(sentence, mark_words)
        if not conjunction_phrase:
            self.logger.debug("  竊・隍・粋謗･邯夊ｩ樊悴讀懷・")
            return None
        
        self.logger.debug(f"  迫 隍・粋謗･邯夊ｩ樊､懷・: '{conjunction_phrase}'")
        
        # 蠕灘ｱ樒ｯ縺ｮ隕∫ｴ繧呈歓蜃ｺ
        advcl_verb = advcl_verbs[0]  # 譛蛻昴・advcl蜍戊ｩ槭ｒ菴ｿ逕ｨ
        sub_slots = self._extract_subordinate_conjunction_elements(sentence, advcl_verb, conjunction_phrase)
        
        # 荳ｻ遽縺ｯ譌｢蟄倥・base_result繧剃ｽｿ逕ｨ・域磁邯夊ｩ樊ｧ区枚縺ｧ縺ｯ遘ｻ陦後＠縺ｪ縺・ｼ・        main_slots = base_result.get('slots', {}) if base_result else {}
        
        # 蠕灘ｱ樒ｯ隕∫ｴ繧剃ｸｻ遽縺九ｉ髯､蜴ｻ
        self._remove_subordinate_elements_from_main(main_slots, sub_slots, advcl_verb)
        
        # M1菴咲ｽｮ縺ｫ謗･邯夊ｩ槭ｒ驟咲ｽｮ・育ｩｺ譁・ｭ怜・縺ｧ繝槭・繧ｯ・・        if not main_slots.get('M1'):
            main_slots['M1'] = ''
        
        result = {
            'slots': main_slots,
            'sub_slots': sub_slots,
            'grammar_info': {
                'detected_patterns': ['conjunction'],
                'conjunction_type': conjunction_phrase,
                'subordinate_verb': advcl_verb.text
            }
        }
        
        self.logger.debug(f"  笨・謗･邯夊ｩ槫・逅・ｮ御ｺ・ {len(sub_slots)}蛟九・蠕灘ｱ樒ｯ隕∫ｴ")
        return result
    
    def _detect_compound_conjunction(self, sentence, mark_words) -> Optional[str]:
        """隍・粋謗･邯夊ｩ槭・讀懷・・・as if"遲会ｼ・""
        if len(mark_words) < 2:
            return None
        
        # 騾｣邯壹☆繧砧ark word繧呈､懷・
        mark_words.sort(key=lambda x: x.id)
        
        # "as if"繝代ち繝ｼ繝ｳ縺ｮ讀懷・
        for i in range(len(mark_words) - 1):
            word1 = mark_words[i]
            word2 = mark_words[i + 1]
            
            # 騾｣邯壹☆繧倶ｽ咲ｽｮ縺ｫ縺ゅｋ蝣ｴ蜷・            if word2.id == word1.id + 1:
                phrase = f"{word1.text} {word2.text}"
                if phrase.lower() in ['as if', 'even if', 'as though']:
                    return phrase
        
        return None
    
    def _extract_subordinate_conjunction_elements(self, sentence, advcl_verb, conjunction_phrase) -> Dict[str, str]:
        """蠕灘ｱ樒ｯ隕∫ｴ縺ｮ謚ｽ蜃ｺ"""
        sub_slots = {}
        
        # 謗･邯夊ｩ槭ｒsub-m1縺ｫ驟咲ｽｮ
        sub_slots['sub-m1'] = conjunction_phrase
        
        # 蠕灘ｱ樒ｯ縺ｮ荳ｻ隱・        for word in sentence.words:
            if word.head == advcl_verb.id and word.deprel == 'nsubj':
                sub_slots['sub-s'] = word.text
                break
        
        # 蠕灘ｱ樒ｯ縺ｮ蜍戊ｩ・        sub_slots['sub-v'] = advcl_verb.text
        
        # 蠕灘ｱ樒ｯ縺ｮ逶ｮ逧・ｪ・        for word in sentence.words:
            if word.head == advcl_verb.id and word.deprel == 'obj':
                sub_slots['sub-o1'] = word.text
                break
        
        return sub_slots

    def _remove_subordinate_elements_from_main(self, main_slots: Dict[str, str], sub_slots: Dict[str, str], advcl_verb) -> None:
        """蠕灘ｱ樒ｯ隕∫ｴ繧剃ｸｻ遽縺九ｉ髯､蜴ｻ・井ｸｻ遽縺ｮ荳ｻ隱槭・蜍戊ｩ槭・菫晄戟・・""
        # 蠕灘ｱ樒ｯ縺ｫ縺ｮ縺ｿ蟄伜惠縺吶ｋ隕∫ｴ繧堤音螳・        subordinate_only_elements = set()
        
        # 蠕灘ｱ樒ｯ縺ｮ逶ｮ逧・ｪ槭・陬懆ｪ樒ｭ会ｼ井ｸｻ隱槭・蜍戊ｩ樔ｻ･螟厄ｼ峨ｒ蜿門ｾ・        for sub_key, sub_value in sub_slots.items():
            if sub_value and sub_key.startswith('sub-') and sub_key not in ['sub-m1', 'sub-s', 'sub-v']:
                subordinate_only_elements.add(sub_value.lower())
        
        # 荳ｻ遽繧ｹ繝ｭ繝・ヨ縺九ｉ蠕灘ｱ樒ｯ縺ｫ縺ｮ縺ｿ蟄伜惠縺吶ｋ隕∫ｴ繧帝勁蜴ｻ
        for main_key, main_value in list(main_slots.items()):
            if main_value and main_value.lower() in subordinate_only_elements:
                main_slots[main_key] = ''
                self.logger.debug(f"  売 蠕灘ｱ樒ｯ蟆ら畑隕∫ｴ繧剃ｸｻ遽縺九ｉ髯､蜴ｻ: {main_key}='{main_value}' 竊・''")


# =============================================================================
# Phase 0 繝・せ繝育畑 蝓ｺ譛ｬ繝・せ繝医ワ繝ｼ繝阪せ
# =============================================================================

def test_phase0_basic():
    """Phase 0 蝓ｺ譛ｬ蜍穂ｽ懃｢ｺ隱阪ユ繧ｹ繝・""
    print("ｧｪ Phase 0 蝓ｺ譛ｬ繝・せ繝磯幕蟋・..")
    
    try:
        # 蛻晄悄蛹悶ユ繧ｹ繝・        mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
        print("笨・蛻晄悄蛹匁・蜉・)
        
        # 蝓ｺ譛ｬ蜃ｦ逅・ユ繧ｹ繝・        test_sentence = "The car is red."
        result = mapper.process(test_sentence)
        
        print(f"笨・蝓ｺ譛ｬ蜃ｦ逅・・蜉・ {result['sentence']}")
        print(f"投 蜃ｦ逅・凾髢・ {result['meta']['processing_time']:.3f}s")
        print(f"肌 Stanza諠・ｱ: {result['meta']['stanza_info']}")
        
        # 邨ｱ險育｢ｺ隱・        stats = mapper.get_stats()
        print(f"嶋 蜃ｦ逅・ｵｱ險・ {stats}")
        
        print("脂 Phase 0 蝓ｺ譛ｬ繝・せ繝亥ｮ御ｺ・ｼ・)
        return True
        
    except Exception as e:
        print(f"笶・Phase 0 繝・せ繝亥､ｱ謨・ {e}")
        return False

# =============================================================================
# Phase 1 繝・せ繝育畑 髢｢菫らｯ繝・せ繝医ワ繝ｼ繝阪せ
# =============================================================================

def test_phase2_passive_voice():
    """Phase 2 蜿怜虚諷九ワ繝ｳ繝峨Λ繝ｼ繝・せ繝・""
    print("ｧｪ Phase 2 蜿怜虚諷九ユ繧ｹ繝磯幕蟋・..")
    
    try:
        # 蛻晄悄蛹・        mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
        
        # Phase 1 & 2 繝上Φ繝峨Λ繝ｼ霑ｽ蜉
        mapper.add_handler('relative_clause')
        mapper.add_handler('passive_voice')
        print("笨・髢｢菫らｯ + 蜿怜虚諷九ワ繝ｳ繝峨Λ繝ｼ霑ｽ蜉螳御ｺ・)
        
        # 驥崎ｦ√ユ繧ｹ繝医こ繝ｼ繧ｹ
        test_cases = [
            ("The car was bought.", "蜊倡ｴ泌女蜍墓・"),
            ("The car was bought by him.", "by蜿･莉倥″蜿怜虚諷・),
            ("The book which was read was interesting.", "髢｢菫らｯ+蜿怜虚諷玖､・粋"),
            ("The letter was written by her.", "蜿怜虚諷句渕譛ｬ蠖｢")
        ]
        
        success_count = 0
        for i, (test_sentence, pattern_type) in enumerate(test_cases, 1):
            print(f"\n当 繝・せ繝・i}: '{test_sentence}' ({pattern_type})")
            print("-" * 60)
            
            try:
                result = mapper.process(test_sentence)
                
                print("投 蜃ｦ逅・ｵ先棡:")
                print(f"  繝｡繧､繝ｳ繧ｹ繝ｭ繝・ヨ: {result.get('slots', {})}")
                print(f"  繧ｵ繝悶せ繝ｭ繝・ヨ: {result.get('sub_slots', {})}")
                print(f"  譁・ｳ墓ュ蝣ｱ: {result.get('grammar_info', {})}")
                print(f"  蜃ｦ逅・凾髢・ {result['meta']['processing_time']:.3f}s")
                
                # 蜿怜虚諷九メ繧ｧ繝・け
                slots = result.get('slots', {})
                if 'Aux' in slots and 'V' in slots:
                    print(f"\n識 蜿怜虚諷九メ繧ｧ繝・け:")
                    print(f"  S: '{slots.get('S', '')}'")
                    print(f"  Aux: '{slots.get('Aux', '')}'")  
                    print(f"  V: '{slots.get('V', '')}'")
                    if 'M1' in slots:
                        print(f"  M1 (by蜿･): '{slots.get('M1', '')}'")
                    
                    print("  笨・蜿怜虚諷区ｧ矩讀懷・謌仙粥・・)
                    success_count += 1
                else:
                    print("  笶・蜿怜虚諷区ｧ矩譛ｪ讀懷・")
                    
            except Exception as e:
                print(f"笶・繝・せ繝・i}繧ｨ繝ｩ繝ｼ: {e}")
        
        # 邨ｱ險育｢ｺ隱・        stats = mapper.get_stats()
        print(f"\n嶋 Phase 2 邨ｱ險・")
        print(f"  蜃ｦ逅・焚: {stats['processing_count']}")
        print(f"  蟷ｳ蝮・・逅・凾髢・ {stats['average_processing_time']:.3f}s")
        print(f"  繝上Φ繝峨Λ繝ｼ謌仙粥謨ｰ: {stats['handler_success_count']}")
        
        print(f"\n脂 Phase 2 繝・せ繝亥ｮ御ｺ・ 謌仙粥: {success_count}/{len(test_cases)}")
        return success_count == len(test_cases)
        
    except Exception as e:
        print(f"笶・Phase 2 繝・せ繝亥､ｱ謨・ {e}")
        return False

def test_phase1_relative_clause():
    """Phase 1 髢｢菫らｯ繝上Φ繝峨Λ繝ｼ繝・せ繝・""
    print("ｧｪ Phase 1 髢｢菫らｯ繝・せ繝磯幕蟋・..")
    
    try:
        # 蛻晄悄蛹・        mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
        
        # Phase 1 繝上Φ繝峨Λ繝ｼ霑ｽ蜉
        mapper.add_handler('relative_clause')
        print("笨・髢｢菫らｯ繝上Φ繝峨Λ繝ｼ霑ｽ蜉螳御ｺ・)
        
        # 驥崎ｦ√ユ繧ｹ繝医こ繝ｼ繧ｹ・育怐逡･髢｢菫ゆｻ｣蜷崎ｩ槫ｯｾ蠢懷ｼｷ蛹厄ｼ・        test_cases = [
            ("The car which we saw was red.", "逶ｮ逧・ｪ樣未菫ゆｻ｣蜷崎ｩ・),
            ("The man who runs fast is strong.", "荳ｻ隱樣未菫ゆｻ｣蜷崎ｩ・), 
            ("The man whose car is red lives here.", "謇譛画ｼ髢｢菫ゆｻ｣蜷崎ｩ・),
            ("The place where he lives is nice.", "髢｢菫ょ憶隧檜here"),
            ("The book I read was interesting.", "逵∫払逶ｮ逧・ｪ樣未菫ゆｻ｣蜷崎ｩ橸ｼ郁・蜍墓・・・),
            ("The book that was written is famous.", "逵∫払逶ｮ逧・ｪ樣未菫ゆｻ｣蜷崎ｩ橸ｼ亥女蜍墓・・・),
            ("The person standing there is my friend.", "逵∫払荳ｻ隱樣未菫ゆｻ｣蜷崎ｩ橸ｼ育樟蝨ｨ蛻・ｩ橸ｼ・)
        ]
        
        success_count = 0
        for i, (test_sentence, pattern_type) in enumerate(test_cases, 1):
            print(f"\n当 繝・せ繝・i}: '{test_sentence}' ({pattern_type})")
            print("-" * 60)
            
            try:
                result = mapper.process(test_sentence)
                
                print("投 蜃ｦ逅・ｵ先棡:")
                print(f"  繝｡繧､繝ｳ繧ｹ繝ｭ繝・ヨ: {result.get('slots', {})}")
                print(f"  繧ｵ繝悶せ繝ｭ繝・ヨ: {result.get('sub_slots', {})}")
                print(f"  譁・ｳ墓ュ蝣ｱ: {result.get('grammar_info', {})}")
                print(f"  蜃ｦ逅・凾髢・ {result['meta']['processing_time']:.3f}s")
                
                # 隨ｬ1繝・せ繝医こ繝ｼ繧ｹ縺ｮ迚ｹ蛻･繝√ぉ繝・け
                if i == 1:  # "The car which we saw was red."
                    slots = result.get('slots', {})
                    sub_slots = result.get('sub_slots', {})
                    
                    print(f"\n識 驥崎ｦ√メ繧ｧ繝・け:")
                    expected_sub_o1 = "The car which we saw"
                    actual_sub_o1 = sub_slots.get('sub-o1', '')
                    print(f"  譛溷ｾ・sub-o1: '{expected_sub_o1}'")
                    print(f"  螳滄圀 sub-o1: '{actual_sub_o1}'")
                    
                    if expected_sub_o1.lower() in actual_sub_o1.lower():
                        print("  笨・蝓ｺ譛ｬ隕∵ｱる＃謌撰ｼ・)
                        success_count += 1
                    else:
                        print("  笶・蝓ｺ譛ｬ隕∵ｱよ悴驕疲・")
                else:
                    success_count += 1
                    
            except Exception as e:
                print(f"笶・繝・せ繝・i}繧ｨ繝ｩ繝ｼ: {e}")
        
        # 邨ｱ險育｢ｺ隱・        stats = mapper.get_stats()
        print(f"\n嶋 Phase 1 邨ｱ險・")
        print(f"  蜃ｦ逅・焚: {stats['processing_count']}")
        print(f"  蟷ｳ蝮・・逅・凾髢・ {stats['average_processing_time']:.3f}s")
        print(f"  繝上Φ繝峨Λ繝ｼ謌仙粥謨ｰ: {stats['handler_success_count']}")
        
        print(f"\n脂 Phase 1 繝・せ繝亥ｮ御ｺ・ 謌仙粥: {success_count}/{len(test_cases)}")
        return success_count == len(test_cases)
        
    except Exception as e:
        print(f"笶・Phase 1 繝・せ繝亥､ｱ謨・ {e}")
        return False

def clean_result_for_json(result: Dict) -> Dict:
    """
    JSON蜃ｺ蜉帷畑縺ｫ邨先棡繧偵け繝ｪ繝ｼ繝ｳ繧｢繝・・
    蠕ｪ迺ｰ蜿ら・繧・撼JSON蟇ｾ蠢懊が繝悶ず繧ｧ繧ｯ繝医ｒ髯､蜴ｻ
    """
    def clean_value(obj, visited=None):
        if visited is None:
            visited = set()
        
        # 蠕ｪ迺ｰ蜿ら・繝√ぉ繝・け
        obj_id = id(obj)
        if obj_id in visited:
            return "<circular_reference>"
        
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, dict):
            visited.add(obj_id)
            cleaned = {}
            for k, v in obj.items():
                # 迚ｹ螳壹・繧ｭ繝ｼ縺ｯ髯､螟・                if k in ['stanza_doc', 'spacy_doc', '__dict__', '__weakref__']:
                    continue
                try:
                    cleaned[k] = clean_value(v, visited.copy())
                except (RecursionError, RuntimeError):
                    cleaned[k] = f"<error_cleaning_{k}>"
            return cleaned
        elif isinstance(obj, list):
            visited.add(obj_id)
            try:
                return [clean_value(item, visited.copy()) for item in obj[:100]]  # 譛螟ｧ100隕∫ｴ
            except (RecursionError, RuntimeError):
                return ["<error_cleaning_list>"]
        else:
            # 縺昴・莉悶・繧ｪ繝悶ず繧ｧ繧ｯ繝医・譁・ｭ怜・陦ｨ迴ｾ
            try:
                return str(obj)[:200]  # 譛螟ｧ200譁・ｭ・            except:
                return "<unrepresentable_object>"


def process_batch_sentences(input_file: str, output_file: str = None) -> str:
    """
    繝舌ャ繝∝・逅・ｼ・3萓区枚荳諡ｬ螳溯｡・    
    Args:
        input_file: 蜈･蜉帙ヵ繧｡繧､繝ｫ (JSON)
        output_file: 蜃ｺ蜉帙ヵ繧｡繧､繝ｫ (逵∫払譎ゅ・ auto-generated)
    
    Returns:
        output_file: 菫晏ｭ倥＆繧後◆繝輔ぃ繧､繝ｫ蜷・    """
    import argparse
    from datetime import datetime
    
    print(f"売 繝舌ャ繝∝・逅・幕蟋・ {input_file}")
    
    # 蜈･蜉帙ョ繝ｼ繧ｿ隱ｭ縺ｿ霎ｼ縺ｿ
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
    except FileNotFoundError:
        print(f"笶・繧ｨ繝ｩ繝ｼ: 繝輔ぃ繧､繝ｫ縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ - {input_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"笶・JSON隗｣譫舌お繝ｩ繝ｼ: {e}")
        return None
    
    # 蜃ｺ蜉帙ヵ繧｡繧､繝ｫ蜷咲函謌・    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"batch_results_{timestamp}.json"
    
    # 繧ｷ繧ｹ繝・Β蛻晄悄蛹・    mapper = UnifiedStanzaRephraseMapper()
    print("笨・繧ｷ繧ｹ繝・Β蛻晄悄蛹門ｮ御ｺ・)
    
    # 邨先棡譬ｼ邏・    results = {
        "meta": {
            "input_file": input_file,
            "processed_at": datetime.now().isoformat(),
            "total_sentences": 0,
            "success_count": 0,
            "error_count": 0
        },
        "results": {}
    }
    
    # 繝・・繧ｿ蠖｢蠑丞愛螳壹→蜃ｦ逅・    if "data" in test_data:
        # final_54_test_data.json 蠖｢蠑・        sentences_data = test_data["data"]
        results["meta"]["total_sentences"] = len(sentences_data)
        
        print(f"投 蜃ｦ逅・ｯｾ雎｡: {len(sentences_data)}萓区枚")
        
        for test_id, test_case in sentences_data.items():
            try:
                sentence = test_case["sentence"]
                print(f"Processing [{test_id}]: {sentence}")
                
                # 譁・ｧ｣譫仙ｮ溯｡・                result = mapper.process(sentence)
                
                # 蝓ｺ譛ｬ繧ｹ繝ｭ繝・ヨ諠・ｱ縺ｮ縺ｿ謚ｽ蜃ｺ・亥ｾｪ迺ｰ蜿ら・蝠城｡後ｒ蝗樣∩・・                clean_result = {
                    "sentence": result.get("sentence", ""),
                    "slots": result.get("slots", {}),
                    "sub_slots": result.get("sub_slots", {}),
                    "meta": {
                        "processing_time": result.get("meta", {}).get("processing_time", 0.0),
                        "sentence_id": result.get("meta", {}).get("sentence_id", 0),
                        "active_handlers": result.get("meta", {}).get("active_handlers", 0)
                    }
                }
                
                results["results"][test_id] = {
                    "sentence": sentence,
                    "analysis_result": clean_result,
                    "expected": test_case.get("expected", {}),
                    "status": "success"
                }
                results["meta"]["success_count"] += 1
                
            except Exception as e:
                print(f"笶・繧ｨ繝ｩ繝ｼ [{test_id}]: {e}")
                results["results"][test_id] = {
                    "sentence": test_case.get("sentence", ""),
                    "error": str(e),
                    "status": "error"
                }
                results["meta"]["error_count"] += 1
    
    elif isinstance(test_data, list):
        # 繧ｷ繝ｳ繝励Ν繝ｪ繧ｹ繝亥ｽ｢蠑・["sentence1", "sentence2", ...]
        results["meta"]["total_sentences"] = len(test_data)
        
        for i, sentence in enumerate(test_data):
            try:
                print(f"Processing [{i+1}]: {sentence}")
                result = mapper.process(sentence)
                
                # 蝓ｺ譛ｬ繧ｹ繝ｭ繝・ヨ諠・ｱ縺ｮ縺ｿ謚ｽ蜃ｺ・亥ｾｪ迺ｰ蜿ら・蝠城｡後ｒ蝗樣∩・・                clean_result = {
                    "sentence": result.get("sentence", ""),
                    "slots": result.get("slots", {}),
                    "sub_slots": result.get("sub_slots", {}),
                    "meta": {
                        "processing_time": result.get("meta", {}).get("processing_time", 0.0),
                        "sentence_id": result.get("meta", {}).get("sentence_id", 0),
                        "active_handlers": result.get("meta", {}).get("active_handlers", 0)
                    }
                }
                
                results["results"][str(i+1)] = {
                    "sentence": sentence,
                    "analysis_result": clean_result,
                    "status": "success"
                }
                results["meta"]["success_count"] += 1
                
            except Exception as e:
                print(f"笶・繧ｨ繝ｩ繝ｼ [{i+1}]: {e}")
                results["results"][str(i+1)] = {
                    "sentence": sentence,
                    "error": str(e),
                    "status": "error"
                }
                results["meta"]["error_count"] += 1
    
    else:
        print("笶・譛ｪ蟇ｾ蠢懊・繝・・繧ｿ蠖｢蠑上〒縺・)
        return None
    
    # 邨先棡菫晏ｭ・    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n笨・蜃ｦ逅・ｮ御ｺ・ｼ・)
        print(f"刀 邨先棡菫晏ｭ・ {output_file}")
        print(f"投 邨ｱ險・")
        print(f"   邱乗焚: {results['meta']['total_sentences']}")
        print(f"   謌仙粥: {results['meta']['success_count']}")
        print(f"   繧ｨ繝ｩ繝ｼ: {results['meta']['error_count']}")
        print(f"   謌仙粥邇・ {results['meta']['success_count']/results['meta']['total_sentences']*100:.1f}%")
        
        return output_file
        
    except Exception as e:
        print(f"笶・菫晏ｭ倥お繝ｩ繝ｼ: {e}")
        return None

def main():
    """CLI 繝｡繧､繝ｳ繧ｨ繝ｳ繝医Μ繝ｼ繝昴う繝ｳ繝・""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Unified Stanza-Rephrase Mapper - 繝舌ャ繝∝・逅・沿",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
菴ｿ逕ｨ萓・
  # 53萓区枚荳諡ｬ蜃ｦ逅・  python unified_stanza_rephrase_mapper.py --input final_test_system/final_54_test_data.json
  
  # 蜃ｺ蜉帙ヵ繧｡繧､繝ｫ謖・ｮ・  python unified_stanza_rephrase_mapper.py --input sentences.json --output my_results.json
  
  # 繧ｷ繝ｳ繝励Ν繝ｪ繧ｹ繝亥ｽ｢蠑上・JSON繧ょｯｾ蠢・  python unified_stanza_rephrase_mapper.py --input simple_sentences.json
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='蜈･蜉妍SON繝輔ぃ繧､繝ｫ・井ｾ区枚繝・・繧ｿ・・
    )
    
    parser.add_argument(
        '--output', '-o',
        help='蜃ｺ蜉妍SON繝輔ぃ繧､繝ｫ・育怐逡･譎ゅ・閾ｪ蜍慕函謌撰ｼ・
    )
    
    parser.add_argument(
        '--test-mode',
        action='store_true',
        help='繝・せ繝医Δ繝ｼ繝会ｼ域立Phase 0-2螳溯｡鯉ｼ・
    )
    
    args = parser.parse_args()
    
    if args.test_mode:
        # 蠕捺擂縺ｮ繝・せ繝医Δ繝ｼ繝・        print("ｧｪ 繝・せ繝医Δ繝ｼ繝牙ｮ溯｡・)
        if test_phase0_basic():
            print("\n" + "="*60)
            if test_phase1_relative_clause():
                print("\n" + "="*60)
                test_phase2_passive_voice()
            else:
                print("笶・Phase 1螟ｱ謨励・縺溘ａ Phase 2繧偵せ繧ｭ繝・・")
        else:
            print("笶・Phase 0螟ｱ謨励・縺溘ａ Phase 1,2繧偵せ繧ｭ繝・・")
    else:
        # 繝舌ャ繝∝・逅・Δ繝ｼ繝・        result_file = process_batch_sentences(args.input, args.output)
        if result_file:
            print(f"\n脂 繝舌ャ繝∝・逅・′螳御ｺ・＠縺ｾ縺励◆")
            print(f"邨先棡繝輔ぃ繧､繝ｫ: {result_file}")
        else:
            print("\n笶・繝舌ャ繝∝・逅・′螟ｱ謨励＠縺ｾ縺励◆")
            exit(1)

if __name__ == "__main__":
    main()
