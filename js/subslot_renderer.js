// subslot_renderer_dev.js
window.addEventListener("DOMContentLoaded", () => {
  const slotIds = [
    "slot-o1-sub-m1", "slot-o1-sub-s", "slot-o1-sub-aux", "slot-o1-sub-m2",
    "slot-o1-sub-v", "slot-o1-sub-c", "slot-o1-sub-o1", "slot-o1-sub-o2",
    "slot-o1-sub-c2", "slot-o1-sub-m3",

    "slot-o2-sub-m1", "slot-o2-sub-s", "slot-o2-sub-aux", "slot-o2-sub-m2",
    "slot-o2-sub-v", "slot-o2-sub-c", "slot-o2-sub-o1", "slot-o2-sub-o2",
    "slot-o2-sub-c2", "slot-o2-sub-m3",

    "slot-c-sub-m1", "slot-c-sub-s", "slot-c-sub-aux", "slot-c-sub-m2",
    "slot-c-sub-v", "slot-c-sub-c", "slot-c-sub-o1", "slot-c-sub-o2",
    "slot-c-sub-c2", "slot-c-sub-m3",

    // C1サブスロット追加
    "slot-c1-sub-m1", "slot-c1-sub-s", "slot-c1-sub-aux", "slot-c1-sub-m2",
    "slot-c1-sub-v", "slot-c1-sub-c1", "slot-c1-sub-o1", "slot-c1-sub-o2",
    "slot-c1-sub-c2", "slot-c1-sub-m3"
  ];

  slotIds.forEach(id => {
    const img = document.querySelector(`#${id} img`);
    if (img) {
      // 🚫 C1サブスロットの画像は保護（applyImageToSubslotで管理されるため）
      if (id.startsWith('slot-c1-sub-') && img.hasAttribute('data-meta-tag')) {
        console.log(`🛡️ C1サブスロット画像を保護: ${id} (src: ${img.src})`);
        return; // C1サブスロットの既存画像は触らない
      }
      
      console.log(`Rendering: ${id}`);
      img.src = `slot_images/common/placeholder.png`;
      img.alt = `Placeholder for ${id}`;
    } else {
      console.warn(`Not found: ${id}`);
    }
  });
  
  // 🛡️ C1サブスロット画像保護システム（強制保護）
  document.addEventListener('DOMNodeInserted', function(e) {
    if (e.target.tagName === 'IMG' && e.target.closest('[id^="slot-c1-sub-"]')) {
      const container = e.target.closest('[id^="slot-c1-sub-"]');
      if (container && e.target.hasAttribute('data-meta-tag')) {
        console.log(`🛡️ C1サブスロット画像を強制保護: ${container.id}`);
        Object.defineProperty(e.target, 'src', {
          set: function(value) {
            if (this.hasAttribute('data-meta-tag') && value.includes('placeholder.png')) {
              console.log(`🚫 C1サブスロット画像の placeholder.png 設定をブロック: ${container.id}`);
              return; // placeholder.png への変更を阻止
            }
            this.setAttribute('src', value);
          },
          get: function() {
            return this.getAttribute('src');
          }
        });
      }
    }
  });
});