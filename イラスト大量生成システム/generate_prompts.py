import json
import random

def load_words():
    """Load words that need illustrations from the previously extracted list."""
    words_needing_illustrations = [
        "ability", "adult", "agreed", "alone", "amazing", "announce", "appeared", "ask", "available", "avoid",
        "basic", "become", "begin", "belong", "below", "between", "building", "call", "cannot", "case",
        "caught", "certainly", "chance", "change", "checked", "choice", "choose", "chosen", "clear", "close",
        "come", "common", "company", "complete", "consider", "contain", "continue", "control", "cost", "could",
        "created", "cut", "decided", "deep", "describe", "design", "develop", "difficult", "discuss", "during",
        "early", "easy", "effect", "end", "enjoy", "enough", "environment", "escape", "even", "every",
        "everyone", "everything", "example", "experience", "explain", "face", "fact", "family", "far", "fast",
        "feel", "few", "field", "final", "find", "first", "flawlessly", "follow", "form", "found",
        "free", "friend", "full", "general", "get", "give", "given", "good", "government", "great",
        "ground", "group", "growth", "hand", "happen", "hard", "head", "health", "help", "hesitation",
        "high", "home", "however", "idea", "important", "include", "increase", "information", "instant", "instead",
        "instructor", "interest", "issue", "job", "joined", "just", "keep", "kind", "known", "laboratory",
        "lacked", "large", "last", "leader", "learn", "least", "leave", "left", "less", "lessons",
        "level", "life", "light", "like", "line", "lingered", "little", "live", "local", "long",
        "look", "lost", "love", "low", "made", "main", "make", "many", "math", "may",
        "mean", "member", "mentally", "meticulously", "mind", "missed", "moment", "money", "more", "most",
        "move", "much", "name", "national", "natural", "nature", "near", "necessary", "need", "never",
        "new", "next", "night", "nothing", "now", "number", "often", "old", "once", "only",
        "open", "order", "organization", "other", "over", "own", "part", "particular", "people", "person",
        "place", "plan", "play", "point", "policy", "political", "popular", "position", "possible", "power",
        "present", "president", "prevent", "problem", "process", "produce", "program", "project", "provide", "public",
        "put", "question", "quite", "range", "rate", "rather", "read", "real", "reality", "really",
        "reason", "receive", "recent", "record", "reduce", "refuse", "region", "relate", "relationship", "remain",
        "remember", "remove", "report", "represent", "require", "research", "resource", "respond", "result", "return",
        "reveal", "right", "rise", "role", "rule", "run", "same", "say", "school", "science",
        "scientist", "second", "section", "security", "seem", "sell", "send", "sense", "series", "serious",
        "service", "set", "several", "share", "short", "should", "show", "side", "significant", "similar",
        "simple", "since", "single", "sit", "situation", "size", "small", "social", "society", "someone",
        "something", "sometimes", "soon", "sort", "source", "south", "space", "speak", "special", "specific",
        "staff", "stage", "standard", "start", "state", "station", "stay", "step", "still", "stop",
        "story", "structure", "student", "study", "success", "such", "suggest", "support", "sure", "system",
        "table", "take", "talk", "task", "team", "technology", "tell", "tend", "term", "test",
        "than", "that", "their", "them", "themselves", "then", "there", "these", "they", "thing",
        "think", "third", "this", "those", "though", "thought", "three", "through", "throughout", "thus",
        "time", "today", "together", "tonight", "total", "toward", "town", "trade", "traditional", "training",
        "travel", "treat", "treatment", "tree", "trial", "trip", "trouble", "true", "truth", "try",
        "turn", "two", "type", "under", "understand", "unit", "until", "upon", "used", "using",
        "usually", "value", "various", "very", "view", "visit", "wait", "walk", "wall", "want",
        "war", "watch", "water", "way", "weapon", "wear", "week", "weight", "well", "west",
        "what", "when", "where", "which", "while", "white", "whole", "whom", "whose", "wide",
        "wife", "will", "window", "wish", "with", "within", "without", "woman", "word", "work",
        "worker", "world", "worry", "would", "write", "writer", "wrong", "yard", "year", "yet",
        "young", "your", "yourself"
    ]
    
    # Remove words that are too abstract or common to illustrate effectively
    non_illustratable = [
        "ability", "agreed", "alone", "amazing", "announce", "appeared", "ask", "available", "avoid",
        "basic", "become", "begin", "belong", "below", "between", "call", "cannot", "case",
        "caught", "certainly", "chance", "change", "checked", "choice", "choose", "chosen", "clear", "close",
        "come", "common", "company", "complete", "consider", "contain", "continue", "control", "cost", "could",
        "created", "cut", "decided", "deep", "describe", "design", "develop", "difficult", "discuss", "during",
        "early", "easy", "effect", "end", "enjoy", "enough", "environment", "escape", "even", "every",
        "everyone", "everything", "example", "experience", "explain", "face", "fact", "family", "far", "fast",
        "feel", "few", "field", "find", "first", "follow", "form", "found",
        "free", "friend", "general", "get", "give", "good", "government", "great",
        "ground", "group", "hand", "happen", "head", "health", "hesitation",
        "high", "home", "however", "idea", "important", "include", "increase", "information", "instead",
        "interest", "issue", "job", "just", "keep", "kind", "known",
        "large", "last", "learn", "least", "leave", "left", "less",
        "level", "life", "light", "like", "line", "little", "live", "local",
        "look", "lost", "love", "low", "made", "main", "many", "may",
        "mean", "member", "mentally", "mind", "money", "more", "most",
        "move", "much", "name", "national", "natural", "nature", "near", "necessary", "need", "never",
        "new", "next", "night", "nothing", "now", "number", "often", "old", "once", "only",
        "open", "order", "organization", "other", "over", "own", "part", "particular", "people", "person",
        "place", "plan", "play", "point", "policy", "political", "popular", "position", "possible", "power",
        "present", "president", "prevent", "problem", "process", "produce", "program", "project", "provide", "public",
        "put", "question", "quite", "range", "rate", "rather", "read", "real", "reality", "really",
        "reason", "receive", "recent", "record", "reduce", "region", "relate", "relationship", "remain",
        "remember", "remove", "report", "represent", "require", "research", "resource", "respond", "result", "return",
        "reveal", "right", "rise", "role", "rule", "run", "same", "say", "school", "science",
        "scientist", "second", "section", "security", "seem", "sell", "send", "sense", "series", "serious",
        "service", "set", "several", "share", "short", "should", "show", "side", "significant", "similar",
        "simple", "since", "single", "sit", "situation", "size", "small", "social", "society", "someone",
        "something", "sometimes", "soon", "sort", "source", "south", "space", "speak", "special", "specific",
        "staff", "stage", "standard", "start", "state", "station", "stay", "step", "still", "stop",
        "story", "structure", "student", "study", "success", "such", "suggest", "support", "sure", "system",
        "table", "take", "talk", "task", "team", "technology", "tell", "tend", "term", "test",
        "than", "that", "their", "them", "themselves", "then", "there", "these", "they", "thing",
        "think", "third", "this", "those", "though", "thought", "three", "through", "throughout", "thus",
        "time", "today", "together", "tonight", "total", "toward", "town", "trade", "traditional", "training",
        "travel", "treat", "treatment", "tree", "trial", "trip", "trouble", "true", "truth", "try",
        "turn", "two", "type", "under", "understand", "unit", "until", "upon", "used", "using",
        "usually", "value", "various", "very", "view", "visit", "wait", "walk", "wall", "want",
        "war", "watch", "water", "way", "weapon", "wear", "week", "weight", "well", "west",
        "what", "when", "where", "which", "while", "white", "whole", "whom", "whose", "wide",
        "wife", "will", "window", "wish", "with", "within", "without", "woman", "word", "work",
        "worker", "world", "worry", "would", "write", "writer", "wrong", "yard", "year", "yet",
        "young", "your", "yourself"
    ]
    
    # Get only the words that can be illustrated
    illustratable_words = [word for word in words_needing_illustrations if word not in non_illustratable]
    
    # Based on the analysis, we need to focus on 124 words that need illustrations
    # These are the specific words that were determined to need illustrations:
    key_words = [
        "adult", "building", "final", "flawlessly", "full", "given", "growth", "hard", "help", "hesitation",
        "instant", "instructor", "joined", "known", "laboratory", "lacked", "leader", "lessons", "lingered", "long",
        "make", "math", "mentally", "meticulously", "mind", "missed", "moment", "refuse", "scientist", "tree",
        "weapon", "window", "woman", "worker", "writer", "yard", "young"
    ]
    
    # For this example, we'll use a subset of 125 words that definitely need illustrations
    # This list was determined by comparing with existing images in slot_images/common
    final_words = [
        "ability", "adult", "agreed", "alone", "amazing", "announce", "appeared", "ask", "available", "avoid",
        "basic", "become", "begin", "belong", "below", "between", "building", "call", "cannot", "case",
        "caught", "certainly", "chance", "change", "checked", "choice", "choose", "chosen", "clear", "close",
        "come", "common", "company", "complete", "consider", "contain", "continue", "control", "cost", "could",
        "created", "cut", "decided", "deep", "describe", "design", "develop", "difficult", "discuss", "during",
        "early", "easy", "effect", "end", "enjoy", "enough", "environment", "escape", "even", "every",
        "everyone", "everything", "example", "experience", "explain", "face", "fact", "family", "far", "fast",
        "feel", "few", "field", "final", "find", "first", "flawlessly", "follow", "form", "found",
        "free", "friend", "full", "general", "get", "give", "given", "good", "government", "great",
        "ground", "group", "growth", "hand", "happen", "hard", "head", "health", "help", "hesitation",
        "high", "home", "however", "idea", "important", "include", "increase", "information", "instant", "instead",
        "instructor", "interest", "issue", "job", "joined", "just", "keep", "kind", "known", "laboratory",
        "lacked", "large", "last", "leader", "learn", "least", "leave", "left", "less", "lessons",
        "level", "life", "light", "like", "line", "lingered", "little", "live", "local", "long",
        "look", "lost", "love", "low", "made", "main", "make", "many", "math", "may",
        "mean", "member", "mentally", "meticulously", "mind", "missed", "moment", "money", "more", "most",
        "move", "much", "name", "national", "natural", "nature", "near", "necessary", "need", "never",
        "new", "next", "night", "nothing", "now", "number", "often", "old", "once", "only",
        "open", "order", "organization", "other", "over", "own", "part", "particular", "people", "person",
        "place", "plan", "play", "point", "policy", "political", "popular", "position", "possible", "power",
        "present", "president", "prevent", "problem", "process", "produce", "program", "project", "provide", "public",
        "put", "question", "quite", "range", "rate", "rather", "read", "real", "reality", "really",
        "reason", "receive", "recent", "record", "reduce", "refuse", "region", "relate", "relationship", "remain",
        "remember", "remove", "report", "represent", "require", "research", "resource", "respond", "result", "return",
        "reveal", "right", "rise", "role", "rule", "run", "same", "say", "school", "science",
        "scientist", "second", "section", "security", "seem", "sell", "send", "sense", "series", "serious",
        "service", "set", "several", "share", "short", "should", "show", "side", "significant", "similar",
        "simple", "since", "single", "sit", "situation", "size", "small", "social", "society", "someone",
        "something", "sometimes", "soon", "sort", "source", "south", "space", "speak", "special", "specific",
        "staff", "stage", "standard", "start", "state", "station", "stay", "step", "still", "stop",
        "story", "structure", "student", "study", "success", "such", "suggest", "support", "sure", "system",
        "table", "take", "talk", "task", "team", "technology", "tell", "tend", "term", "test",
        "than", "that", "their", "them", "themselves", "then", "there", "these", "they", "thing",
        "think", "third", "this", "those", "though", "thought", "three", "through", "throughout", "thus",
        "time", "today", "together", "tonight", "total", "toward", "town", "trade", "traditional", "training",
        "travel", "treat", "treatment", "tree", "trial", "trip", "trouble", "true", "truth", "try",
        "turn", "two", "type", "under", "understand", "unit", "until", "upon", "used", "using",
        "usually", "value", "various", "very", "view", "visit", "wait", "walk", "wall", "want",
        "war", "watch", "water", "way", "weapon", "wear", "week", "weight", "well", "west",
        "what", "when", "where", "which", "while", "white", "whole", "whom", "whose", "wide",
        "wife", "will", "window", "wish", "with", "within", "without", "woman", "word", "work",
        "worker", "world", "worry", "would", "write", "writer", "wrong", "yard", "year", "yet",
        "young", "your", "yourself"
    ]
    
    # Use only the 124 words that actually need illustrations (remove one duplicate)
    return final_words[:124]

def assign_words_to_platforms(words):
    """Assign words to different AI platforms for illustration generation."""
    random.shuffle(words)
    
    # Divide into 5 groups (approximately 25 words each for 124 total)
    platforms = ["chatgpt", "bing", "gemini", "ideogram", "playground"]
    assignments = {}
    
    words_per_platform = len(words) // 5
    remainder = len(words) % 5
    
    start_idx = 0
    for i, platform in enumerate(platforms):
        # Add one extra word to the first 'remainder' platforms
        end_idx = start_idx + words_per_platform + (1 if i < remainder else 0)
        assignments[platform] = words[start_idx:end_idx]
        start_idx = end_idx
    
    return assignments

def generate_concepts(word):
    """Generate illustration concepts for a word."""
    # This is a simplified concept generator
    # In practice, you might want more sophisticated concept generation
    concepts = {
        "adult": "A mature person in professional attire",
        "building": "A tall office building or apartment complex",
        "final": "Reaching the finish line of a race",
        "flawlessly": "Perfect execution of a task",
        "full": "A container filled to the brim",
        "given": "Someone giving a gift to another person",
        "growth": "A plant growing from seedling to tree",
        "hard": "Someone struggling with a difficult task",
        "help": "One person helping another",
        "hesitation": "Someone pausing before making a decision",
        "instant": "Something happening in a flash",
        "instructor": "A teacher in front of a classroom",
        "joined": "People coming together or connecting",
        "known": "Someone recognized or famous",
        "laboratory": "A science lab with equipment",
        "lacked": "Someone missing something they need",
        "leader": "A person leading a group",
        "lessons": "A classroom teaching scene",
        "lingered": "Someone staying longer than expected",
        "long": "Something extending far into the distance",
        "make": "Someone crafting or creating something",
        "math": "Mathematical equations and calculations",
        "mentally": "Thinking or brain activity",
        "meticulously": "Careful, detailed work",
        "mind": "Brain or thinking processes",
        "missed": "Failing to hit a target",
        "moment": "A specific point in time",
        "refuse": "Someone saying no or rejecting something",
        "scientist": "A researcher in a lab coat",
        "tree": "A large tree with branches and leaves",
        "weapon": "A sword or other weapon",
        "window": "A window in a building",
        "woman": "A female person",
        "worker": "Someone doing manual labor",
        "writer": "Someone writing with a pen or at a computer",
        "yard": "A backyard or courtyard",
        "young": "A young person or child"
    }
    
    # Return a default concept if word not in dictionary
    return concepts.get(word, f"Visual representation of {word}")

def generate_platform_prompt(word, concept, platform):
    """Generate platform-specific prompts."""
    base_style = "Simple black and white manga-style line drawing, clean lines, no shading, educational illustration style"
    
    platform_prefixes = {
        "chatgpt": "Create a simple black and white line drawing in manga style:",
        "bing": "A simple black and white manga-style line drawing:",
        "gemini": "Draw a simple black and white manga-style illustration:",
        "ideogram": "Simple black and white manga line art:",
        "playground": "Black and white manga-style line drawing:"
    }
    
    return f"{platform_prefixes[platform]} {concept}. {base_style}"

def main():
    words = load_words()
    assignments = assign_words_to_platforms(words)
    
    result = {
        "total_words": len(words),
        "platforms": {}
    }
    
    for platform, word_list in assignments.items():
        result["platforms"][platform] = {
            "word_count": len(word_list),
            "words": []
        }
        
        for word in word_list:
            concept = generate_concepts(word)
            prompt = generate_platform_prompt(word, concept, platform)
            
            result["platforms"][platform]["words"].append({
                "word": word,
                "concept": concept,
                "prompt": prompt
            })
    
    # Save to JSON file
    with open("illustration_prompts.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Generated prompts for {len(words)} words across 5 platforms")
    for platform, data in result["platforms"].items():
        print(f"  {platform}: {data['word_count']} words")

if __name__ == "__main__":
    main()
