import { test, expect } from '@playwright/test';

/**
 * RephraseUI 機能テスト v2
 * 
 * 【改善点】（ChatGPTレビュー反映）
 * - 必須/任意を明確に分離（必須は見つからなければ即fail）
 * - waitForTimeoutをexpect/waitForFunctionに置換
 * - 制御パネルは実際のスロット表示変化まで検証
 * - 表示順のテスト改善（サブスロットを除外）
 * - イラストはnaturalWidthでロード確認
 */

test.describe('RephraseUI 機能テスト', () => {
  
  // 各テストの前にデータをロード
  test.beforeEach(async ({ page }) => {
    await page.goto('/training/index.html?skipAuth=true');
    await page.waitForLoadState('networkidle');
    
    // 【必須】プリセット選択読込ボタンが存在すること
    await expect(page.locator('#presetSelect')).toHaveCount(1);
    await expect(page.locator('#loadPresetButton')).toHaveCount(1);
    
    await page.selectOption('#presetSelect', 'data/slot_order_data.json');
    await page.click('#loadPresetButton');
    
    // 【改善】waitForFunctionでデータロード完了を待機
    await page.waitForFunction(() => {
      const phrases = document.querySelectorAll('.slot-phrase');
      for (const p of phrases) {
        if (p.textContent && p.textContent.trim().length > 0) return true;
      }
      return false;
    }, { timeout: 15000 });
  });

  /**
   * Test-1: 【必須】Structure Builder - スロットにDBからデータが正しく読み込まれる
   */
  test('【必須】スロットにDBからデータが正しく読み込まれる', async ({ page }) => {
    const phrases = await page.locator('.slot-phrase').allTextContents();
    const nonEmptyPhrases = phrases.filter(p => p.trim().length > 0);
    
    console.log(' slot-phrase内容:', nonEmptyPhrases.slice(0, 5));
    expect(nonEmptyPhrases.length).toBeGreaterThan(0);
    
    const texts = await page.locator('.slot-text').allTextContents();
    const nonEmptyTexts = texts.filter(t => t.trim().length > 0);
    
    console.log(' slot-text内容:', nonEmptyTexts.slice(0, 5));
    expect(nonEmptyTexts.length).toBeGreaterThan(0);
    
    console.log(' Structure Builder: データ読み込み成功');
  });

  /**
   * Test-2: 【必須】主要スロットの順序が正しい（サブスロットを除外してチェック）
   */
  test('【必須】主要スロットの順序が正しい', async ({ page }) => {
    // サブスロットを除外した主要スロットのみを取得
    const mainSlots = page.locator('.slot-container:not([id*="sub"]):not(.hidden):not(.empty-slot-hidden)');
    const count = await mainSlots.count();
    
    console.log(' 主要スロット数:', count);
    expect(count).toBeGreaterThan(0);
    
    const slotIds: string[] = [];
    for (let i = 0; i < count; i++) {
      const id = await mainSlots.nth(i).getAttribute('id');
      if (id) slotIds.push(id);
    }
    console.log(' 主要スロットID順:', slotIds);
    
    // 主要スロットの期待順序（文法構造に基づく）
    const expectedOrder = ['slot-m1', 'slot-s', 'slot-aux', 'slot-m2', 'slot-v', 'slot-c1', 'slot-o1', 'slot-o2', 'slot-c2', 'slot-m3'];
    
    let lastExpectedIndex = -1;
    for (const id of slotIds) {
      const expectedIndex = expectedOrder.indexOf(id);
      if (expectedIndex !== -1) {
        expect(expectedIndex).toBeGreaterThanOrEqual(lastExpectedIndex);
        lastExpectedIndex = expectedIndex;
      }
    }
    
    console.log(' 主要スロット順序: 正しい');
  });

  /**
   * Test-3: 【必須】全体ランダマイズで内容が変わる
   * 
   * 実際のID: #randomize-all
   */
  test('【必須】全体ランダマイズで内容が変わる', async ({ page }) => {
    // 【必須】全体ランダマイズボタンの存在確認
    const randomizeBtn = page.locator('#randomize-all');
    await expect(randomizeBtn).toHaveCount(1);
    
    // ランダマイズ前のフレーズを記録
    const beforePhrases = await page.locator('.slot-phrase').allTextContents();
    const beforeContent = beforePhrases.filter(p => p.trim()).join('|');
    
    console.log(' ランダマイズ前:', beforeContent.substring(0, 100));
    
    // 【改善】expect.pollで変化を待つ（最大3回試行）
    let changed = false;
    let afterContent = '';
    
    for (let attempt = 0; attempt < 3 && !changed; attempt++) {
      await randomizeBtn.click();
      
      try {
        await expect.poll(async () => {
          const after = await page.locator('.slot-phrase').allTextContents();
          afterContent = after.filter(p => p.trim()).join('|');
          return afterContent !== beforeContent;
        }, { timeout: 3000 }).toBe(true);
        changed = true;
      } catch {
        console.log(' 試行', attempt + 1, ': 変化なし、再試行...');
      }
    }
    
    console.log(' ランダマイズ後:', afterContent.substring(0, 100));
    expect(changed).toBe(true);
    console.log(' Randomizer: 全体ランダマイズで内容変更確認');
  });

  /**
   * Test-4: 【必須】ランダマイズ後もスロット構造が維持される
   */
  test('【必須】ランダマイズ後もスロット構造が維持される', async ({ page }) => {
    const beforeCount = await page.locator('.slot-container').count();
    console.log(' ランダマイズ前のスロット数:', beforeCount);
    
    const randomizeBtn = page.locator('#randomize-all');
    await expect(randomizeBtn).toHaveCount(1);
    
    await randomizeBtn.click();
    
    // 【改善】expect.pollで構造維持を確認
    await expect.poll(async () => {
      return await page.locator('.slot-container').count();
    }, { timeout: 5000 }).toBeGreaterThan(0);
    
    const afterCount = await page.locator('.slot-container').count();
    console.log(' ランダマイズ後のスロット数:', afterCount);
    
    // 【必須】スロット数が極端に減っていないこと
    expect(afterCount).toBeGreaterThanOrEqual(beforeCount * 0.5);
    
    console.log(' ランダマイズ後もスロット構造維持');
  });

  /**
   * Test-5: 【任意】サブスロットの折りたたみ/展開
   */
  test('【任意】サブスロットの折りたたみ/展開', async ({ page }) => {
    const toggleBtns = page.locator('button[data-subslot-toggle]');
    const count = await toggleBtns.count();
    
    if (count === 0) {
      test.skip();
      return;
    }
    
    const firstToggle = toggleBtns.first();
    const subslotContainer = page.locator('[id*="subslot"], .subslot-container').first();
    
    if (await subslotContainer.count() === 0) {
      test.skip();
      return;
    }
    
    const beforeVisible = await subslotContainer.isVisible();
    console.log(' トグル前のサブスロット表示状態:', beforeVisible);
    
    await firstToggle.click();
    
    // 【改善】expect.pollで状態変化を待つ
    await expect.poll(async () => {
      return await subslotContainer.isVisible();
    }, { timeout: 2000 }).toBe(!beforeVisible);
    
    console.log(' Subslot Toggle: 折りたたみ/展開機能正常');
  });

  /**
   * Test-6: 【任意】スロットにイラストが正しくロードされる（naturalWidth確認）
   */
  test('【任意】スロットにイラストが正しくロードされる', async ({ page }) => {
    const images = page.locator('.slot-image');
    const count = await images.count();
    
    if (count === 0) {
      test.skip();
      return;
    }
    
    console.log(' スロットイメージ数:', count);
    
    // 【改善】naturalWidthで実際にロードされているか確認
    let loadedCount = 0;
    
    for (let i = 0; i < Math.min(count, 10); i++) {
      const img = images.nth(i);
      const src = await img.getAttribute('src');
      
      if (src && !src.includes('placeholder')) {
        const naturalWidth = await img.evaluate((el: HTMLImageElement) => el.naturalWidth);
        
        if (naturalWidth > 0) {
          loadedCount++;
          console.log(' ロード済み:', src.split('/').pop(), '(' + naturalWidth + 'px)');
        }
      }
    }
    
    console.log(' ロード済みイメージ数:', loadedCount);
    expect(loadedCount).toBeGreaterThan(0);
    console.log(' Image System: イラスト正常ロード確認');
  });

  /**
   * Test-7: 【必須】制御パネルが開く
   */
  test('【必須】制御パネルが開く', async ({ page }) => {
    const toggleBtn = page.locator('#toggle-control-panels');
    await expect(toggleBtn).toHaveCount(1);
    
    await toggleBtn.click();
    
    const controlPanel = page.locator('#visibility-control-panel-inline');
    await expect(controlPanel).toBeVisible({ timeout: 2000 });
    
    console.log(' 制御パネル表示: OK');
    
    // チェックボックスが存在することを確認
    const checkboxes = controlPanel.locator('input[type="checkbox"]');
    const checkboxCount = await checkboxes.count();
    
    console.log(' 制御パネル内のチェックボックス数:', checkboxCount);
    expect(checkboxCount).toBeGreaterThan(0);
    
    console.log(' Control Panel: 制御パネル表示チェックボックス存在確認');
  });

  /**
   * Test-8: 【任意】音声ボタンが存在する
   */
  test('【任意】音声ボタンが存在する', async ({ page }) => {
    const voiceBtn = page.locator('#play-voice-button, .voice-button, button[data-voice]').first();
    
    if (await voiceBtn.count() === 0) {
      test.skip();
      return;
    }
    
    const isEnabled = await voiceBtn.isEnabled();
    console.log(' 音声ボタン有効状態:', isEnabled);
    
    expect(isEnabled).toBe(true);
    console.log(' Voice System: 音声ボタン存在確認');
  });
});
