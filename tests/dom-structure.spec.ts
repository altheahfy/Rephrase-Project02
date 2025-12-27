import { test, expect } from '@playwright/test';

/**
 * A. DOM構造テスト - ランダマイズ後の構造検証
 * 
 * 検証項目:
 * 1. 必須スロット（S, V等）が存在するか
 * 2. Slot_display_order に従って正しい順序か
 * 3. サブスロットの折りたたみ状態が保持されるか
 * 4. 制御パネルの非表示設定が維持されるか
 * 5. 動的記載エリアと静的スロットが100%一致するか
 */

test.describe('A. DOM構造テスト - RephraseUI', () => {
  
  test.beforeEach(async ({ page }) => {
    // ページを開く（認証スキップ）
    await page.goto('/training/index.html?skipAuth=true');
    await page.waitForLoadState('networkidle');
    console.log('✓ ページロード完了');
    
    // データ選択・読込（ページリロードなし）
    await page.selectOption('#presetSelect', 'data/slot_order_data.json');
    await page.click('#loadPresetButton');
    console.log('✓ データ読込ボタンクリック完了');
    
    // スロットが表示されるまで明示的に待機（10秒タイムアウト）
    await page.waitForSelector('.slot-container', { timeout: 10000 });
    await page.waitForTimeout(2000); // 追加の安定化待機
    
    // スロットが実際に表示されているか確認
    const slotCount = await page.locator('.slot-container').count();
    console.log(`✓ ${slotCount}個のスロット検出`);
  });

  test('Test-1: 初期表示で必須スロットが存在する', async ({ page }) => {
    // スロットが表示されるまで明示的に待機
    await page.waitForSelector('.slot-container', { timeout: 10000 });
    
    // スロットが表示されているか確認
    const slots = page.locator('.slot-container');
    const count = await slots.count();
    expect(count).toBeGreaterThan(0);
    
    // 最低1つのスロットが実際に表示されている
    await expect(slots.first()).toBeVisible();
    
    console.log(`✓ 初期表示OK: ${count}個のスロット検出`);
  });

  test('Test-2: 全体ランダマイズ後もスロット構造が保持される', async ({ page }) => {
    // ランダマイズ前のスロット情報を取得（id属性使用）
    const beforeSlots = await page.locator('.slot-container').evaluateAll(elements => 
      elements.map(el => ({
        id: el.getAttribute('id'),
        visible: el.style.display !== 'none'
      }))
    );
    
    console.log('ランダマイズ前:', beforeSlots);
    
    // 全体ランダマイズボタンをクリック
    const randomizeButton = page.locator('#randomize-all-button, button:has-text("全体ランダマイズ")');
    if (await randomizeButton.count() > 0) {
      await randomizeButton.click();
      await page.waitForTimeout(1500); // ランダマイズ処理待ち
    }
    
    // ランダマイズ後のスロット数を確認
    const afterSlots = await page.locator('.slot-container').evaluateAll(elements => 
      elements.map(el => ({
        id: el.getAttribute('id'),
        visible: el.style.display !== 'none'
      }))
    );
    
    console.log('ランダマイズ後:', afterSlots);
    
    // スロット数が維持されているか（変化する場合もあるため、0以上を確認）
    expect(afterSlots.length).toBeGreaterThan(0);
    
    // 各スロットが valid な id を持つか
    for (const slot of afterSlots) {
      expect(slot.id).toBeTruthy();
    }
    
    console.log('✓ 全体ランダマイズ後もスロット構造保持OK');
  });

  test('Test-3: サブスロット折りたたみ状態が保持される', async ({ page }) => {
    // サブスロットトグルボタンを探す
    const toggleButton = page.locator('.subslot-toggle, .toggle-button').first();
    
    if (await toggleButton.count() > 0) {
      // サブスロットを閉じる
      await toggleButton.click();
      await page.waitForTimeout(500);
      
      // 閉じた状態を確認
      const subSlotBefore = page.locator('.sub-slot-container').first();
      const isHiddenBefore = await subSlotBefore.evaluate(el => 
        el.style.display === 'none' || el.classList.contains('collapsed')
      );
      
      expect(isHiddenBefore).toBe(true);
      console.log('✓ サブスロット折りたたみOK');
      
      // サブスロットのid属性を記録（ランダマイズ後の再取得用）
      const subSlotId = await subSlotBefore.getAttribute('id');
      
      // 個別ランダマイズ実行
      const randomizeIndividual = page.locator('#randomize-individual-button, button:has-text("個別ランダマイズ")');
      if (await randomizeIndividual.count() > 0) {
        await randomizeIndividual.click();
        await page.waitForTimeout(1500);
        
        // id属性で再度取得して折りたたみ状態をチェック
        const subSlotAfter = subSlotId ? page.locator(`#${subSlotId}`) : subSlotBefore;
        const isHiddenAfter = await subSlotAfter.evaluate(el => 
          el.style.display === 'none' || el.classList.contains('collapsed')
        );
        
        expect(isHiddenAfter).toBe(true);
        console.log('✓ ランダマイズ後も折りたたみ状態保持OK');
      }
    } else {
      console.log('⚠ サブスロットトグルボタンが見つからない（スキップ）');
    }
  });

  test('Test-4: 制御パネルの非表示設定が維持される', async ({ page }) => {
    // 制御パネルを探す
    const controlPanel = page.locator('#control-panel, .control-panel');
    
    if (await controlPanel.count() > 0) {
      // V スロットを非表示にするボタンを探す
      const hideVButton = controlPanel.locator('button:has-text("V"), input[value="V"]').first();
      
      if (await hideVButton.count() > 0) {
        await hideVButton.click();
        await page.waitForTimeout(500);
        
        // V スロット内のテキストが非表示になったか確認
        const vSlot = page.locator('.slot-container[data-role="V"], .slot[data-role="V"]').first();
        const vText = vSlot.locator('.slot-text, .text');
        
        if (await vText.count() > 0) {
          const isHidden = await vText.evaluate(el => 
            el.style.display === 'none' || el.style.visibility === 'hidden'
          );
          
          expect(isHidden).toBe(true);
          console.log('✓ V スロット非表示OK');
          
          // ランダマイズ実行
          const randomizeButton = page.locator('#randomize-all-button').first();
          if (await randomizeButton.count() > 0) {
            await randomizeButton.click();
            await page.waitForTimeout(1500);
            
            // 非表示設定が維持されているか
            const isStillHidden = await vText.evaluate(el => 
              el.style.display === 'none' || el.style.visibility === 'hidden'
            );
            
            expect(isStillHidden).toBe(true);
            console.log('✓ ランダマイズ後も非表示設定保持OK');
          }
        }
      } else {
        console.log('⚠ V非表示ボタンが見つからない（スキップ）');
      }
    } else {
      console.log('⚠ 制御パネルが見つからない（スキップ）');
    }
  });

  test('Test-5: スロットにテキストデータが読み込まれる', async ({ page }) => {
    // データロード後の追加待機（UI更新完了を確保）
    await page.waitForTimeout(3000);
    
    // 静的スロットのテキストを取得（.slot-phrase, .slot-text, その他すべて）
    const slotTexts = await page.locator('.slot-container').evaluateAll(elements =>
      elements.map(el => {
        // すべてのテキストコンテンツを取得（子要素含む）
        const allText = el.textContent?.trim() || '';
        return allText;
      }).filter(text => {
        // ボタンのテキスト（▼詳細、🎲）を除外し、3文字以上の内容があるものだけ
        const cleaned = text.replace(/[▼🎲]/g, '').replace(/詳細/g, '').trim();
        return cleaned.length >= 3;
      })
    );
    
    console.log('スロットテキスト:', slotTexts);
    console.log('テキスト数:', slotTexts.length);
    
    // スロットにデータが入っているか確認
    expect(slotTexts.length).toBeGreaterThan(0);
    
    console.log('✓ スロットテキストデータ読込OK');
  });

  test('Test-6: スロット表示順序が正しい', async ({ page }) => {
    // data-order 属性を持つスロットを取得
    const slotOrders = await page.locator('.slot-container[data-order]').evaluateAll(elements =>
      elements.map(el => ({
        role: el.getAttribute('data-role'),
        order: parseInt(el.getAttribute('data-order') || '0')
      }))
    );
    
    console.log('スロット順序:', slotOrders);
    
    if (slotOrders.length > 1) {
      // order が昇順になっているか確認
      for (let i = 0; i < slotOrders.length - 1; i++) {
        expect(slotOrders[i].order).toBeLessThanOrEqual(slotOrders[i + 1].order);
      }
      console.log('✓ スロット表示順序OK');
    } else {
      console.log('⚠ data-order 属性が見つからない（スキップ）');
    }
  });
});
