/* global lucide */
document.addEventListener('DOMContentLoaded', () => {
  console.log('script.js loaded ✅');

  // ── Elements ───────────────────────────────────────────────────────
  const fileInput = document.getElementById('input-images');
  const dropZone = document.getElementById('drop-zone');
  const previewGrid = document.getElementById('preview-section');
  const convertedGrid = document.getElementById('converted-images-section');
  const toasts = document.getElementById('toasts');

  // Theme toggle es opcional (si falta, NO rompemos nada)
  const themeBtn = document.getElementById('theme-toggle');
  const root = document.documentElement;

  console.log('DOM refs:', {
    fileInput: !!fileInput,
    dropZone: !!dropZone,
    previewGrid: !!previewGrid,
    convertedGrid: !!convertedGrid,
    toasts: !!toasts,
    themeBtn: !!themeBtn
  });

  // Si falta lo esencial para previews/converted, no tiene sentido seguir
  if (!fileInput || !dropZone || !previewGrid || !convertedGrid || !toasts) {
    console.error('Missing required DOM elements ❌. Check your IDs in index.html.');
    return;
  }

  // ── Theme toggle ────────────────────────────────────────────────────
  try {
    const saved = localStorage.getItem('theme') || 'light';
    root.classList.toggle('dark', saved === 'dark');

    if (themeBtn) {
      setIcon(saved);

      themeBtn.addEventListener('click', () => {
        const next = root.classList.contains('dark') ? 'light' : 'dark';
        root.classList.toggle('dark', next === 'dark');
        localStorage.setItem('theme', next);
        setIcon(next);
      });
    }

    function setIcon(mode) {
      if (!themeBtn) return;
      themeBtn.innerHTML = '';

      // No dependas de lucide para que la app funcione
      if (!window.lucide || typeof lucide.createElement !== 'function') {
        themeBtn.textContent = mode === 'dark' ? '☀️' : '🌙';
        return;
      }

      const svg = lucide.createElement(mode === 'dark' ? 'sun' : 'moon');
      svg.classList.add('w-5', 'h-5');
      themeBtn.appendChild(svg);
    }
  } catch (e) {
    console.warn('Theme toggle failed (non-blocking):', e);
  }

  // ── Toast helper ────────────────────────────────────────────────────
  function addToast(type, msg) {
    const toast = document.createElement('div');

    const color =
      type === 'success' ? 'bg-emerald-500'
      : type === 'error' ? 'bg-rose-500'
      : 'bg-sky-500';

    toast.className = `px-4 py-3 rounded-lg shadow-lg text-white ${color}`;
    toast.textContent = msg;
    toasts.appendChild(toast);

    setTimeout(() => toast.remove(), 5000);
  }

  // ── Converted rendering ─────────────────────────────────────────────
  function showConverted(urls) {
    console.log('showConverted urls:', urls);
    convertedGrid.innerHTML = '';

    urls.forEach(url => {
      const a = document.createElement('a');
      a.href = url;
      a.download = '';
      a.target = '_blank';
      a.rel = 'noopener noreferrer';

      const img = document.createElement('img');
      img.src = url;
      img.className = 'converted-image';
      img.loading = 'lazy';

      img.addEventListener('error', () => {
        console.warn('Converted image failed to load:', url);
      });

      a.appendChild(img);
      convertedGrid.appendChild(a);
    });
  }

  // ── Flashes (nuevo formato: [ [category, message], ... ]) ───────────
  try {
    const rawFlashes = window.flashedMessages || [];
    console.log('flashedMessages:', rawFlashes);

    const convertedUrls = [];

    rawFlashes.forEach(item => {
      if (!Array.isArray(item) || item.length < 2) return;
      const [category, message] = item;

      if (category === 'converted_url') convertedUrls.push(message);
      else {
        const type = (category === 'success' || category === 'error') ? category : 'info';
        addToast(type, message);
      }
    });

    if (convertedUrls.length) showConverted(convertedUrls);
  } catch (e) {
    console.error('Flash parsing failed ❌:', e);
  }

  // ── Preview grid ────────────────────────────────────────────────────
  fileInput.addEventListener('change', () => {
    console.log('file input changed:', fileInput.files?.length || 0);
    displayPreviews(fileInput.files);
  });

  function displayPreviews(files) {
    console.log('displayPreviews called with:', files?.length || 0);
    previewGrid.innerHTML = '';

    [...files].forEach(file => {
      if (!file.type || !file.type.startsWith('image/')) return;

      const img = document.createElement('img');
      img.className = 'preview-image';
      previewGrid.appendChild(img);

      const reader = new FileReader();
      reader.onload = e => (img.src = e.target.result);
      reader.onerror = err => console.warn('FileReader error:', err);
      reader.readAsDataURL(file);
    });
  }

  // ── Drag & drop ─────────────────────────────────────────────────────
  ['dragenter', 'dragover'].forEach(ev =>
    dropZone.addEventListener(ev, e => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add('border-teal-500', 'bg-teal-50', 'dark:bg-teal-900/30');
    })
  );

  ['dragleave', 'drop'].forEach(ev =>
    dropZone.addEventListener(ev, e => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove('border-teal-500', 'bg-teal-50', 'dark:bg-teal-900/30');
    })
  );

  dropZone.addEventListener('drop', e => {
    const files = e.dataTransfer.files;
    console.log('dropped files:', files?.length || 0);

    displayPreviews(files);

    // Importante: asignarlos al input para que el form los envíe
    const dt = new DataTransfer();
    [...files].forEach(f => dt.items.add(f));
    fileInput.files = dt.files;
  });
});