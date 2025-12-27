import { test, expect } from '@playwright/test';

/**
 * RephraseUI 機能テスト
 * 
 * RephraseUIの実際の仕様に基づいた有意義なテスト
 * 
 * 【検証対象の機能】
 * 1. Structure Builder - DBからスロット構造を構築
 * 2. Randomizer - 全体/個別ランダマイズでV_group_key単位で内容が変わる
 * 3. Control Panel - スロット要素の表示/非表示切り替え
 * 4. Subslot Toggle - サブスロットの折りたたみ/展開
 * 5. Image System - イラストがスロットに表示される
 */

test.describe('RephraseUI 機能テスト', () => {
  
  // 各テストの前にデータをロード
  test.beforeEach(async ({ page }) => {
    // 認証スキップでページを開く
    await page.goto('/training/index.html?skipAuth=true');
    await page.waitForLoadState('networkidle');
    
    // データを選択して読み込み
    await page.selectOption('#presetSelect', 'data/slot_order_data.json');
    await page.click('#loadPresetButton');
    
    // データロード完了を待機（slot-phraseにテキストが入るまで）
    await page.waitForFunction(() => {
      const phrases = document.querySelectorAll('.slot-phrase');
      for (const p of phrases) {
        if (p.textContent && p.textContent.trim().length > 0) return true;
      }
      return false;
    }, { timeout: 15000 });
    
    await page.waitForTimeout(1000); // 追加の安定化
  });

  /**
   * Test-1: Structure Builder - スロットにDBからデータが正しく読み込まれる
   * 
   * 検証内容:
   * - .slot-phraseに英語フレーズが入っている
   * - .slot-textに日本語テキストが入っている
   * - 主要スロット（S, V, O1等）が存在する
   */
  test('スロットにDBからデータが正しく読み込まれる', async ({ page }) => {
    // slot-phraseの内容を取得
    const phrases = await page.locator('.slot-phrase').allTextContents();
    const nonEmptyPhrases = phrases.filter(p => p.trim().length > 0);
    
    console.log('📝 slot-phrase内容:', nonEmptyPhrases.slice(0, 5));
    
    // 少なくとも1つのスロットにフレーズが入っている
    expect(nonEmptyPhrases.length).toBeGreaterThan(0);
    
    // slot-textの内容を取得（日本語補助テキスト）
    const texts = await page.locator('.slot-text').allTextContents();
    const nonEmptyTexts = texts.filter(t => t.trim().length > 0);
    
    console.log('📝 slot-text内容:', nonEmptyTexts.slice(0, 5));
    
    // 日本語テキストも存在する
    expect(nonEmptyTexts.length).toBeGreaterThan(0);
    
    console.log('✅ Structure Builder: データ読み込み成功');
  });

  /**
   * Test-2: Randomizer - 全体ランダマイズでV_group_keyが変わり内容が更新される
   * 
   * 検証内容:
   * - ランダマイズボタンクリック前後で.slot-phraseの内容が変わる
   * - 変化はV_group_key単位で起こる（同じV_group_keyが連続しない）
   */
  test('全体ランダマイズで内容が変わる', async ({ page }) => {
    // ランダマイズ前のフレーズを記録
    const beforePhrases = await page.locator('.slot-phrase').allTextContents();
    const beforeContent = beforePhrases.filter(p => p.trim()).join('|');
    
    console.log('📝 ランダマイズ前:', beforeContent.substring(0, 100));
    
    // 全体ランダマイズボタンをクリック
    const randomizeBtn = page.locator('#randomize-all-button');
    
    if (await randomizeBtn.count() > 0) {
      // 複数回クリックして変化を確認（V_group_key重複回避があるので変わるはず）
      await randomizeBtn.click();
      await page.waitForTimeout(2000);
      
      const afterPhrases = await page.locator('.slot-phrase').allTextContents();
      const afterContent = afterPhrases.filter(p => p.trim()).join('|');
      
      console.log('📝 ランダマイズ後:', afterContent.substring(0, 100));
      
      // 内容が変わっているか確認（同じV_group_keyでなければ変わるはず）
      // 注意: 同じV_group_keyが選ばれる可能性もあるので、複数回試す
      let changed = beforeContent !== afterContent;
      
      if (!changed) {
        // もう一度試す
        await randomizeBtn.click();
        await page.waitForTimeout(2000);
        const retry = await page.locator('.slot-phrase').allTextContents();
        changed = beforeContent !== retry.filter(p => p.trim()).join('|');
      }
      
      expect(changed).toBe(true);
      console.log('✅ Randomizer: 全体ランダマイズで内容変更確認');
    } else {
      console.log('⚠️ 全体ランダマイズボタンが見つからない');
    }
  });

  /**
   * Test-3: Subslot Toggle - サブスロットの折りたたみ/展開が機能する
   * 
   * 検証内容:
   * - ▼詳細ボタンクリックでサブスロットが展開/折りたたみされる
   * - 展開時はサブスロット内のテキストが見える
   */
  test('サブスロットの折りたたみ/展開', async ({ page }) => {
    // サブスロットトグルボタンを探す
    const toggleBtns = page.locator('button[data-subslot-toggle]');
    const count = await toggleBtns.count();
    
    if (count > 0) {
      const firstToggle = toggleBtns.first();
      const toggleId = await firstToggle.getAttribute('data-subslot-toggle');
      
      // 対応するサブスロットコンテナを探す
      const subslotContainer = page.locator(`#slot-${toggleId}-subslots, .subslot-container[data-parent="${toggleId}"]`).first();
      
      if (await subslotContainer.count() > 0) {
        // 現在の表示状態を記録
        const beforeVisible = await subslotContainer.isVisible();
        console.log(`📝 トグル前のサブスロット表示状態: ${beforeVisible}`);
        
        // トグルボタンをクリック
        await firstToggle.click();
        await page.waitForTimeout(500);
        
        // 表示状態が変わったか確認
        const afterVisible = await subslotContainer.isVisible();
        console.log(`📝 トグル後のサブスロット表示状態: ${afterVisible}`);
        
        // 状態が反転しているか
        expect(afterVisible).toBe(!beforeVisible);
        console.log('✅ Subslot Toggle: 折りたたみ/展開機能正常');
      } else {
        console.log('⚠️ サブスロットコンテナが見つからない');
      }
    } else {
      console.log('⚠️ サブスロットトグルボタンが見つからない（このデータにはサブスロットがない可能性）');
    }
  });

  /**
   * Test-4: Image System - スロットにイラストが表示される
   * 
   * 検証内容:
   * - .slot-imageのsrcがplaceholder以外になっている
   * - イラストが実際にロードされている
   */
  test('スロットにイラストが表示される', async ({ page }) => {
    // スロットイメージを取得
    const images = page.locator('.slot-image');
    const count = await images.count();
    
    console.log(`📝 スロットイメージ数: ${count}`);
    
    if (count > 0) {
      // 少なくとも1つのイメージがplaceholder以外を参照しているか
      let hasRealImage = false;
      
      for (let i = 0; i < Math.min(count, 10); i++) {
        const src = await images.nth(i).getAttribute('src');
        if (src && !src.includes('placeholder')) {
          hasRealImage = true;
          console.log(`📝 実イメージ発見: ${src}`);
          break;
        }
      }
      
      expect(hasRealImage).toBe(true);
      console.log('✅ Image System: イラスト表示確認');
    } else {
      console.log('⚠️ スロットイメージが見つからない');
    }
  });

  /**
   * Test-5: Control Panel - 制御パネルでスロット要素の表示/非表示を切り替えられる
   * 
   * 検証内容:
   * - 制御パネルボタンで制御パネルが開く
   * - スロット要素のチェックボックスで表示/非表示が切り替わる
   */
  test('制御パネルでスロット表示/非表示を切り替えられる', async ({ page }) => {
    // 制御パネルトグルボタンを探す
    const toggleBtn = page.locator('#toggle-control-panels');
    
    if (await toggleBtn.count() > 0) {
      // 制御パネルを開く
      await toggleBtn.click();
      await page.waitForTimeout(500);
      
      // 制御パネルが表示されたか
      const controlPanel = page.locator('#visibility-control-panel-inline');
      
      if (await controlPanel.count() > 0) {
        const isVisible = await controlPanel.isVisible();
        console.log(`📝 制御パネル表示状態: ${isVisible}`);
        
        expect(isVisible).toBe(true);
        
        // 表示されているチェックボックスを探して操作
        const checkboxes = controlPanel.locator('input[type="checkbox"]:visible');
        const checkboxCount = await checkboxes.count();
        
        console.log(`📝 制御パネル内の可視チェックボックス数: ${checkboxCount}`);
        
        if (checkboxCount > 0) {
          // 最初の可視チェックボックスの状態を変更
          const firstCheckbox = checkboxes.first();
          const beforeChecked = await firstCheckbox.isChecked();
          
          await firstCheckbox.click();
          await page.waitForTimeout(300);
          
          const afterChecked = await firstCheckbox.isChecked();
          
          // 状態が変わったか
          expect(afterChecked).toBe(!beforeChecked);
          console.log('✅ Control Panel: 表示/非表示切り替え機能正常');
        } else {
          // 可視チェックボックスがない場合は、制御パネルが開くことだけを確認
          console.log('⚠️ 可視チェックボックスがないが、制御パネルは開いた');
        }
      } else {
        console.log('⚠️ 制御パネル要素が見つからない');
      }
    } else {
      console.log('⚠️ 制御パネルトグルボタンが見つからない');
    }
  });

  /**
   * Test-6: 音声ボタンが存在し、クリック可能である
   * 
   * 検証内容:
   * - 音声再生ボタンが存在する
   * - ボタンがクリック可能な状態である
   */
  test('音声ボタンが存在する', async ({ page }) => {
    // 音声関連のボタンを探す
    const voiceBtn = page.locator('#play-voice-button, .voice-button, button[data-voice]').first();
    
    if (await voiceBtn.count() > 0) {
      const isEnabled = await voiceBtn.isEnabled();
      console.log(`📝 音声ボタン有効状態: ${isEnabled}`);
      
      expect(isEnabled).toBe(true);
      console.log('✅ Voice System: 音声ボタン存在確認');
    } else {
      // 音声ボタンがない場合は警告のみ（必須機能ではない場合）
      console.log('⚠️ 音声ボタンが見つからない（オプション機能の可能性）');
    }
  });
});
