from allennlp.predictors.predictor import Predictor

# ex007でSemantic Role Labelingをテスト
text = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."

print("=== AllenNLP Semantic Role Labeling テスト ===")
try:
    # SRLモデルロード（初回は時間がかかる可能性）
    predictor = Predictor.from_path(
        "https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz"
    )
    
    # SRL実行
    result = predictor.predict(sentence=text)
    
    print("🎯 動詞と意味役割の自動抽出:")
    
    for i, verb in enumerate(result['verbs']):
        print(f"\n動詞 {i+1}: '{verb['verb']}'")
        print(f"  記述: {verb['description']}")
        
        # 意味役割を分析
        tags = verb['tags']
        words = result['words']
        
        current_arg = None
        current_phrase = []
        
        for word, tag in zip(words, tags):
            if tag.startswith('B-'):  # 新しい引数の開始
                if current_arg and current_phrase:
                    print(f"    {current_arg}: '{' '.join(current_phrase)}'")
                current_arg = tag[2:]
                current_phrase = [word]
            elif tag.startswith('I-') and current_arg:  # 引数の継続
                current_phrase.append(word)
            else:
                if current_arg and current_phrase:
                    print(f"    {current_arg}: '{' '.join(current_phrase)}'")
                current_arg = None
                current_phrase = []
        
        # 最後の引数を出力
        if current_arg and current_phrase:
            print(f"    {current_arg}: '{' '.join(current_phrase)}'")
    
    print("\n" + "="*60)
    print("🎯 5文型との対応分析:")
    print("ARG0 ≈ 主語(S)")
    print("ARG1 ≈ 目的語(O)")  
    print("ARG2 ≈ 間接目的語(O2)")
    print("ARGM-TMP ≈ 時間修飾(M)")
    print("ARGM-LOC ≈ 場所修飾(M)")
    
except Exception as e:
    print(f"❌ AllenNLPエラー: {e}")
    print("💡 インターネット接続が必要、または初回モデルダウンロード中")
