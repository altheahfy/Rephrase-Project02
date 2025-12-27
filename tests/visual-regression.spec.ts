import { test, expect } from '@playwright/test';

/**
 * B. Visual Regression テスト - UI見た目の変化検出
 * 
 * 検証項目:
 * 1. 初期表示レイアウトが基準画像と一致するか（5%誤差許容）
 * 2. 制御パネル表示が正しいか
 * 3. スロット配置・サイズが変わっていないか
 * 4. イラスト表示が正しいか
 * 5. スマホ表示が崩れていないか（将来）
 * 
 * 基準画像: tests/snapshots/*.png
 * 差分画像: test-results/*.png（失敗時のみ）
 */

test.describe('B. Visual Regression - RephraseUI', () => {
  
  test.beforeEach(async ({ page }) => {
    // ページを開く（認証スキップ）
    await page.goto('/training/index.html?skipAuth=true');
    await page.waitForLoadState('networkidle');
    console.log('✓ ページロード完了');
    
    // データ選択プルダウンからメインデータを選択
    await page.selectOption('#presetSelect', 'data/slot_order_data.json');
    await page.click('#loadPresetButton');
    console.log('✓ データ読込ボタンクリック完了');
    
    // スロットが表示されるまで明示的に待機（10秒タイムアウト）
    await page.waitForSelector('.slot-container', { timeout: 10000 });
    await page.waitForTimeout(2000); // 追加の安定化待機
    
    const slotCount = await page.locator('.slot-container').count();
    console.log(`✓ ${slotCount}個のスロット検出`);
  });

  test('Test-1: 初期表示レイアウト（全画面）', async ({ page }) => {
    // 画面全体のスクリーンショット
    await expect(page).toHaveScreenshot('initial-full-layout.png', {
      fullPage: true,
      animations: 'disabled', // アニメーション無効化
    });
    
    console.log('✓ 初期表示レイアウト検証完了');
  });

  test('Test-2: スロット表示エリアのみ', async ({ page }) => {
    // スロット表示エリアだけを撮影
    const slotsArea = page.locator('#upper-slots-area');
    
    if (await slotsArea.count() > 0) {
      await expect(slotsArea).toHaveScreenshot('slots-area-layout.png', {
        animations: 'disabled',
      });
      console.log('✓ スロット表示エリア検証完了');
    } else {
      console.log('⚠ スロット表示エリアが見つからない');
    }
  });

  test('Test-3: 制御パネル表示', async ({ page }) => {
    // 制御パネルを撮影
    const controlPanel = page.locator('#control-panel, .control-panel');
    
    if (await controlPanel.count() > 0) {
      await expect(controlPanel).toHaveScreenshot('control-panel-layout.png', {
        animations: 'disabled',
      });
      console.log('✓ 制御パネル表示検証完了');
    } else {
      console.log('⚠ 制御パネルが見つからない');
    }
  });

  test('Test-4: ランダマイズ後のレイアウト', async ({ page }) => {
    // ランダマイズボタンをクリック
    const randomizeButton = page.locator('#randomize-all-button, button:has-text("全体ランダマイズ")');
    
    if (await randomizeButton.count() > 0) {
      await randomizeButton.click();
      await page.waitForTimeout(2000); // ランダマイズ完了・イラスト再読込待ち
      
      // ランダマイズ後の全画面
      await expect(page).toHaveScreenshot('after-randomize-full-layout.png', {
        fullPage: true,
        animations: 'disabled',
      });
      console.log('✓ ランダマイズ後レイアウト検証完了');
    } else {
      console.log('⚠ ランダマイズボタンが見つからない');
    }
  });

  test('Test-5: サブスロット展開状態', async ({ page }) => {
    // サブスロットトグルボタンを探す
    const toggleButton = page.locator('.subslot-toggle, .toggle-button').first();
    
    if (await toggleButton.count() > 0) {
      // 展開状態をスクリーンショット
      const slotsArea = page.locator('#upper-slots-area');
      await expect(slotsArea).toHaveScreenshot('subslot-expanded-layout.png', {
        animations: 'disabled',
      });
      
      // 折りたたみ状態をスクリーンショット
      await toggleButton.click();
      await page.waitForTimeout(500);
      
      await expect(slotsArea).toHaveScreenshot('subslot-collapsed-layout.png', {
        animations: 'disabled',
      });
      
      console.log('✓ サブスロット展開/折りたたみ検証完了');
    } else {
      console.log('⚠ サブスロットトグルボタンが見つからない');
    }
  });

  test('Test-6: 制御パネル操作後のレイアウト', async ({ page }) => {
    // V スロットを非表示にする
    const controlPanel = page.locator('#control-panel, .control-panel');
    
    if (await controlPanel.count() > 0) {
      const hideVButton = controlPanel.locator('button:has-text("V"), input[value="V"]').first();
      
      if (await hideVButton.count() > 0) {
        await hideVButton.click();
        await page.waitForTimeout(500);
        
        // 非表示後のレイアウト
        const slotsArea = page.locator('#upper-slots-area');
        await expect(slotsArea).toHaveScreenshot('slots-v-hidden-layout.png', {
          animations: 'disabled',
        });
        
        console.log('✓ 制御パネル操作後レイアウト検証完了');
      }
    }
  });

  test.skip('Test-7: スマホ表示（将来実装）', async ({ page }) => {
    // スマホサイズに変更
    await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
    await page.waitForTimeout(1000);
    
    await expect(page).toHaveScreenshot('mobile-layout.png', {
      fullPage: true,
      animations: 'disabled',
    });
    
    console.log('✓ スマホ表示検証完了');
  });
});
