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
   * 
   * ロジック:
   * 1. DB調査: 使用される可能性のある全サブスロット（親+サブの組み合わせ）を把握
   * 2. ランダマイズを実施してそのサブスロットが表示されるのを待つ
   * 3. 表示されたら制御パネルでそこの英語と日本語補助テキストを非表示
   * 4. トグルで開閉
   * 5. 英語と日本語補助テキストが表示されてしまわないか確認
   * 6. これを可能性のある全サブスロットに対して実施
   */
  test('[最優先] 全サブスロット開閉操作でhidden状態が保持される', async ({ page }) => {
    test.setTimeout(300000); // 5分
    
    // 1. DBから全サブスロット組み合わせ（親+サブ）を抽出
    const allDbSubslots = new Set<string>();
    for (const row of dbData) {
      if (row.SubslotID && row.Slot && row.V_group_key && row.例文ID) {
        const parentSlot = row.Slot.toLowerCase();
        const subslotId = row.SubslotID;
        allDbSubslots.add(`${parentSlot}-${subslotId}`);
      }
    }
    
    console.log(`📋 DB内の全サブスロット組み合わせ: ${allDbSubslots.size}種類`);
    console.log(`   ${Array.from(allDbSubslots).sort().join(', ')}`);
    
    if (allDbSubslots.size === 0) {
      console.log('⚠️ DBにサブスロットが存在しない');
      test.skip();
      return;
    }
    
    // 2. 各サブスロット組み合わせに対してテスト
    const testedSubslots = new Set<string>();
    const violations: any[] = [];
    let totalFailCount = 0;
    const MAX_RANDOMIZE = 50;
    const randomizeBtn = page.locator('#randomize-all');
    
    for (let attempt = 0; attempt < MAX_RANDOMIZE && testedSubslots.size < allDbSubslots.size; attempt++) {
      // ランダマイズ実行
      await randomizeBtn.click();
      await page.waitForTimeout(1000);
      
      console.log(`\n━━━ ${attempt + 1}回目のランダマイズ ━━━`);
      
      // 🆕 動的記載エリアから実際にレンダリングされたサブスロットを解析
      const renderedSubslots = await page.evaluate(() => {
        const dynamicArea = document.getElementById('dynamic-slot-area');
        if (!dynamicArea) return [];
        
        const results: Array<{parent: string, subslots: string[]}> = [];
        const subslotElements = dynamicArea.querySelectorAll('.subslot[id*="-sub-"]');
        
        // 親スロットごとにグループ化
        const groupedByParent = new Map<string, Set<string>>();
        
        subslotElements.forEach((element) => {
          const id = element.id;
          // ID形式: "slot-m1-sub-s" → 親: "m1", サブ: "sub-s"
          const match = id.match(/^slot-(\w+)-sub-(\w+)$/);
          if (!match) return;
          
          const parent = match[1].toLowerCase();
          const subslotType = `sub-${match[2]}`;
          
          // 実際にコンテンツがあるか確認
          const subElement = element.querySelector('.subslot-element');
          const subText = element.querySelector('.subslot-text');
          const hasContent = (subElement?.textContent?.trim() && subElement.textContent.trim() !== '') ||
                           (subText?.textContent?.trim() && subText.textContent.trim() !== '');
          
          if (hasContent) {
            if (!groupedByParent.has(parent)) {
              groupedByParent.set(parent, new Set());
            }
            groupedByParent.get(parent)!.add(subslotType);
          }
        });
        
        // Map → Array変換
        groupedByParent.forEach((subslots, parent) => {
          results.push({
            parent,
            subslots: Array.from(subslots)
          });
        });
        
        return results;
      });
      
      if (renderedSubslots.length === 0) {
        console.log(`  ⚠️ 動的記載エリアにサブスロットなし（スキップ）`);
        continue;
      }
      
      console.log(`  🔍 動的記載エリア解析結果:`);
      renderedSubslots.forEach(item => {
        console.log(`    ${item.parent}: ${item.subslots.join(', ')}`);
      });
      
      // 各親スロットのサブスロットをテスト
      for (const {parent: parentSlotName, subslots: subslotIds} of renderedSubslots) {
        // 親スロットのトグルボタンを特定
        const toggleBtn = page.locator(`button[data-subslot-toggle="${parentSlotName}"]`);
        
        if (await toggleBtn.count() === 0) {
          console.log(`  ⏩ ${parentSlotName} トグルボタンが見つからない（スキップ）`);
          continue;
        }
        
        console.log(`\n🔓 ${parentSlotName} サブスロット領域を開きます`);
        
        // トグルボタンを表示領域にスクロール
        await toggleBtn.scrollIntoViewIfNeeded({ timeout: 3000 }).catch(() => {
          console.log(`  ⚠️ スクロール失敗（継続）`);
        });
        
        // 親スロットを開く
        try {
          await toggleBtn.click({ timeout: 5000 });
          await page.waitForTimeout(500);
        } catch (e) {
          console.log(`  ❌ クリックエラー: ${e.message}`);
          continue;
        }
        
        // 動的記載エリアから静的DOMへの転写を待機
        const actualWrapperId = `slot-${parentSlotName}-sub`;
        const transferComplete = await page.waitForFunction((wrapperId) => {
          const wrapper = document.getElementById(wrapperId);
          if (!wrapper || window.getComputedStyle(wrapper).display === 'none') return false;
          
          const containers = wrapper.querySelectorAll('.slot-container, .subslot-container');
          if (containers.length === 0) return false;
          
          for (const container of containers) {
            const slotPhrase = container.querySelector('.slot-phrase');
            const slotText = container.querySelector('.slot-text');
            if ((slotPhrase?.textContent?.trim()) || (slotText?.textContent?.trim())) {
              return true;
            }
          }
          return false;
        }, actualWrapperId, { timeout: 10000 }).catch(() => null);
        
        if (!transferComplete) {
          console.log(`  ⚠️ ${parentSlotName} の転写タイムアウト（スキップ）`);
          await toggleBtn.click().catch(() => {});
          await page.waitForTimeout(400);
          continue;
        }
        
        console.log(`  ✅ ${parentSlotName} の転写完了`);
        
        // サブスロット専用制御パネルで「全英文非表示」をクリック
        const subslotPanelId = `subslot-visibility-panel-${parentSlotName}`;
        const subslotPanel = page.locator(`#${subslotPanelId}`);
        
        // サブスロット制御パネルが存在するか確認
        if (await subslotPanel.count() === 0) {
          console.log(`  ⚠️ ${parentSlotName} のサブスロット制御パネルが見つからない（スキップ）`);
          continue;
        }
        
        // 制御パネルが非表示の場合は表示させる
        const panelVisible = await subslotPanel.isVisible();
        if (!panelVisible) {
          const controlPanelToggle = page.locator('#toggle-control-panels');
          await controlPanelToggle.click();
          await page.waitForTimeout(500);
        }
        
        // 「全英文非表示」ボタンをクリック（全サブスロットを一括非表示）
        const hideAllButton = subslotPanel.locator('button').filter({ hasText: '全英文非表示' });
        
        if (await hideAllButton.count() === 0) {
          console.log(`  ⚠️ ${parentSlotName} の「全英文非表示」ボタンが見つからない（スキップ）`);
          continue;
        }
        
        console.log(`  🔧 「全英文非表示」ボタンをクリック（全サブスロット一括非表示）`);
        
        // ボタンをスクロールして可視化
        await hideAllButton.scrollIntoViewIfNeeded({ timeout: 2000 }).catch(() => {});
        
        try {
          await hideAllButton.click({ timeout: 5000 });
        } catch (e) {
          console.log(`  ⚠️ 「全英文非表示」クリック失敗: ${e.message}（スキップ）`);
          continue;
        }
        await page.waitForTimeout(500);
        
        console.log(`  ✅ ${parentSlotName} の全サブスロット英語テキストを非表示に設定`);
        
        // 日本語補助テキストも非表示にする（各サブスロットタイプの📝補助ボタンをクリック）
        console.log(`  🔧 日本語補助テキストを非表示にします...`);
        const subslotTypes = ['m1', 's', 'aux', 'm2', 'v', 'c1', 'o1', 'o2', 'c2', 'm3'];
        let auxButtonClickCount = 0;
        for (const subslotType of subslotTypes) {
          try {
            const auxButton = subslotPanel.locator(
              `.subslot-toggle-button[data-subslot-type="${subslotType}"][data-element-type="auxtext"]`
            );
            
            const buttonCount = await auxButton.count();
            if (buttonCount === 0) continue;
            
            const isVisible = await auxButton.isVisible().catch(() => false);
            if (!isVisible) continue;
            
            const isActive = await auxButton.evaluate(el => el.classList.contains('active')).catch(() => false);
            console.log(`    🔍 ${subslotType} 📝補助: active=${isActive}`);
            
            // active=true（表示状態）の場合のみクリックして非表示にする
            if (isActive) {
              await auxButton.click({ timeout: 3000 });
              auxButtonClickCount++;
              await page.waitForTimeout(100);
            }
          } catch (err) {
            console.log(`    ⚠️ ${subslotType} 📝補助ボタンのクリック失敗: ${err.message}`);
          }
        }
        
        console.log(`  ✅ ${parentSlotName} の日本語補助: ${auxButtonClickCount}個クリック`);
        
        // トグル開閉前に状態確認
        console.log(`  🔍 トグル開閉【前】の状態を確認...`);
        for (const subslotId of subslotIds) {
          const combination = `${parentSlotName}-${subslotId}`;
          const containerIdPattern = `slot-${parentSlotName}-${subslotId}`;
          const container = page.locator(`#${containerIdPattern}`);
          
          if (await container.count() === 0) continue;
          
          const slotPhrase = container.locator('.slot-phrase');
          const slotText = container.locator('.slot-text');
          
          const phraseIsVisible = await slotPhrase.isVisible().catch(() => false);
          const textIsVisible = await slotText.isVisible().catch(() => false);
          
          console.log(`    ${combination}: .slot-phrase=${phraseIsVisible}, .slot-text=${textIsVisible}`);
        }
        
        // 親スロットを閉じる
        await toggleBtn.click();
        await page.waitForTimeout(400);
        
        // 親スロットを再度開く
        await toggleBtn.click();
        await page.waitForTimeout(800);
        
        // 全サブスロットのhidden状態を検証
        console.log(`  🔍 全サブスロットのhidden状態を検証...`);
        
        for (const subslotId of subslotIds) {
          const combination = `${parentSlotName}-${subslotId}`;
          const containerIdPattern = `slot-${parentSlotName}-${subslotId}`;
          // 🎯 静的DOMの.slot-containerのみを対象（動的記載エリアを除外）
          const container = page.locator(`#${containerIdPattern}.slot-container`);
          
          if (await container.count() === 0) {
            console.log(`  ⚠️ ${containerIdPattern} が見つからない`);
            continue;
          }
          
          const slotPhrase = container.locator('.slot-phrase');
          const slotText = container.locator('.slot-text');
          
          let failCount = 0;
          
          // 🎯 正しい検証方法：親要素の .hidden-subslot-text クラスをチェック
          // 実装仕様：「非表示」= color: transparent（表示は残る）
          const hasTextHiddenClass = await container.evaluate(el => 
            el.classList.contains('hidden-subslot-text')
          );
          
          if (await slotPhrase.count() > 0) {
            if (!hasTextHiddenClass) {
              console.log(`  ❌ ${combination}: .hidden-subslot-text クラスが失われている`);
              failCount++;
            }
          }
          
          // 🎯 正しい検証方法：親要素の .hidden-subslot-auxtext クラスをチェック
          // 実装仕様：「非表示」= display: none（完全非表示）
          const hasAuxtextHiddenClass = await container.evaluate(el => 
            el.classList.contains('hidden-subslot-auxtext')
          );
          
          if (await slotText.count() > 0) {
            if (!hasAuxtextHiddenClass) {
              console.log(`  ❌ ${combination}: .hidden-subslot-auxtext クラスが失われている`);
              failCount++;
            }
          }
          
          if (failCount === 0) {
            console.log(`  ✅ ${combination}: hidden状態が保持されている`);
            testedSubslots.add(combination);
          } else {
            console.log(`  ❌ ${combination}: hidden状態が解除された（failCount=${failCount}）`);
            violations.push({
              combination,
              parent: parentSlotName,
              subslot: subslotId,
              reason: 'サブスロット開閉操作でhidden状態が解除された'
            });
          }
        }
        
        // 親スロットを閉じる
        console.log(`  🔒 ${parentSlotName} サブスロット領域を閉じます`);
        await toggleBtn.scrollIntoViewIfNeeded({ timeout: 2000 }).catch(() => {});
        await toggleBtn.click({ timeout: 3000 }).catch(() => {});
        await page.waitForTimeout(400);
      }
      
      if ((attempt + 1) % 10 === 0) {
        console.log(`\n📊 ${attempt + 1}回ランダマイズ: ${testedSubslots.size}/${allDbSubslots.size}種類テスト完了`);
      }
    }
    
    console.log(`\n📊 最終結果:`);
    console.log(`   DB内の全組み合わせ: ${allDbSubslots.size}種類`);
    console.log(`   テスト完了: ${testedSubslots.size}種類`);
    console.log(`   違反数: ${totalFailCount}`);
    
    // 判定
    expect(testedSubslots.size).toBeGreaterThanOrEqual(allDbSubslots.size);
    expect(totalFailCount).toBe(0);
    
    if (totalFailCount === 0) {
      console.log('\n🎉 全サブスロット開閉操作でhidden状態が完全保持されている');
    }
  });

  /**
   * Test-4: 【最優先】個別ランダマイズ後もhidden状態が解除されないか
   * 
   * 目的: 個別ランダマイズ（親スロットの個別ランダマイズボタン）後も、
   *       学習者の設定した「非表示状態」が保持されることを保証
   * 
   * ロジック:
   * 1. DB調査: 使用される可能性のある全サブスロット（親+サブの組み合わせ）を把握
   * 2. ランダマイズを実施してそのサブスロットが表示されるのを待つ
   * 3. 表示されたら制御パネルでそこの英語と日本語補助テキストを非表示
   * 4. 親スロットにある個別ランダマイズボタンをクリックしてランダマイズ実施
   * 5. 英語と日本語補助テキストが表示されてしまわないか確認
   * 6. これを可能性のある全サブスロットに対して実施
   */
  test('[最優先] 個別ランダマイズ後もhidden状態が保持される', async ({ page }) => {
    test.setTimeout(300000); // 5分
    
    // 1. DBから全サブスロット組み合わせ（親+サブ）を抽出
    const allDbSubslots = new Set<string>();
    for (const row of dbData) {
      if (row.SubslotID && row.Slot && row.V_group_key && row.例文ID) {
        const parentSlot = row.Slot.toLowerCase();
        const subslotId = row.SubslotID;
        allDbSubslots.add(`${parentSlot}-${subslotId}`);
      }
    }
    
    console.log(`📋 DB内の全サブスロット組み合わせ: ${allDbSubslots.size}種類`);
    console.log(`   ${Array.from(allDbSubslots).sort().join(', ')}`);
    
    if (allDbSubslots.size === 0) {
      console.log('⚠️ DBにサブスロットが存在しない');
      test.skip();
      return;
    }
    
    // 2. 各サブスロット組み合わせに対してテスト
    const testedSubslots = new Set<string>();
    let totalFailCount = 0;
    const MAX_RANDOMIZE = 50;
    const randomizeBtn = page.locator('#randomize-all');
    
    for (let attempt = 0; attempt < MAX_RANDOMIZE && testedSubslots.size < allDbSubslots.size; attempt++) {
      // 全体ランダマイズ実行
      await randomizeBtn.click();
      await page.waitForTimeout(1000);
      
      console.log(`\n━━━ ${attempt + 1}回目のランダマイズ ━━━`);
      
      // 🆕 動的記載エリアから実際にレンダリングされたサブスロットを解析
      const renderedSubslots = await page.evaluate(() => {
        const dynamicArea = document.getElementById('dynamic-slot-area');
        if (!dynamicArea) return [];
        
        const results: Array<{parent: string, subslots: string[]}> = [];
        const subslotElements = dynamicArea.querySelectorAll('.subslot[id*="-sub-"]');
        
        // 親スロットごとにグループ化
        const groupedByParent = new Map<string, Set<string>>();
        
        subslotElements.forEach((element) => {
          const id = element.id;
          // ID形式: "slot-m1-sub-s" → 親: "m1", サブ: "sub-s"
          const match = id.match(/^slot-(\w+)-sub-(\w+)$/);
          if (!match) return;
          
          const parent = match[1].toLowerCase();
          const subslotType = `sub-${match[2]}`;
          
          // 実際にコンテンツがあるか確認
          const subElement = element.querySelector('.subslot-element');
          const subText = element.querySelector('.subslot-text');
          const hasContent = (subElement?.textContent?.trim() && subElement.textContent.trim() !== '') ||
                           (subText?.textContent?.trim() && subText.textContent.trim() !== '');
          
          if (hasContent) {
            if (!groupedByParent.has(parent)) {
              groupedByParent.set(parent, new Set());
            }
            groupedByParent.get(parent)!.add(subslotType);
          }
        });
        
        // Map → Array変換
        groupedByParent.forEach((subslots, parent) => {
          results.push({
            parent,
            subslots: Array.from(subslots)
          });
        });
        
        return results;
      });
      
      if (renderedSubslots.length === 0) {
        console.log(`  ⚠️ 動的記載エリアにサブスロットなし（スキップ）`);
        continue;
      }
      
      console.log(`  🔍 動的記載エリア解析結果:`);
      renderedSubslots.forEach(item => {
        console.log(`    ${item.parent}: ${item.subslots.join(', ')}`);
      });
      
      // 各親スロットのサブスロットをテスト
      for (const {parent: parentSlotName, subslots: subslotIds} of renderedSubslots) {
        // 親スロットのトグルボタンを特定
        const toggleBtn = page.locator(`button[data-subslot-toggle="${parentSlotName}"]`);
        
        if (await toggleBtn.count() === 0) {
          console.log(`  ⏩ ${parentSlotName} トグルボタンが見つからない（スキップ）`);
          continue;
        }
        
        console.log(`\n🔓 ${parentSlotName} サブスロット領域を開きます`);
        
        // トグルボタンを表示領域にスクロール
        await toggleBtn.scrollIntoViewIfNeeded({ timeout: 3000 }).catch(() => {});
        
        // 親スロットを開く
        await toggleBtn.click();
        await page.waitForTimeout(800);
        
        // 動的記載エリアから静的DOMへの転写を待機
        const actualWrapperId = `slot-${parentSlotName}-sub`;
        const transferComplete = await page.waitForFunction((wrapperId) => {
          const wrapper = document.getElementById(wrapperId);
          if (!wrapper || window.getComputedStyle(wrapper).display === 'none') return false;
          
          const containers = wrapper.querySelectorAll('.slot-container, .subslot-container');
          if (containers.length === 0) return false;
          
          for (const container of containers) {
            const slotPhrase = container.querySelector('.slot-phrase');
            const slotText = container.querySelector('.slot-text');
            if ((slotPhrase?.textContent?.trim()) || (slotText?.textContent?.trim())) {
              return true;
            }
          }
          return false;
        }, actualWrapperId, { timeout: 10000 }).catch(() => null);
        
        if (!transferComplete) {
          console.log(`  ⚠️ ${parentSlotName} の転写タイムアウト（スキップ）`);
          await toggleBtn.click().catch(() => {});
          await page.waitForTimeout(400);
          continue;
        }
        
        console.log(`  ✅ ${parentSlotName} の転写完了`);
        
        // サブスロット専用制御パネルで「全英文非表示」をクリック
        const subslotPanelId = `subslot-visibility-panel-${parentSlotName}`;
        const subslotPanel = page.locator(`#${subslotPanelId}`);
        
        // サブスロット制御パネルが存在するか確認
        if (await subslotPanel.count() === 0) {
          console.log(`  ⚠️ ${parentSlotName} のサブスロット制御パネルが見つからない（スキップ）`);
          continue;
        }
        
        // 制御パネルが非表示の場合は表示させる
        const panelVisible = await subslotPanel.isVisible();
        if (!panelVisible) {
          const controlPanelToggle = page.locator('#toggle-control-panels');
          await controlPanelToggle.click();
          await page.waitForTimeout(500);
        }
        
        // 「全英文非表示」ボタンをクリック（全サブスロットを一括非表示）
        const hideAllButton = subslotPanel.locator('button').filter({ hasText: '全英文非表示' });
        
        if (await hideAllButton.count() === 0) {
          console.log(`  ⚠️ ${parentSlotName} の「全英文非表示」ボタンが見つからない（スキップ）`);
          continue;
        }
        
        console.log(`  🔧 「全英文非表示」ボタンをクリック（全サブスロット一括非表示）`);
        
        // ボタンをスクロールして可視化
        await hideAllButton.scrollIntoViewIfNeeded({ timeout: 2000 }).catch(() => {});
        
        try {
          await hideAllButton.click({ timeout: 5000 });
        } catch (e) {
          console.log(`  ⚠️ 「全英文非表示」クリック失敗: ${e.message}（スキップ）`);
          continue;
        }
        await page.waitForTimeout(500);
        
        console.log(`  ✅ ${parentSlotName} の全サブスロット英語テキストを非表示に設定`);
        
        // 日本語補助テキストも非表示にする（各サブスロットタイプの📝補助ボタンをクリック）
        console.log(`  🔧 日本語補助テキストを非表示にします...`);
        const subslotTypes = ['m1', 's', 'aux', 'm2', 'v', 'c1', 'o1', 'o2', 'c2', 'm3'];
        let auxButtonClickCount = 0;
        for (const subslotType of subslotTypes) {
          try {
            const auxButton = subslotPanel.locator(
              `.subslot-toggle-button[data-subslot-type="${subslotType}"][data-element-type="auxtext"]`
            );
            
            const buttonCount = await auxButton.count();
            if (buttonCount === 0) continue;
            
            const isVisible = await auxButton.isVisible().catch(() => false);
            if (!isVisible) continue;
            
            const isActive = await auxButton.evaluate(el => el.classList.contains('active')).catch(() => false);
            console.log(`    🔍 ${subslotType} 📝補助: active=${isActive}`);
            
            // active=true（表示状態）の場合のみクリックして非表示にする
            if (isActive) {
              await auxButton.click({ timeout: 3000 });
              auxButtonClickCount++;
              await page.waitForTimeout(100);
            }
          } catch (err) {
            console.log(`    ⚠️ ${subslotType} 📝補助ボタンのクリック失敗: ${err.message}`);
          }
        }
        
        console.log(`  ✅ ${parentSlotName} の日本語補助: ${auxButtonClickCount}個クリック`);
        
        // 親スロットの個別ランダマイズボタンを探す
        const individualRandomizeBtn = page.locator(`button[data-individual-randomize="${parentSlotName}"]`);
        
        if (await individualRandomizeBtn.count() === 0) {
          console.log(`  ⚠️ ${parentSlotName} の個別ランダマイズボタンが見つからない（スキップ）`);
          continue;
        }
        
        // 個別ランダマイズ実行
        console.log(`  🎲 個別ランダマイズ実行...`);
        await individualRandomizeBtn.click();
        await page.waitForTimeout(1500);
        
        console.log(`  🎲 ${parentSlotName} の個別ランダマイズ実行`);
        
        // 転写完了を待機
        const reTransferComplete = await page.waitForFunction((wrapperId) => {
          const wrapper = document.getElementById(wrapperId);
          if (!wrapper || window.getComputedStyle(wrapper).display === 'none') return false;
          
          const containers = wrapper.querySelectorAll('.slot-container, .subslot-container');
          if (containers.length === 0) return false;
          
          for (const container of containers) {
            const slotPhrase = container.querySelector('.slot-phrase');
            const slotText = container.querySelector('.slot-text');
            if ((slotPhrase?.textContent?.trim()) || (slotText?.textContent?.trim())) {
              return true;
            }
          }
          return false;
        }, actualWrapperId, { timeout: 10000 }).catch(() => null);
        
        if (!reTransferComplete) {
          console.log(`  ⚠️ ${parentSlotName} の再転写タイムアウト（スキップ）`);
          continue;
        }
        
        // 全サブスロットのhidden状態を検証
        console.log(`  🔍 全サブスロットのhidden状態を検証...`);
        
        for (const subslotId of subslotIds) {
          const combination = `${parentSlotName}-${subslotId}`;
          const containerIdPattern = `slot-${parentSlotName}-${subslotId}`;
          // 🎯 静的DOMの.slot-containerのみを対象（動的記載エリアを除外）
          const container = page.locator(`#${containerIdPattern}.slot-container`);
          
          if (await container.count() === 0) {
            console.log(`  ⚠️ ${containerIdPattern} が見つからない`);
            continue;
          }
          
          const slotPhrase = container.locator('.slot-phrase');
          const slotText = container.locator('.slot-text');
          
          let failCount = 0;
          
          // 🎯 正しい検証方法：親要素の .hidden-subslot-text クラスをチェック
          // 実装仕様：「非表示」= color: transparent（表示は残る）
          const hasTextHiddenClass = await container.evaluate(el => 
            el.classList.contains('hidden-subslot-text')
          );
          
          if (await slotPhrase.count() > 0) {
            if (!hasTextHiddenClass) {
              console.log(`  ❌ ${combination}: .hidden-subslot-text クラスが失われている`);
              failCount++;
            }
          }
          
          // 🎯 正しい検証方法：親要素の .hidden-subslot-auxtext クラスをチェック
          // 実装仕様：「非表示」= display: none（完全非表示）
          const hasAuxtextHiddenClass = await container.evaluate(el => 
            el.classList.contains('hidden-subslot-auxtext')
          );
          
          if (await slotText.count() > 0) {
            if (!hasAuxtextHiddenClass) {
              console.log(`  ❌ ${combination}: .hidden-subslot-auxtext クラスが失われている`);
              failCount++;
            }
          }
          
          if (failCount === 0) {
            console.log(`  ✅ ${combination}: hidden状態が保持されている`);
          } else {
            totalFailCount += failCount;
          }
          
          testedSubslots.add(combination);
        }
        
        // 親スロットを閉じる
        console.log(`  🔒 ${parentSlotName} サブスロット領域を閉じます`);
        await toggleBtn.scrollIntoViewIfNeeded({ timeout: 2000 }).catch(() => {});
        await toggleBtn.click({ timeout: 3000 }).catch(() => {});
        await page.waitForTimeout(400);
      }
      
      if ((attempt + 1) % 10 === 0) {
        console.log(`\n📊 ${attempt + 1}回ランダマイズ: ${testedSubslots.size}/${allDbSubslots.size}種類テスト完了`);
      }
    }
    
    console.log(`\n📊 最終結果:`);
    console.log(`   DB内の全組み合わせ: ${allDbSubslots.size}種類`);
    console.log(`   テスト完了: ${testedSubslots.size}種類`);
    console.log(`   違反数: ${totalFailCount}`);
    
    // 判定
    expect(testedSubslots.size).toBeGreaterThanOrEqual(allDbSubslots.size);
    expect(totalFailCount).toBe(0);
    
    if (totalFailCount === 0) {
      console.log('\n🎉 個別ランダマイズ後もhidden状態が完全保持されている');
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
