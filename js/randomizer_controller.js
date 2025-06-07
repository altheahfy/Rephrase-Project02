// randomizer_controller.js
// 必要ライブラリ: SheetJS (XLSX) を事前に読み込んでおくこと
// <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>

import { randomizeAll } from './randomizer_all.js';

/**
 * ユーザーがアップロードした grammar_data0001.xlsx ファイルを読み込んで、
 * 増殖①シートの中からランダムに1文を選び、構文スロットにマッピングして反映する
 */
export function handleExcelFileUpload(file) {
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

    // ランダムに1行選ぶ
    const randomRow = json[Math.floor(Math.random() * json.length)];

    // スロットへのマッピング（列名は実際のExcelに応じて調整）
    const slotData = {
      subject: randomRow['subject'] || '',
      auxiliary: randomRow['auxiliary'] || '',
      verb: randomRow['verb'] || '',
      object: randomRow['object'] || '',
      object_verb: randomRow['object_verb'] || '',
      complement: randomRow['complement'] || '',
      object2: randomRow['object2'] || '',
      complement2: randomRow['complement2'] || '',
      adverbial: randomRow['adverbial'] || '',
      adverbial2: randomRow['adverbial2'] || '',
      adverbial3: randomRow['adverbial3'] || '',

      sub_s: randomRow['sub_s'] || '',
      sub_aux: randomRow['sub_aux'] || '',
      sub_v: randomRow['sub_v'] || '',
      sub_o1: randomRow['sub_o1'] || '',
      sub_o2: randomRow['sub_o2'] || '',
      sub_c1: randomRow['sub_c1'] || '',
      sub_c2: randomRow['sub_c2'] || '',
      sub_m1: randomRow['sub_m1'] || '',
      sub_m2: randomRow['sub_m2'] || '',
      sub_m3: randomRow['sub_m3'] || '',
    };

    // 表示に反映
    randomizeAll(slotData);
  };
  reader.readAsArrayBuffer(file);
}
