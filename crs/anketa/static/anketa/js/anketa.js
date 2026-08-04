document.addEventListener('DOMContentLoaded', () => {
    const fill = document.querySelector('.progress-fill');
    if (!fill) return;
    const target = fill.dataset.target || 0;
    requestAnimationFrame(() => {
        fill.style.width = target + '%';
    });
});