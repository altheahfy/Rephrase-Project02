
// randomizer_controller.js（グローバル関数対応 + セキュリティ強化）
import { randomizeAll } from './randomizer_all.js';
import { validateFileUpload, escapeHtml } from './security.js';

export function handleExcelFileUpload(file) {
  // 🔒 ファイルアップロードのセキュリティ検証
  const validation = validateFileUpload(file);
  if (!validation.valid) {
    const errorMsg = '🔒 セキュリティエラー:\n' + validation.errors.join('\n');
    alert(errorMsg);
    console.error('🔒 ファイルアップロード拒否:', validation.errors);
    return;
  }
  
  console.log('🔒 ファイルアップロード検証 OK:', file.name);
  
  const reader = new FileReader();
  reader.onload = function (e) {
    const data = new Uint8Array(e.target.result);
    const workbook = XLSX.read(data, { type: 'array' });
    const sheet = workbook.Sheets['増殖①'];
    if (!sheet) {
      alert('シート「増殖①」が見つかりません');
      return;
    }
    const json = XLSX.utils.sheet_to_json(sheet);

    const allIds = [...new Set(json.map(row => String(row['文法項目番号']).trim()))];
    const chosenId = allIds[Math.floor(Math.random() * allIds.length)];
    const targetRows = json.filter(row => String(row['文法項目番号']).trim() === chosenId);
    if (targetRows.length === 0) {
      console.warn('⚠️ 対象文法項目が見つかりません:', chosenId);
      return;
    }

    const slotData = {};
    for (const row of targetRows) {
      const internal = row['構文要素ID'];
      const value = row['表示テキスト'];

      // CCDD診断ログ: フィールド存在チェック
      if (!row.hasOwnProperty('構文要素ID')) {
        console.warn('🛑 構文要素ID 列が存在しません:', row);
      }
      if (!row.hasOwnProperty('表示テキスト')) {
        console.warn('🛑 表示テキスト 列が存在しません:', row);
      }

      // CCDD診断ログ: 値未設定チェック
      if (!internal) {
        console.warn('⚠️ 構文要素IDが空です:', row);
        continue;
      }
      if (!value) {
        console.warn(`⚠️ "${internal}" に対応する 表示テキスト が空または未定義です`);
        continue;
      }

      // 🔒 入力値のサニタイゼーション
      const safeInternal = escapeHtml(String(internal).trim());
      const safeValue = escapeHtml(String(value).trim());

      let slotId = '';
      if (safeInternal.startsWith('sub_')) {
        slotId = `slot-o1-sub-${safeInternal.replace('sub_', '')}`;
      } else {
        slotId = `slot-${safeInternal}`;
      }
      
      // 🔒 安全な値をスロットデータに格納
      slotData[slotId] = safeValue;
    }

    console.log('📘 構文スロットデータ:', slotData);
    console.log('🔒 データ処理完了（セキュリティチェック済み）');
    randomizeAll(slotData);
  };
  reader.readAsArrayBuffer(file);
}

// グローバル登録
window.handleExcelFileUpload = handleExcelFileUpload;
