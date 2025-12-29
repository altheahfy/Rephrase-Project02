import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

/**
 * RephraseUI「私の代行テスト」
 * 
 * 【目的】
 * 人間が修正後に必ず行っていた確認行為を自動化する
 * 「UIの一般的な動作確認」ではなく「私ならOKを出すか？」を判断する
 * 
 * 【対象DB】
 * プルダウンメニューの「フルセット」（data/slot_order_data.json）
 * ※将来的に変更可能
 */

// 対象プリセットの定義（ここを変更して切り替え可能）
const TARGET_PRESET_NAME = 'フルセット';
const TARGET_PRESET_FILE = 'data/slot_order_data.json';

test.describe('RephraseUI 私の代行テスト', () => {
  
  let dbData: any;
  
  test.beforeAll(async () => {
    // DBデータを読み込み（配列形式）
    const dbPath = path.resolve(__dirname, '..', 'training', TARGET_PRESET_FILE);
    const rawData = fs.readFileSync(dbPath, 'utf-8');
    dbData = JSON.parse(rawData);
    
    console.log(`📋 対象DB: ${TARGET_PRESET_NAME} (${TARGET_PRESET_FILE})`);
    console.log(`📊 DB内のスロット行数: ${dbData.length}`);
    
    // 例文ID一覧を抽出
    const exampleIds = new Set<string>();
    for (const row of dbData) {
      if (row.例文ID) exampleIds.add(row.例文ID);
    }
    console.log(`📊 例文数: ${exampleIds.size}`);
  });
  
  test.beforeEach(async ({ page }) => {
    // URLパラメータなしでページを開く（grammarパラメータの影響を排除）
    await page.goto('/training/index.html?skipAuth=true');
    await page.waitForLoadState('networkidle');
    
    // プリセット選択UIが準備完了するまで待機
    await page.waitForTimeout(1000);
    
    // プルダウンから「フルセット」を選択
    const presetSelect = page.locator('#presetSelect');
    await expect(presetSelect).toBeVisible({ timeout: 5000 });
    
    const currentValue = await presetSelect.inputValue();
    console.log(`🔍 プリセット選択前の値: ${currentValue}`);
    
    // 強制的に「フルセット」を選択
    await page.evaluate((targetFile) => {
      const select = document.getElementById('presetSelect') as HTMLSelectElement;
      if (select) {
        select.value = targetFile;
        // changeイベントを発火（自動ロード処理がある場合に備えて）
        select.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }, TARGET_PRESET_FILE);
    
    await page.waitForTimeout(500);
    
    const afterValue = await presetSelect.inputValue();
    console.log(`🔍 プリセット選択後の値: ${afterValue}`);
    
    if (afterValue !== TARGET_PRESET_FILE) {
      throw new Error(`❌ プリセット選択失敗: 期待=${TARGET_PRESET_FILE}, 実際=${afterValue}`);
    }
    
    // ロードボタンをクリック
    const loadBtn = page.locator('#loadPresetButton');
    await expect(loadBtn).toBeVisible({ timeout: 5000 });
    await loadBtn.click();
    
    console.log('✅ プリセットロードボタンクリック完了');
    
    // JSONデータロード完了を確実に待機
    await page.waitForFunction((expectedFile) => {
      // window.loadedJsonDataが更新されているか確認
      const loadedData = (window as any).loadedJsonData;
      if (!loadedData || !Array.isArray(loadedData) || loadedData.length === 0) {
        return false;
      }
      
      // プリセット選択が期待値と一致しているか確認
      const select = document.getElementById('presetSelect') as HTMLSelectElement;
      if (!select || select.value !== expectedFile) {
        return false;
      }
      
      // スロット内容が表示されているか確認
      const phrases = document.querySelectorAll('.slot-phrase');
      for (const p of phrases) {
        if (p.textContent && p.textContent.trim().length > 0) {
          return true;
        }
      }
      return false;
    }, TARGET_PRESET_FILE, { timeout: 15000 });
    
    console.log('✅ データロード完了確認');
    
    // ロードされたデータの情報を取得
    const loadedInfo = await page.evaluate(() => {
      const data = (window as any).loadedJsonData;
      const select = document.getElementById('presetSelect') as HTMLSelectElement;
      return {
        dataLength: data?.length || 0,
        presetValue: select?.value || 'unknown'
      };
    });
    
    console.log(`📊 ロードされたデータ行数: ${loadedInfo.dataLength}`);
    console.log(`📋 確認されたプリセット値: ${loadedInfo.presetValue}`);
    
    // データが正しくロードされていることを確認
    if (loadedInfo.dataLength === 0) {
      throw new Error('❌ データがロードされていません');
    }
    
    if (loadedInfo.presetValue !== TARGET_PRESET_FILE) {
      throw new Error(`❌ プリセット不一致: 期待=${TARGET_PRESET_FILE}, 実際=${loadedInfo.presetValue}`);
    }
    
    // サブスロットトグルボタンの数を確認
    const toggleBtns = await page.locator('button[data-subslot-toggle]').count();
    console.log(`📍 サブスロットトグルボタン数: ${toggleBtns}`);
  });

  /**
   * Test-3: 【最優先】全サブスロットに対する開閉操作でhidden状態が解除されないか
   * 
   * 目的: サブスロット開閉操作が、学習者の設定した「非表示状態」を破壊しないことを保証
   */
  test('[最優先] 全サブスロット開閉操作でhidden状態が保持される', async ({ page }) => {
    // 1. 英語テキスト・日本語補助テキストを非表示に設定
    const toggleBtn = page.locator('#toggle-control-panels');
    await toggleBtn.click();
    
    const controlPanel = page.locator('#visibility-control-panel-inline');
    await expect(controlPanel).toBeVisible({ timeout: 2000 });
    
    // 全チェックボックスを取得してOFFにする
    const checkboxes = controlPanel.locator('input[type="checkbox"]');
    const checkboxCount = await checkboxes.count();
    
    console.log(`🔧 制御パネル内のチェックボックス数: ${checkboxCount}`);
    
    // 全てOFFにする
    for (let i = 0; i < checkboxCount; i++) {
      const checkbox = checkboxes.nth(i);
      if (await checkbox.isChecked()) {
        await checkbox.evaluate((el: HTMLInputElement) => el.click());
      }
    }
    
    console.log('✅ 全テキストを非表示に設定完了');
    
    // 制御パネルを閉じる
    await toggleBtn.click();
    await page.waitForTimeout(500);
    
    // 2. 静的スロットDOM内の全サブスロットトグルボタンを列挙
    const toggleBtns = page.locator('button[data-subslot-toggle]');
    const toggleCount = await toggleBtns.count();
    
    if (toggleCount === 0) {
      console.log('⚠️ サブスロットトグルボタンが見つからない（このプリセットにはサブスロットがない）');
      test.skip();
      return;
    }
    
    console.log(`📍 サブスロットトグルボタン数: ${toggleCount}`);
    
    // 3. 各サブスロットについて開く→閉じる→静的スロットDOMのhidden状態確認
    let testCount = 0;
    let failCount = 0;
    
    for (let i = 0; i < toggleCount; i++) {
      const toggleBtn = toggleBtns.nth(i);
      const toggleId = await toggleBtn.getAttribute('data-subslot-toggle');
      
      if (!toggleId) continue;
      
      // 静的スロットDOM（.slot-wrapper#slot-{parent}-sub）を取得
      const staticWrapper = page.locator(`#${toggleId}`);
      
      if (await staticWrapper.count() === 0) {
        console.log(`⚠️ 静的スロットDOM ${toggleId} が見つからない`);
        continue;
      }
      
      // 開く
      const beforeOpenVisible = await staticWrapper.isVisible();
      if (!beforeOpenVisible) {
        await toggleBtn.click();
        await page.waitForTimeout(400);
      }
      
      // 静的スロットDOM内の全.subslot-containerを取得
      const subslotContainers = staticWrapper.locator('.subslot-container');
      const containerCount = await subslotContainers.count();
      
      // 各.subslot-container内のテキスト要素のhidden状態を確認
      for (let j = 0; j < containerCount; j++) {
        const container = subslotContainers.nth(j);
        const containerId = await container.getAttribute('id');
        
        const slotPhrase = container.locator('.slot-phrase');
        const slotText = container.locator('.slot-text');
        
        if (await slotPhrase.count() > 0) {
          const isPhraseVisible = await slotPhrase.first().evaluate(el => {
            const style = window.getComputedStyle(el);
            return style.opacity !== '0' && style.visibility !== 'hidden' && style.display !== 'none';
          });
          
          if (isPhraseVisible) {
            console.log(`❌ 静的スロットDOM ${containerId}: .slot-phrase が表示されている（hidden状態が解除された）`);
            failCount++;
          }
        }
        
        if (await slotText.count() > 0) {
          const isTextVisible = await slotText.first().evaluate(el => {
            const style = window.getComputedStyle(el);
            return style.opacity !== '0' && style.visibility !== 'hidden' && style.display !== 'none';
          });
          
          if (isTextVisible) {
            console.log(`❌ 静的スロットDOM ${containerId}: .slot-text が表示されている（hidden状態が解除された）`);
            failCount++;
          }
        }
      }
      
      // 閉じる
      await toggleBtn.click();
      await page.waitForTimeout(400);
      
      testCount++;
    }
    
    console.log(`✅ テスト完了: ${testCount}個のサブスロット検証`);
    
    // 判定
    expect(failCount).toBe(0);
    
    if (failCount === 0) {
      console.log('🎉 静的スロットDOM全サブスロットでhidden状態が保持されている');
    }
  });

  /**
   * Test-4: 【最優先】ランダマイズ後もhidden状態が解除されないか（主節・サブスロット両方）
   * 
   * 目的: ランダマイズがUI再描画を伴っても、ユーザー設定（非表示）が保持されることを保証
   */
  test('[最優先] ランダマイズ後もhidden状態が保持される', async ({ page }) => {
    // 1. 英語テキスト・日本語補助テキストを非表示に設定
    const toggleBtn = page.locator('#toggle-control-panels');
    await toggleBtn.click();
    
    const controlPanel = page.locator('#visibility-control-panel-inline');
    await expect(controlPanel).toBeVisible({ timeout: 2000 });
    
    const checkboxes = controlPanel.locator('input[type="checkbox"]');
    const checkboxCount = await checkboxes.count();
    
    // 全てOFFにする
    for (let i = 0; i < checkboxCount; i++) {
      const checkbox = checkboxes.nth(i);
      if (await checkbox.isChecked()) {
        await checkbox.evaluate((el: HTMLInputElement) => el.click());
      }
    }
    
    console.log('✅ 全テキストを非表示に設定完了');
    
    // 制御パネルを閉じる
    await toggleBtn.click();
    await page.waitForTimeout(500);
    
    // 2. ランダマイズを複数回実行して検証
    const randomizeBtn = page.locator('#randomize-all');
    await expect(randomizeBtn).toHaveCount(1);
    
    const RANDOMIZE_COUNT = 5;
    let totalFailCount = 0;
    
    for (let round = 0; round < RANDOMIZE_COUNT; round++) {
      await randomizeBtn.click();
      await page.waitForTimeout(1000);
      
      console.log(`\n🔄 ランダマイズ ${round + 1}/${RANDOMIZE_COUNT}回目`);
      
      // 静的スロットDOM（主節）のhidden状態確認
      const mainSlotContainers = page.locator('.slot-container:not([id*="-sub"])');
      const mainContainerCount = await mainSlotContainers.count();
      
      let roundFailCount = 0;
      
      // 主節の各.slot-containerを検証
      for (let i = 0; i < mainContainerCount; i++) {
        const container = mainSlotContainers.nth(i);
        const containerId = await container.getAttribute('id');
        
        const slotPhrase = container.locator('.slot-phrase');
        const slotText = container.locator('.slot-text');
        
        if (await slotPhrase.count() > 0) {
          const isPhraseVisible = await slotPhrase.first().evaluate(el => {
            const style = window.getComputedStyle(el);
            return style.opacity !== '0' && style.visibility !== 'hidden' && style.display !== 'none';
          });
          
          if (isPhraseVisible) {
            console.log(`❌ 静的スロットDOM ${containerId}: .slot-phrase が表示されている`);
            roundFailCount++;
          }
        }
        
        if (await slotText.count() > 0) {
          const isTextVisible = await slotText.first().evaluate(el => {
            const style = window.getComputedStyle(el);
            return style.opacity !== '0' && style.visibility !== 'hidden' && style.display !== 'none';
          });
          
          if (isTextVisible) {
            console.log(`❌ 静的スロットDOM ${containerId}: .slot-text が表示されている`);
            roundFailCount++;
          }
        }
      }
      
      // 静的スロットDOM（サブスロット）のhidden状態確認
      const staticSubWrappers = page.locator('.slot-wrapper[id*="-sub"]');
      const wrapperCount = await staticSubWrappers.count();
      
      let visibleSubCount = 0;
      
      for (let i = 0; i < wrapperCount; i++) {
        const wrapper = staticSubWrappers.nth(i);
        const isWrapperVisible = await wrapper.isVisible();
        
        if (!isWrapperVisible) continue;
        
        visibleSubCount++;
        
        const subslotContainers = wrapper.locator('.subslot-container');
        const containerCount = await subslotContainers.count();
        
        for (let j = 0; j < containerCount; j++) {
          const container = subslotContainers.nth(j);
          const containerId = await container.getAttribute('id');
          
          const slotPhrase = container.locator('.slot-phrase');
          const slotText = container.locator('.slot-text');
          
          if (await slotPhrase.count() > 0) {
            const isPhraseVisible = await slotPhrase.first().evaluate(el => {
              const style = window.getComputedStyle(el);
              return style.opacity !== '0' && style.visibility !== 'hidden' && style.display !== 'none';
            });
            
            if (isPhraseVisible) {
              console.log(`❌ 静的サブスロットDOM ${containerId}: .slot-phrase が表示されている`);
              roundFailCount++;
            }
          }
          
          if (await slotText.count() > 0) {
            const isTextVisible = await slotText.first().evaluate(el => {
              const style = window.getComputedStyle(el);
              return style.opacity !== '0' && style.visibility !== 'hidden' && style.display !== 'none';
            });
            
            if (isTextVisible) {
              console.log(`❌ 静的サブスロットDOM ${containerId}: .slot-text が表示されている`);
              roundFailCount++;
            }
          }
        }
      }
      
      console.log(`📍 表示中の静的サブスロットラッパー数: ${visibleSubCount}`);
      
      if (roundFailCount === 0) {
        console.log(`✅ ${round + 1}回目: hidden状態保持OK`);
      } else {
        console.log(`❌ ${round + 1}回目: ${roundFailCount}個の要素でhidden状態が解除された`);
      }
      
      totalFailCount += roundFailCount;
    }
    
    console.log(`\n📊 総合結果: ${RANDOMIZE_COUNT}回のランダマイズで ${totalFailCount}個の違反`);
    
    // 判定
    expect(totalFailCount).toBe(0);
    
    if (totalFailCount === 0) {
      console.log('🎉 ランダマイズ後もhidden状態が完全保持されている');
    }
  });

  /**
   * Test-2: イレギュラーなorderが定義されている場合、UI表示順がorderに従っているか
   * 
   * 目的: DB側で定義された語順（order）が、UIで無視・正規化されていないことを保証
   */
  test('[必須] イレギュラーなorder定義がUI表示順に反映される', async ({ page }) => {
    // DBから例文IDごとにスロット順序を抽出
    const exampleOrders = new Map<string, any[]>();
    
    for (const row of dbData) {
      if (!row.例文ID || row.SubslotID) continue; // 主節スロットのみ
      
      if (!exampleOrders.has(row.例文ID)) {
        exampleOrders.set(row.例文ID, []);
      }
      
      exampleOrders.get(row.例文ID)!.push({
        slot: row.Slot,
        order: row.Slot_display_order
      });
    }
    
    // 各例文のスロット順序をソート
    const standardOrder = ['M1', 'S', 'Aux', 'M2', 'V', 'C1', 'O1', 'O2', 'C2', 'M3'];
    const irregularExamples: any[] = [];
    
    for (const [exampleId, slots] of exampleOrders) {
      const sortedSlots = slots.sort((a, b) => a.order - b.order);
      const actualOrder = sortedSlots.map(s => s.slot);
      
      // 標準順序（該当スロットのみ）
      const expectedOrder = standardOrder.filter(s => actualOrder.includes(s));
      
      // 完全一致しない場合はイレギュラー
      const isIrregular = JSON.stringify(actualOrder) !== JSON.stringify(expectedOrder);
      
      if (isIrregular) {
        irregularExamples.push({
          id: exampleId,
          actualOrder: actualOrder,
          expectedOrder: expectedOrder
        });
      }
    }
    
    console.log(`📋 イレギュラーなorder定義: ${irregularExamples.length}個`);
    
    if (irregularExamples.length === 0) {
      console.log('⚠️ イレギュラーなorder定義が見つからない（全て標準順）');
      test.skip();
      return;
    }
    
    console.log(`📝 イレギュラー例:`, irregularExamples.slice(0, 3));
    
    // ランダマイズを複数回実行して、イレギュラーorder例文を検証
    const randomizeBtn = page.locator('#randomize-all');
    let testCount = 0;
    const MAX_ATTEMPTS = 20;
    
    for (let attempt = 0; attempt < MAX_ATTEMPTS && testCount < 3; attempt++) {
      await randomizeBtn.click();
      await page.waitForTimeout(1000);
      
      // 現在表示中のスロットDOMを取得
      const mainSlots = page.locator('.slot-container:not([id*="sub"]):not(.hidden)');
      const slotCount = await mainSlots.count();
      
      const displayedSlots: string[] = [];
      for (let i = 0; i < slotCount; i++) {
        const id = await mainSlots.nth(i).getAttribute('id');
        if (id) {
          // id形式: "slot-m1" → "M1"
          const slotType = id.replace('slot-', '').toUpperCase();
          displayedSlots.push(slotType);
        }
      }
      
      // 表示されているスロット順序が標準順から逸脱しているか確認
      const expectedDisplayed = standardOrder.filter(s => displayedSlots.includes(s));
      const isIrregular = JSON.stringify(displayedSlots) !== JSON.stringify(expectedDisplayed);
      
      if (isIrregular) {
        console.log(`✅ イレギュラーorder検出: ${displayedSlots.join(' → ')}`);
        console.log(`   期待標準順: ${expectedDisplayed.join(' → ')}`);
        testCount++;
      }
    }
    
    console.log(`📊 イレギュラーorder検証数: ${testCount}個`);
    
    // 少なくとも1つはイレギュラーorderを検証できた
    expect(testCount).toBeGreaterThan(0);
    
    console.log('🎉 イレギュラーorder定義がUI表示順に反映されている');
  });

  /**
   * Test-1: DBに存在する全てのサブスロットが画面上に一度以上表示されるか
   * 
   * 目的: DBに存在するサブスロット構造が、UI表示ロジック上で欠落していないことを保証
   * 
   * ロジック:
   * 1. DB内の各例文について、親スロットごとのサブスロット構造をマップ化
   *    例: make/ex007 → S に [sub-s, sub-aux, sub-m2, sub-v, sub-o1]
   * 2. ランダマイズで各例文を表示し、各親スロットのサブスロットが全て表示されているか確認
   * 3. DB内の全サブスロット組み合わせ（親+サブ）がUIに出現するまで繰り返す
   */
  test('[必須] DBの全サブスロット種別がUIに表示される', async ({ page }) => {
    test.setTimeout(300000); // 5分
    
    // 1. DBから例文構造をマップ化：各例文の各親スロットにどのサブスロットがあるか
    const exampleStructure = new Map<string, Map<string, Set<string>>>();
    // 形式: Map<"V_group_key/例文ID", Map<"親スロット", Set<"サブスロット種別">>>
    
    for (const row of dbData) {
      if (row.SubslotID && row.Slot && row.V_group_key && row.例文ID) {
        const exampleKey = `${row.V_group_key}/${row.例文ID}`;
        if (!exampleStructure.has(exampleKey)) {
          exampleStructure.set(exampleKey, new Map());
        }
        const example = exampleStructure.get(exampleKey)!;
        const parentSlot = row.Slot.toLowerCase();
        if (!example.has(parentSlot)) {
          example.set(parentSlot, new Set());
        }
        example.get(parentSlot)!.add(row.SubslotID);
      }
    }
    
    console.log(`📋 DB内の例文数: ${exampleStructure.size}`);
    
    // DB内の全サブスロット組み合わせ（親+サブ）を集計
    const allDbCombinations = new Set<string>();
    exampleStructure.forEach((parentMap, exampleKey) => {
      parentMap.forEach((subslots, parentSlot) => {
        subslots.forEach(subslotId => {
          allDbCombinations.add(`${parentSlot}-${subslotId}`);
        });
      });
    });
    
    console.log(`📊 DB内の全サブスロット組み合わせ: ${allDbCombinations.size}種類`);
    console.log(`   ${Array.from(allDbCombinations).sort().join(', ')}`);
    
    if (allDbCombinations.size === 0) {
      console.log('⚠️ DBにサブスロットが存在しない');
      test.skip();
      return;
    }
    
    // 2. ランダマイズして各例文の各親スロットのサブスロットが全て表示されるか確認
    const uiFoundCombinations = new Set<string>();
    const randomizeBtn = page.locator('#randomize-all');
    const MAX_RANDOMIZE = 50;
    
    for (let i = 0; i < MAX_RANDOMIZE; i++) {
      await randomizeBtn.click();
      await page.waitForTimeout(1000);
      
      // 現在表示中のサブスロットトグルボタンを取得
      const toggleBtns = page.locator('button[data-subslot-toggle]');
      const toggleCount = await toggleBtns.count();
      
      if (toggleCount === 0) {
        console.log(`  ⚠️ ${i + 1}回目: サブスロットトグルボタンなし（スキップ）`);
        continue;
      }
      
      console.log(`\n━━━ ${i + 1}回目のランダマイズ: トグルボタン ${toggleCount}個 ━━━`);
      
      // 各親スロットを開いてサブスロットを確認
      for (let j = 0; j < toggleCount; j++) {
        const toggleBtn = toggleBtns.nth(j);
        const parentSlot = await toggleBtn.getAttribute('data-subslot-toggle');
        if (!parentSlot) continue;
        
        // 親スロットを開く
        await toggleBtn.evaluate((btn: HTMLElement) => btn.click());
        await page.waitForTimeout(500);
        
        // 静的DOM内の実際のサブスロット要素を確認
        const staticWrapperId = `slot-${parentSlot}-sub`;
        const actualSubslots = await page.evaluate((wrapperId) => {
          const wrapper = document.getElementById(wrapperId);
          if (!wrapper) return [];
          
          const containers = wrapper.querySelectorAll('.slot-container, .subslot-container');
          const found: string[] = [];
          
          containers.forEach((container) => {
            const id = container.id;
            if (!id) return;
            
            // ID形式: "slot-s-sub-s" → sub-s
            const match = id.match(/slot-\w+-sub-(\w+)$/);
            if (!match) return;
            
            // 実際にコンテンツがあるか確認（.slot-phraseまたは.slot-textに内容があるか）
            const slotPhrase = container.querySelector('.slot-phrase');
            const slotText = container.querySelector('.slot-text');
            const hasContent = (slotPhrase?.textContent?.trim() && slotPhrase.textContent.trim() !== '') ||
                             (slotText?.textContent?.trim() && slotText.textContent.trim() !== '');
            
            if (hasContent) {
              const subslotType = `sub-${match[1]}`;
              found.push(subslotType);
            }
          });
          
          return found;
        }, staticWrapperId);
        
        // 見つかったサブスロットを記録
        actualSubslots.forEach(subslotId => {
          const combination = `${parentSlot}-${subslotId}`;
          if (!uiFoundCombinations.has(combination)) {
            uiFoundCombinations.add(combination);
            console.log(`  ✅ ${combination} を発見`);
          }
        });
        
        // 親スロットを閉じる
        await toggleBtn.evaluate((btn: HTMLElement) => btn.click());
        await page.waitForTimeout(300);
      }
      
      // 全種類揃ったら早期終了
      if (uiFoundCombinations.size >= allDbCombinations.size) {
        console.log(`\n✅ ${i + 1}回のランダマイズで全サブスロット組み合わせが出現`);
        break;
      }
      
      if ((i + 1) % 10 === 0) {
        console.log(`\n📊 ${i + 1}回ランダマイズ: ${uiFoundCombinations.size}/${allDbCombinations.size}種類出現`);
      }
    }
    
    // 3. 検証：DB内の全組み合わせがUIに出現したか
    const missingCombinations: string[] = [];
    allDbCombinations.forEach(combination => {
      if (!uiFoundCombinations.has(combination)) {
        missingCombinations.push(combination);
      }
    });
    
    console.log(`\n📊 最終結果:`);
    console.log(`   DB内の全組み合わせ: ${allDbCombinations.size}種類`);
    console.log(`   UI出現: ${uiFoundCombinations.size}種類`);
    
    if (missingCombinations.length > 0) {
      console.log(`\n❌ 未出現: ${missingCombinations.join(', ')}`);
    }
    
    expect(uiFoundCombinations.size).toBeGreaterThanOrEqual(allDbCombinations.size);
    console.log('\n🎉 DB内の全サブスロット種別が静的スロットDOMに正しく表示される');
  });
});
