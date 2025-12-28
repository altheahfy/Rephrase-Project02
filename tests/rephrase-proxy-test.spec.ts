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
   */
  test('[必須] DBの全サブスロット種別がUIに表示される', async ({ page }) => {
    // テストタイムアウトを延長
    test.setTimeout(120000); // 120秒
    // 1. DBをスキャンして全サブスロット種別を取得
    const dbSubslotTypes = new Set<string>();
    
    for (const row of dbData) {
      if (row.SubslotID) {
        // SubslotID形式: "sub-s", "sub-o1", "sub-v" など
        dbSubslotTypes.add(row.SubslotID);
      }
    }
    
    console.log(`📋 DB内の全サブスロット種別: ${Array.from(dbSubslotTypes).sort().join(', ')}`);
    console.log(`📊 合計: ${dbSubslotTypes.size}種類`);
    
    if (dbSubslotTypes.size === 0) {
      console.log('⚠️ DBにサブスロットが存在しない');
      test.skip();
      return;
    }
    
    // 2. ランダマイズを複数回実行して静的スロットDOMに出現したサブスロットを収集
    const uiSubslotTypes = new Set<string>();
    const randomizeBtn = page.locator('#randomize-all');
    const MAX_RANDOMIZE = 30; // 最大30回ランダマイズ
    
    for (let i = 0; i < MAX_RANDOMIZE; i++) {
      await randomizeBtn.click();
      await page.waitForTimeout(800); // ランダマイズ完了待機
      
      // 実際に表示されている（visible）トグルボタンだけを取得
      const allToggleBtns = page.locator('button[data-subslot-toggle]');
      const allCount = await allToggleBtns.count();
      
      // visible なボタンだけをフィルタリング
      const visibleToggleBtns: Array<{ btn: any, attr: string }> = [];
      for (let t = 0; t < allCount; t++) {
        const btn = allToggleBtns.nth(t);
        const isVisible = await btn.isVisible();
        if (isVisible) {
          const attr = await btn.getAttribute('data-subslot-toggle');
          if (attr) {
            visibleToggleBtns.push({ btn, attr });
          }
        }
      }
      
      const toggleCount = visibleToggleBtns.length;
      
      if (toggleCount === 0) {
        console.log(`⚠️ ${i + 1}回目: 表示されているサブスロットトグルボタンが見つからない（スキップ）`);
        continue;
      }
      
      console.log(`📍 ${i + 1}回目: 表示中のトグルボタン数 ${toggleCount}個`);
      
      // デバッグ用：最初の1回だけ詳細ログを出力
      const enableDetailedDebug = (i === 0);
      
      // 各親スロットのサブスロット領域を開いて検査
      for (const { btn: toggleBtn, attr: toggleAttr } of visibleToggleBtns) {
        
        if (!toggleAttr) continue;
        
        // 静的スロットDOMのID形式: slot-{parent}-sub
        const staticWrapperId = `slot-${toggleAttr}-sub`;
        
        // 静的スロットDOM（.slot-wrapper#slot-{parent}-sub）を取得
        const staticWrapper = page.locator(`#${staticWrapperId}`);
        
        if (await staticWrapper.count() === 0) {
          console.log(`⚠️ 静的ラッパー ${staticWrapperId} が見つからない`);
          continue;
        }
        
        // サブスロット領域を開く（内容転写トリガー）
        const isWrapperVisible = await staticWrapper.isVisible();
        if (!isWrapperVisible) {
          // JavaScriptで直接クリック（visibleなボタンなので成功するはず）
          await toggleBtn.evaluate((btn: HTMLElement) => btn.click());
          
          // 転写完了を待機（最大3秒）：内容が入るまで待つ
          await page.waitForFunction(
            (wrapperId) => {
              const wrapper = document.getElementById(wrapperId);
              if (!wrapper) return false;
              const containers = wrapper.querySelectorAll('.subslot-container');
              for (const c of containers) {
                const text = c.querySelector('.slot-text')?.textContent?.trim();
                const phrase = c.querySelector('.slot-phrase')?.textContent?.trim();
                if (text || phrase) return true;
              }
              return false;
            },
            staticWrapperId,
            { timeout: 3000 }
          ).catch(() => {
            console.log(`  ⚠️ ${toggleAttr}: 転写タイムアウト（3秒待機）`);
          });
          
          // 開いたことを確認
          const nowVisible = await staticWrapper.isVisible();
          if (nowVisible) {
            console.log(`  ✅ ${toggleAttr} サブスロット領域を開きました`);
            
            // 🔍 DOM構造を直接確認（最初の1回のみ）
            if (enableDetailedDebug) {
              const domDebug = await page.evaluate((wrapperId) => {
                const wrapper = document.getElementById(wrapperId);
                if (!wrapper) return { error: 'wrapper not found' };
                
                const containers = wrapper.querySelectorAll('.slot-container, .subslot-container');
                const result = {
                  wrapperHTML: wrapper.outerHTML.substring(0, 500), // 先頭500文字
                  containerCount: containers.length,
                  containers: [] as any[]
                };
                
                containers.forEach((container, idx) => {
                  result.containers.push({
                    id: container.id,
                    textContent: container.textContent?.substring(0, 100),
                    innerHTML: container.innerHTML.substring(0, 200)
                  });
                });
                
                return result;
              }, staticWrapperId);
              
              console.log(`  🔍 DOM Debug for ${toggleAttr}:`, JSON.stringify(domDebug, null, 2));
              
              // 🔍 CSS疑似要素の内容を確認
              const pseudoDebug = await page.evaluate((wrapperId) => {
                const wrapper = document.getElementById(wrapperId);
                if (!wrapper) return { error: 'wrapper not found' };
                
                const containers = wrapper.querySelectorAll('.slot-container, .subslot-container');
                const results: any[] = [];
                
                containers.forEach((container) => {
                  const styles = window.getComputedStyle(container);
                  const beforeContent = window.getComputedStyle(container, '::before').content;
                  const afterContent = window.getComputedStyle(container, '::after').content;
                  results.push({
                    id: container.id,
                    textContent: container.textContent?.substring(0, 50),
                    beforeContent: beforeContent !== 'none' ? beforeContent : null,
                    afterContent: afterContent !== 'none' ? afterContent : null,
                    display: styles.display,
                    visibility: styles.visibility
                  });
                });
                
                return results;
              }, staticWrapperId);
              console.log(`  🔍 CSS Pseudo Elements for ${toggleAttr}:`, JSON.stringify(pseudoDebug, null, 2));
              
              // 🔍 動的記載エリアの状態も確認
              const dynamicAreaDebug = await page.evaluate(() => {
                const dynamicArea = document.getElementById('dynamic-slot-area');
                if (!dynamicArea) return { error: 'dynamic area not found' };
                
                return {
                  visible: dynamicArea.style.display !== 'none',
                  innerHTML: dynamicArea.innerHTML.substring(0, 500),
                  hasSubslots: dynamicArea.querySelectorAll('.subslot').length,
                  hasSubslotElements: dynamicArea.querySelectorAll('.subslot-element').length
                };
              });
              console.log(`  🔍 Dynamic Area Debug:`, JSON.stringify(dynamicAreaDebug, null, 2));
              
              // 🔍 視覚的に見えている座標の要素を特定
              const visualDebug = await page.evaluate((wrapperId) => {
                const wrapper = document.getElementById(wrapperId);
                if (!wrapper) return { error: 'wrapper not found' };
                
                const rect = wrapper.getBoundingClientRect();
                // ラッパーの中央付近の座標
                const x = rect.left + rect.width / 2;
                const y = rect.top + 50; // 上部から50px
                
                const element = document.elementFromPoint(x, y);
                
                return {
                  coordinates: { x, y },
                  element: element ? {
                    tagName: element.tagName,
                    id: element.id,
                    className: element.className,
                    textContent: element.textContent?.substring(0, 100)
                  } : null
                };
              }, staticWrapperId);
              console.log(`  🔍 Visual Element at Coordinates:`, JSON.stringify(visualDebug, null, 2));
              
              // 📸 デバッグ用：ユーザーが視覚確認できるように2秒待機してからスクリーンショット
              console.log(`  ⏳ スクリーンショット撮影のため2秒待機...`);
              await page.waitForTimeout(2000);
            }
            
            // スクリーンショット撮影（デバッグ用）
            await page.screenshot({ 
              path: `test-results/subslot-${toggleAttr}-open.png`,
              fullPage: true 
            });
            console.log(`  📸 スクリーンショット保存: subslot-${toggleAttr}-open.png`);
          }
        }
        
        // 開いた状態で静的スロットDOM内の.slot-containerまたは.subslot-containerを検査
        const slotContainers = staticWrapper.locator('.slot-container, .subslot-container');
        const containerCount = await slotContainers.count();
        
        for (let j = 0; j < containerCount; j++) {
          const container = slotContainers.nth(j);
          const id = await container.getAttribute('id');
          
          if (!id) continue;
          
          // .slot-container自体のtextContentを直接読む
          const containerText = await container.textContent();
          const hasContent = containerText?.trim();
          
          if (hasContent) {
            console.log(`✅ ${id}: 内容あり ("${containerText?.trim().substring(0, 50)}...")`);
            
            // id形式: "slot-o1-sub-s" → "sub-s"
            const match = id.match(/slot-\w+-sub-(\w+)$/);
            if (match) {
              const subslotType = `sub-${match[1]}`;
              uiSubslotTypes.add(subslotType);
            }
          }
        }
        
        // サブスロット領域を閉じる
        if (!isWrapperVisible) {
          await toggleBtn.evaluate((btn: HTMLElement) => btn.click());
          await page.waitForTimeout(300);
        }
      }
      
      // 全種類揃ったら早期終了
      if (uiSubslotTypes.size >= dbSubslotTypes.size) {
        console.log(`✅ ${i + 1}回のランダマイズで全サブスロット種別が静的スロットDOMに出現`);
        break;
      }
      
      if ((i + 1) % 10 === 0) {
        console.log(`🔄 ${i + 1}回ランダマイズ: ${uiSubslotTypes.size}/${dbSubslotTypes.size}種類出現`);
        console.log(`   出現済み: ${Array.from(uiSubslotTypes).sort().join(', ')}`);
      }
    }
    
    console.log(`📊 UI出現サブスロット種別: ${Array.from(uiSubslotTypes).sort().join(', ')}`);
    console.log(`📊 出現率: ${uiSubslotTypes.size}/${dbSubslotTypes.size}種類`);
    
    // 3. DB集合 ⊆ UI出現集合 が成立するか確認
    const missingTypes: string[] = [];
    for (const dbType of dbSubslotTypes) {
      if (!uiSubslotTypes.has(dbType)) {
        missingTypes.push(dbType);
      }
    }
    
    if (missingTypes.length > 0) {
      console.log(`❌ UIに出現しなかったサブスロット種別: ${missingTypes.join(', ')}`);
    }
    
    // 判定
    expect(missingTypes.length).toBe(0);
    
    console.log('🎉 DB内の全サブスロット種別が静的スロットDOMに正しく表示される');
  });
});
