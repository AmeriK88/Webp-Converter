/* global lucide */
document.addEventListener('DOMContentLoaded', () => {
  // ── Elements ───────────────────────────────────────────────────────
  const fileInput   = document.getElementById('input-images');
  const dropZone    = document.getElementById('drop-zone');
  const previewGrid = document.getElementById('preview-section');
  const convertedGrid = document.getElementById('converted-images-section');
  const toasts      = document.getElementById('toasts');
  const themeBtn    = document.getElementById('theme-toggle');
  const root        = document.documentElement;

  // ── Theme toggle ────────────────────────────────────────────────────
  const saved = localStorage.getItem('theme') || 'light';
  root.classList.toggle('dark', saved === 'dark');
  setIcon(saved);

  themeBtn.addEventListener('click', () => {
    const next = root.classList.contains('dark') ? 'light' : 'dark';
    root.classList.toggle('dark', next === 'dark');
    localStorage.setItem('theme', next);
    setIcon(next);
  });

  function setIcon(mode) {
    themeBtn.innerHTML = '';                       // limpia
    const svg = lucide.createElement(mode === 'dark' ? 'sun' : 'moon');
    svg.classList.add('w-5','h-5');
    themeBtn.appendChild(svg);
  }

  // ── Toast helper ────────────────────────────────────────────────────
  function addToast(type, msg) {
    const toast = document.createElement('div');
    toast.className =
      `px-4 py-3 rounded-lg shadow-lg text-white ${
        type === 'success' ? 'bg-emerald-500' : 'bg-rose-500'
      }`;
    toast.textContent = msg;
    toasts.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
  }

  // ── Mostrar flashes (toasts + imágenes convertidas) ────────────────
  (window.flashedMessages || []).forEach(({ category, message }) => {
    if (category === 'converted') {
      const urls = message.split('|');
      showConverted(urls);
    } else {
      addToast(category, message);
    }
  });

  function showConverted(urls) {
    convertedGrid.innerHTML = '';
    urls.forEach(url => {
      const link = document.createElement('a');
      link.href = url;
      link.download = '';
      link.target = '_blank';

      const img = document.createElement('img');
      img.src = url;
      img.className = 'converted-image';
      link.appendChild(img);

      convertedGrid.appendChild(link);
    });
  }

  // ── Preview grid ────────────────────────────────────────────────────
  fileInput.addEventListener('change', () => displayPreviews(fileInput.files));

  function displayPreviews(files) {
    previewGrid.innerHTML = '';
    [...files].forEach(file => {
      if (!file.type.startsWith('image/')) return;
      const img = document.createElement('img');
      img.className = 'preview-image';
      previewGrid.appendChild(img);

      const reader = new FileReader();
      reader.onload = e => (img.src = e.target.result);
      reader.readAsDataURL(file);
    });
  }

  // ── Drag & drop ─────────────────────────────────────────────────────
  ['dragenter','dragover'].forEach(ev =>
    dropZone.addEventListener(ev, e => {
      e.preventDefault(); e.stopPropagation();
      dropZone.classList.add('border-teal-500','bg-teal-50','dark:bg-teal-900/30');
    })
  );
  ['dragleave','drop'].forEach(ev =>
    dropZone.addEventListener(ev, e => {
      e.preventDefault(); e.stopPropagation();
      dropZone.classList.remove('border-teal-500','bg-teal-50','dark:bg-teal-900/30');
    })
  );
  dropZone.addEventListener('drop', e => {
    fileInput.files = e.dataTransfer.files;
    displayPreviews(fileInput.files);
  });
});
