#!/usr/bin/env python3
"""
Imperative Sentence Engine - Priority 15

Handles imperative sentence structures:
- Commands: "Go!", "Stop!", "Run!"
- Polite requests: "Please come here.", "Please help me."
- Negative imperatives: "Don't go!", "Don't do that!"
- Imperative with subject: "You go first!", "Somebody help!"

Coverage: 25% frequency → +7% coverage rate
Patterns: Go!, Stop!, Please come here!, Don't run!, You sit down!
"""

import stanza
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import logging
import time

@dataclass
class ImperativeResult:
    """Result structure for imperative sentence analysis."""
    slots: Dict[str, str]
    confidence: float
    metadata: Dict[str, Any]
    success: bool
    processing_time: float
    error: Optional[str] = None

class ImperativeEngine:
    """
    Imperative sentence processing engine.
    
    Handles:
    1. Simple commands (Go!, Stop!, Run!)
    2. Polite requests (Please come here.)
    3. Negative imperatives (Don't go!, Don't do that!)
    4. Imperative with explicit subject (You go first!)
    5. Complex imperatives with objects/complements
    """
    
    def __init__(self):
        """Initialize the imperative engine with Stanza."""
        self.logger = logging.getLogger(__name__)
        
        try:
            # Initialize Stanza pipeline for imperative analysis
            self.nlp = stanza.Pipeline(
                lang='en',
                processors='tokenize,pos,lemma,depparse',
                download_method=None,
                verbose=False
            )
            self.logger.info("✅ Imperative Engine: Stanza pipeline initialized")
        except Exception as e:
            self.logger.error(f"❌ Imperative Engine: Stanza initialization failed: {e}")
            self.nlp = None
        
        # Imperative indicators
        self.imperative_patterns = {
            'polite_markers': ['please', 'kindly'],
            'negative_markers': ["don't", "do not", "never", "stop"],
            'command_verbs': ['go', 'come', 'run', 'stop', 'wait', 'help', 'look', 'listen', 'sit', 'stand'],
            'action_verbs': ['take', 'give', 'bring', 'put', 'open', 'close', 'turn', 'move', 'call', 'tell']
        }
    
    def process(self, sentence: str, debug: bool = False) -> ImperativeResult:
        """
        Process sentence for imperative patterns.
        
        Args:
            sentence: Input sentence
            debug: Enable debug logging
            
        Returns:
            ImperativeResult with slot analysis
        """
        start_time = time.time()
        
        try:
            # Clean sentence
            clean_sentence = sentence.strip()
            
            # Quick pattern check
            if not self._is_imperative_candidate(clean_sentence):
                return ImperativeResult(
                    slots={},
                    confidence=0.0,
                    metadata={'reason': 'Not imperative pattern'},
                    success=False,
                    processing_time=time.time() - start_time
                )
            
            # Stanza analysis
            if self.nlp is None:
                return self._fallback_analysis(clean_sentence, start_time)
            
            doc = self.nlp(clean_sentence)
            
            # Analyze imperative structure
            slots = self._analyze_imperative_structure(doc, clean_sentence, debug)
            
            # Calculate confidence
            confidence = self._calculate_confidence(slots, clean_sentence)
            
            # Generate metadata
            metadata = self._generate_metadata(doc, slots, clean_sentence)
            
            processing_time = time.time() - start_time
            
            return ImperativeResult(
                slots=slots,
                confidence=confidence,
                metadata=metadata,
                success=bool(slots and confidence > 0.3),
                processing_time=processing_time
            )
            
        except Exception as e:
            self.logger.error(f"Imperative engine error: {str(e)}")
            return ImperativeResult(
                slots={},
                confidence=0.0,
                metadata={'error': str(e)},
                success=False,
                processing_time=time.time() - start_time,
                error=str(e)
            )
    
    def _is_imperative_candidate(self, sentence: str) -> bool:
        """Quick check if sentence might be imperative."""
        sentence_lower = sentence.lower()
        
        # Exclude obvious non-imperatives first
        if any(sentence_lower.startswith(exclude) for exclude in ['i ', 'you are', 'he ', 'she ', 'they ', 'we are']):
            return False
        
        # Exclude questions (but not rhetorical commands)
        if sentence.startswith(('Are ', 'Is ', 'Do ', 'Does ', 'Did ', 'Can ', 'Will ', 'Would ')):
            return False
        
        # Check for imperative indicators
        patterns = [
            # Exclamation marks (strong indicator)
            sentence.endswith('!'),
            
            # Starts with verb (common imperative pattern)
            any(sentence_lower.startswith(verb) for verb in self.imperative_patterns['command_verbs']),
            
            # Contains polite markers
            any(marker in sentence_lower for marker in self.imperative_patterns['polite_markers']),
            
            # Negative imperatives
            any(sentence_lower.startswith(neg) for neg in self.imperative_patterns['negative_markers']),
            
            # Short commands (high probability)
            len(sentence.split()) <= 3 and not sentence_lower.startswith(('i ', 'you ', 'he ', 'she ', 'they ', 'we ')),
            
            # Common imperative verbs
            any(sentence_lower.startswith(verb) for verb in self.imperative_patterns['action_verbs']),
        ]
        
        return any(patterns)
    
    def _analyze_imperative_structure(self, doc, sentence: str, debug: bool) -> Dict[str, str]:
        """Analyze the imperative sentence structure using Stanza."""
        slots = {}
        
        try:
            # Find root verb (imperative verb)
            root_verb = None
            for sent in doc.sentences:
                for word in sent.words:
                    if word.deprel == 'root' and word.upos in ['VERB', 'AUX']:
                        root_verb = word
                        break
            
            if not root_verb:
                return self._fallback_slot_analysis(sentence)
            
            # Imperative verb goes to V slot
            slots['V'] = root_verb.text
            
            # Analyze sentence structure
            sent = doc.sentences[0]
            
            # Check for polite markers (M1 slot)
            sentence_lower = sentence.lower()
            for marker in self.imperative_patterns['polite_markers']:
                if marker in sentence_lower:
                    slots['M1'] = marker.capitalize()
                    break
            
            # Check for negative markers (Aux slot)
            for neg_marker in self.imperative_patterns['negative_markers']:
                if sentence_lower.startswith(neg_marker):
                    slots['Aux'] = neg_marker
                    break
            
            # Check for explicit subject (rare in imperatives, but possible)
            for word in sent.words:
                if word.deprel == 'nsubj' and word.upos == 'PRON':
                    slots['S'] = word.text
                    break
            
            # Find direct object (O1)
            for word in sent.words:
                if word.deprel == 'obj' or word.deprel == 'dobj':
                    # Get full object phrase
                    obj_phrase = self._extract_phrase(sent, word)
                    slots['O1'] = obj_phrase
                    break
            
            # Find indirect object (O2)
            for word in sent.words:
                if word.deprel == 'iobj':
                    obj_phrase = self._extract_phrase(sent, word)
                    slots['O2'] = obj_phrase
                    break
            
            # Find complement (C1)
            for word in sent.words:
                if word.deprel in ['xcomp', 'ccomp', 'acomp']:
                    comp_phrase = self._extract_phrase(sent, word)
                    slots['C1'] = comp_phrase
                    break
            
            # Find adverbial modifiers (M2, M3)
            adv_mods = []
            for word in sent.words:
                if word.deprel in ['advmod', 'npmod'] and word.head == root_verb.id:
                    adv_mods.append(word.text)
            
            if adv_mods:
                if len(adv_mods) >= 1:
                    slots['M2'] = adv_mods[0]
                if len(adv_mods) >= 2:
                    slots['M3'] = adv_mods[1]
            
            # Find prepositional phrases (C2)
            prep_phrases = []
            for word in sent.words:
                if word.upos == 'ADP':  # Preposition
                    # Find the noun it modifies
                    for target in sent.words:
                        if target.head == word.id and target.upos in ['NOUN', 'PRON']:
                            prep_phrase = f"{word.text} {target.text}"
                            # Add any adjectives or determiners
                            modifiers = []
                            for mod in sent.words:
                                if mod.head == target.id and mod.upos in ['ADJ', 'DET', 'NUM']:
                                    modifiers.append(mod.text)
                            if modifiers:
                                prep_phrase = f"{word.text} {' '.join(modifiers)} {target.text}"
                            prep_phrases.append(prep_phrase)
                            break
            
            if prep_phrases and 'C2' not in slots:
                slots['C2'] = prep_phrases[0]
            
            if debug:
                self.logger.info(f"Imperative analysis: {slots}")
            
            return slots
            
        except Exception as e:
            self.logger.error(f"Structure analysis error: {e}")
            return self._fallback_slot_analysis(sentence)
    
    def _extract_phrase(self, sent, head_word) -> str:
        """Extract complete phrase including dependents."""
        phrase_words = [head_word]
        
        # Find all dependents
        for word in sent.words:
            if word.head == head_word.id:
                phrase_words.append(word)
        
        # Sort by word position
        phrase_words.sort(key=lambda w: w.id)
        
        return ' '.join(word.text for word in phrase_words)
    
    def _fallback_slot_analysis(self, sentence: str) -> Dict[str, str]:
        """Fallback analysis without Stanza."""
        slots = {}
        words = sentence.strip().split()
        
        if not words:
            return slots
        
        sentence_lower = sentence.lower()
        
        # Check for polite markers
        for marker in self.imperative_patterns['polite_markers']:
            if marker in sentence_lower:
                slots['M1'] = marker.capitalize()
                break
        
        # Check for negative markers
        for neg_marker in self.imperative_patterns['negative_markers']:
            if sentence_lower.startswith(neg_marker):
                slots['Aux'] = neg_marker
                # Find verb after negative
                neg_words = neg_marker.split()
                if len(words) > len(neg_words):
                    slots['V'] = words[len(neg_words)]
                return slots
        
        # Simple pattern: first word is usually the verb
        if words[0].lower() not in self.imperative_patterns['polite_markers']:
            slots['V'] = words[0].rstrip('!.,?')
        
        # If starts with "please", second word is verb
        if words[0].lower() == 'please' and len(words) > 1:
            slots['V'] = words[1].rstrip('!.,?')
        
        # Simple object detection (remaining words after verb)
        verb_pos = 0
        if 'M1' in slots:  # Skip polite marker
            verb_pos = 1
        if 'Aux' in slots:  # Skip auxiliary
            verb_pos += len(slots['Aux'].split())
        
        if len(words) > verb_pos + 1:
            remaining = ' '.join(words[verb_pos + 1:]).rstrip('!.,?')
            if remaining:
                slots['O1'] = remaining
        
        return slots
    
    def _calculate_confidence(self, slots: Dict[str, str], sentence: str) -> float:
        """Calculate confidence score for imperative classification."""
        if not slots:
            return 0.0
        
        confidence = 0.0
        sentence_lower = sentence.lower()
        
        # Base confidence for having a verb
        if 'V' in slots:
            confidence += 0.4
        
        # Boost for imperative indicators
        if sentence.endswith('!'):
            confidence += 0.3
        
        # Boost for polite markers
        if any(marker in sentence_lower for marker in self.imperative_patterns['polite_markers']):
            confidence += 0.2
        
        # Boost for negative imperatives
        if any(sentence_lower.startswith(neg) for neg in self.imperative_patterns['negative_markers']):
            confidence += 0.2
        
        # Boost for known command verbs
        verb = slots.get('V', '').lower()
        if verb in self.imperative_patterns['command_verbs'] + self.imperative_patterns['action_verbs']:
            confidence += 0.3
        
        # Penalty for long sentences (less likely to be imperative)
        word_count = len(sentence.split())
        if word_count > 10:
            confidence -= 0.1
        elif word_count <= 3:
            confidence += 0.1
        
        # Penalty for first-person indicators (unlikely in imperatives)
        if sentence_lower.startswith(('i ', 'we ')):
            confidence -= 0.4
        
        # Penalty for question words (likely questions, not imperatives)
        if any(sentence_lower.startswith(qw) for qw in ['what', 'where', 'when', 'who', 'how', 'why']):
            confidence -= 0.3
        
        return min(1.0, max(0.0, confidence))
    
    def _generate_metadata(self, doc, slots: Dict[str, str], sentence: str) -> Dict[str, Any]:
        """Generate metadata for the analysis."""
        metadata = {
            'engine': 'imperative',
            'priority': 15,
            'pattern_type': 'imperative_sentence',
            'sentence_length': len(sentence.split()),
            'slots_filled': len(slots),
            'has_exclamation': sentence.endswith('!'),
            'has_polite_marker': any(marker in sentence.lower() for marker in self.imperative_patterns['polite_markers']),
            'is_negative': any(sentence.lower().startswith(neg) for neg in self.imperative_patterns['negative_markers'])
        }
        
        if doc and doc.sentences:
            sent = doc.sentences[0]
            metadata.update({
                'pos_tags': [word.upos for word in sent.words],
                'dependencies': [(word.text, word.deprel, word.head) for word in sent.words]
            })
        
        return metadata
    
    def _fallback_analysis(self, sentence: str, start_time: float) -> ImperativeResult:
        """Fallback analysis when Stanza is unavailable."""
        slots = self._fallback_slot_analysis(sentence)
        confidence = self._calculate_confidence(slots, sentence)
        
        return ImperativeResult(
            slots=slots,
            confidence=confidence,
            metadata={
                'engine': 'imperative',
                'fallback_mode': True,
                'reason': 'Stanza unavailable'
            },
            success=bool(slots and confidence > 0.3),
            processing_time=time.time() - start_time
        )
    
    def get_engine_info(self) -> Dict[str, Any]:
        """Return engine information."""
        return {
            'name': 'ImperativeEngine',
            'priority': 15,
            'description': 'Imperative sentence processing',
            'patterns': ['Go!', 'Stop!', 'Please come here!', "Don't run!", 'You sit down!'],
            'coverage': '25% frequency → +7% coverage rate',
            'slots_supported': ['M1', 'S', 'Aux', 'V', 'O1', 'O2', 'C1', 'C2', 'M2', 'M3']
        }
