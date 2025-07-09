// 画像メタタグ自動生成スクリプト
// 既存の画像ファイルに対してメタタグ定義を自動生成します

// 既存の画像ファイル一覧（slot_images/common/）
const existingImages = [
  "absence.png", "academic.png", "administrator.png", "adult.png", "afraid.png",
  "afternoon.png", "alarm.png", "alone.png", "amaging.png", "analyze.png",
  "appear.png", "ask.png", "available.png", "avoid.png", "become.png",
  "begin.png", "believe.png", "belong.png", "below.png", "book.png",
  "briefing.png", "brother.png", "building.png", "button.png", "capable.png",
  "case.png", "catch up.png", "catch.png", "caught.png", "central.png",
  "certainly.png", "challenge.png", "change.png", "charge.png", "choice.png",
  "chosen.png", "clarity.png", "clear.png", "close.png", "clouded.png",
  "committee.png", "common.png", "company.png", "complete.png", "complex.png",
  "composure.png", "confident.png", "confrontation.png", "consider.png", "content.png",
  "control.png", "counting on.png", "counting.png", "critical.png", "crucial.png",
  "cruelty.png", "data.png", "day.png", "decide.png", "decisive.png",
  "deep.png", "deliver.png", "dependable.png", "detailed.png", "determined.png",
  "difficult.png", "direct.png", "discuss.png", "doubt.png", "early.png",
  "echo.png", "emotionally.png", "employee.png", "encourage.png", "end.png",
  "engineer.png", "enhance.png", "enjoy.png", "enough.png", "environment.png",
  "escape.png", "even.png", "everyone.png", "example.png", "exhausted.png",
  "experiment.png", "explain.png", "explaining.png", "face.png", "far.png",
  "fast.png", "fatigue.png", "feared.png", "feelings.png", "figure out.png",
  "fill.png", "final.png", "find.png", "flawlessly.jpg", "full.png",
  "game.png", "general.png", "get.png", "give.png", "good.png",
  "government.png", "ground.png", "growth.png", "hand.png", "happen.png",
  "hard.png", "he.png", "head.png", "health.png", "help.png",
  "hesitation.png", "high.png", "home.png", "hurting.png", "I.png",
  "idea.png", "implementation.png", "include.png", "increase.png", "indecisive.png",
  "instant.png", "instead.png", "instructor.jpg", "intend.png", "intense.png",
  "issue.png", "job.png", "joined.png", "just.png", "keep.png",
  "kind.png", "know.png", "laboratory.png", "lacked.png", "last.png",
  "leader.png", "lesson.png", "like.png", "lingered.png", "long.png",
  "make.png", "manager.png", "math.png", "meeting.png", "mentally.png",
  "meticulously.png", "mind.png", "missed.png", "moment.png", "morning.png",
  "near.png", "new.png", "nonbody.png", "notice.png", "occured.png",
  "offer.png", "office.png", "once.png", "outage.png", "outcome.png",
  "outline.png", "party.png", "people.png", "placeholder.png", "plan.png",
  "point.png", "policy.png", "potential.png", "power.png", "prepared.png",
  "presentation.png", "pressure.png", "previous.png", "principal.png", "project.png",
  "proposal.png", "publication.png", "push.png", "question.png", "recently.png",
  "reflect.png", "refuse.png", "remarkable.png", "reputation.png", "request.png",
  "research.png", "respond.png", "responsible.png", "return.png", "room.png",
  "school.png", "scientist.png", "second.png", "seemed.png", "severe.png",
  "she.png", "shown.png", "silence.png", "spoke.png", "staff.png",
  "student.png", "suggestion.png", "summary.png", "take.png", "teacher.png",
  "team.png", "they.png", "think.png", "thoughtful.png", "thoughts.png",
  "transferred.png", "trying.png", "uncertainty.png", "unexpected.png", "upsetting.png",
  "urgent.png", "voice.png", "waiting.png", "want.png", "we.png",
  "week.png", "wish.png", "without.png", "woman.png", "working.png",
  "would_rather.png"
];

// 単語から語幹バリエーションを生成
function generateWordVariations(baseWord) {
  const variations = [baseWord];
  
  // 動詞の活用形を追加
  if (baseWord.endsWith('e')) {
    variations.push(baseWord + 'd'); // -ed形
    variations.push(baseWord.slice(0, -1) + 'ing'); // -ing形
  } else {
    variations.push(baseWord + 'ed'); // -ed形
    variations.push(baseWord + 'ing'); // -ing形
  }
  
  // 3人称単数形を追加
  if (baseWord.endsWith('y')) {
    variations.push(baseWord.slice(0, -1) + 'ies');
  } else if (baseWord.endsWith('s') || baseWord.endsWith('sh') || baseWord.endsWith('ch') || baseWord.endsWith('x') || baseWord.endsWith('z')) {
    variations.push(baseWord + 'es');
  } else {
    variations.push(baseWord + 's');
  }
  
  // 名詞の複数形を追加
  if (baseWord.endsWith('y')) {
    variations.push(baseWord.slice(0, -1) + 'ies');
  } else if (baseWord.endsWith('s') || baseWord.endsWith('sh') || baseWord.endsWith('ch') || baseWord.endsWith('x') || baseWord.endsWith('z')) {
    variations.push(baseWord + 'es');
  } else {
    variations.push(baseWord + 's');
  }
  
  // 形容詞の比較級・最上級
  if (baseWord.length <= 6) {
    variations.push(baseWord + 'er');
    variations.push(baseWord + 'est');
  }
  
  // 重複を除去
  return [...new Set(variations)];
}

// 特別なメタタグマッピング（手動定義が必要なもの）
const specialMappings = {
  "catch up.png": {
    meta_tags: ["catch up", "catching up", "caught up", "catches up"],
    description: "追いつく"
  },
  "figure out.png": {
    meta_tags: ["figure out", "figures out", "figured out", "figuring out"],
    description: "理解する、解決する"
  },
  "counting on.png": {
    meta_tags: ["counting on", "count on", "counts on", "counted on"],
    description: "頼りにする"
  },
  "would_rather.png": {
    meta_tags: ["would rather", "would rather", "prefer", "prefers", "preferred"],
    description: "むしろ〜したい"
  },
  "I.png": {
    meta_tags: ["I", "me", "my", "mine", "myself"],
    description: "私"
  },
  "he.png": {
    meta_tags: ["he", "him", "his", "himself"],
    description: "彼"
  },
  "she.png": {
    meta_tags: ["she", "her", "hers", "herself"],
    description: "彼女"
  },
  "we.png": {
    meta_tags: ["we", "us", "our", "ours", "ourselves"],
    description: "私たち"
  },
  "they.png": {
    meta_tags: ["they", "them", "their", "theirs", "themselves"],
    description: "彼ら、彼女ら"
  }
};

// 単語に基づいて説明を生成（簡易版）
function generateDescription(baseWord) {
  const descriptions = {
    // 動詞
    "analyze": "分析する",
    "appear": "現れる",
    "ask": "尋ねる",
    "avoid": "避ける",
    "become": "〜になる",
    "begin": "始める",
    "believe": "信じる",
    "belong": "所属する",
    "catch": "捕まえる",
    "change": "変える",
    "choose": "選ぶ",
    "complete": "完了する",
    "consider": "考慮する",
    "control": "制御する",
    "decide": "決める",
    "deliver": "配達する",
    "discuss": "議論する",
    "encourage": "励ます",
    "enhance": "向上させる",
    "enjoy": "楽しむ",
    "escape": "逃げる",
    "explain": "説明する",
    "face": "直面する",
    "find": "見つける",
    "give": "与える",
    "happen": "起こる",
    "help": "助ける",
    "include": "含む",
    "increase": "増加する",
    "intend": "意図する",
    "keep": "保つ",
    "know": "知る",
    "like": "好む",
    "make": "作る",
    "notice": "気づく",
    "offer": "提供する",
    "prepare": "準備する",
    "push": "押す",
    "reflect": "反映する",
    "refuse": "拒否する",
    "request": "要求する",
    "respond": "応答する",
    "return": "戻る",
    "take": "取る",
    "think": "考える",
    "transfer": "移す",
    "want": "欲しい",
    "wish": "願う",
    "work": "働く",
    
    // 名詞
    "absence": "不在",
    "administrator": "管理者",
    "adult": "大人",
    "afternoon": "午後",
    "alarm": "警報",
    "book": "本",
    "briefing": "説明会",
    "brother": "兄弟",
    "building": "建物",
    "button": "ボタン",
    "case": "場合",
    "choice": "選択",
    "clarity": "明確さ",
    "committee": "委員会",
    "company": "会社",
    "composure": "冷静さ",
    "confrontation": "対立",
    "content": "内容",
    "cruelty": "残酷さ",
    "data": "データ",
    "day": "日",
    "employee": "従業員",
    "end": "終わり",
    "engineer": "エンジニア",
    "environment": "環境",
    "everyone": "みんな",
    "example": "例",
    "experiment": "実験",
    "fatigue": "疲労",
    "feelings": "感情",
    "game": "ゲーム",
    "government": "政府",
    "ground": "地面",
    "growth": "成長",
    "hand": "手",
    "head": "頭",
    "health": "健康",
    "hesitation": "躊躇",
    "home": "家",
    "idea": "アイデア",
    "implementation": "実装",
    "instant": "瞬間",
    "instructor": "指導者",
    "issue": "問題",
    "job": "仕事",
    "laboratory": "研究室",
    "leader": "リーダー",
    "lesson": "授業",
    "manager": "管理者",
    "math": "数学",
    "meeting": "会議",
    "mind": "心",
    "moment": "瞬間",
    "morning": "朝",
    "office": "オフィス",
    "outage": "停電",
    "outcome": "結果",
    "outline": "概要",
    "party": "パーティー",
    "people": "人々",
    "plan": "計画",
    "point": "点",
    "policy": "政策",
    "potential": "可能性",
    "power": "力",
    "presentation": "発表",
    "pressure": "圧力",
    "principal": "校長",
    "project": "プロジェクト",
    "proposal": "提案",
    "publication": "出版物",
    "question": "質問",
    "reputation": "評判",
    "research": "研究",
    "room": "部屋",
    "school": "学校",
    "scientist": "科学者",
    "second": "秒",
    "silence": "沈黙",
    "staff": "スタッフ",
    "student": "学生",
    "suggestion": "提案",
    "summary": "要約",
    "teacher": "教師",
    "team": "チーム",
    "thoughts": "考え",
    "uncertainty": "不確実性",
    "voice": "声",
    "week": "週",
    "woman": "女性",
    
    // 形容詞
    "academic": "学術的な",
    "afraid": "恐れた",
    "alone": "一人の",
    "available": "利用可能な",
    "capable": "有能な",
    "central": "中央の",
    "clear": "明確な",
    "clouded": "曇った",
    "common": "共通の",
    "complex": "複雑な",
    "confident": "自信のある",
    "critical": "重要な",
    "crucial": "決定的な",
    "decisive": "決定的な",
    "deep": "深い",
    "dependable": "信頼できる",
    "detailed": "詳細な",
    "determined": "決意した",
    "difficult": "難しい",
    "direct": "直接的な",
    "early": "早い",
    "emotional": "感情的な",
    "enough": "十分な",
    "even": "平らな",
    "exhausted": "疲れ果てた",
    "far": "遠い",
    "fast": "速い",
    "final": "最終的な",
    "full": "満杯の",
    "general": "一般的な",
    "good": "良い",
    "hard": "困難な",
    "high": "高い",
    "indecisive": "優柔不断な",
    "intense": "激しい",
    "just": "公正な",
    "kind": "親切な",
    "last": "最後の",
    "long": "長い",
    "mental": "精神的な",
    "meticulous": "細心な",
    "near": "近い",
    "new": "新しい",
    "previous": "前の",
    "recent": "最近の",
    "remarkable": "注目すべき",
    "responsible": "責任のある",
    "severe": "深刻な",
    "successful": "成功した",
    "thoughtful": "思慮深い",
    "unexpected": "予期しない",
    "upsetting": "動揺させる",
    "urgent": "緊急の",
    
    // 副詞
    "certainly": "確実に",
    "emotionally": "感情的に",
    "flawlessly": "完璧に",
    "instead": "代わりに",
    "mentally": "精神的に",
    "meticulously": "細心に",
    "once": "一度",
    "recently": "最近",
    "without": "〜なしで"
  };
  
  return descriptions[baseWord] || baseWord;
}

// メタタグ定義を自動生成
function generateMetaTags() {
  const metaTags = [];
  
  existingImages.forEach(imageFile => {
    // ファイル名から拡張子を除去して基本単語を取得
    const baseWord = imageFile.replace(/\.(png|jpg|jpeg)$/, '').toLowerCase();
    
    let entry;
    
    // 特別なマッピングがある場合はそれを使用
    if (specialMappings[imageFile]) {
      entry = {
        image_file: imageFile,
        folder: "common",
        meta_tags: specialMappings[imageFile].meta_tags,
        priority: 3,
        description: specialMappings[imageFile].description
      };
    } else {
      // 自動生成
      const variations = generateWordVariations(baseWord);
      entry = {
        image_file: imageFile,
        folder: "common",
        meta_tags: variations,
        priority: 3,
        description: generateDescription(baseWord)
      };
    }
    
    metaTags.push(entry);
  });
  
  return metaTags;
}

// JSON形式で出力
const generatedMetaTags = generateMetaTags();
console.log('Generated meta tags:');
console.log(JSON.stringify(generatedMetaTags, null, 2));

// ファイルに書き出す場合（Node.js環境）
if (typeof require !== 'undefined') {
  const fs = require('fs');
  fs.writeFileSync('image_meta_tags_generated.json', JSON.stringify(generatedMetaTags, null, 2));
  console.log('Generated file: image_meta_tags_generated.json');
}
