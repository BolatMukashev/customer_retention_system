document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.toggle-switch input[data-url]').forEach(function (toggle) {
        const row = toggle.closest('.profile-row');
        const label = row ? row.querySelector('.toggle-label') : null;
        const onText = toggle.dataset.onText || 'Включено';
        const offText = toggle.dataset.offText || 'Выключено';

        toggle.addEventListener('change', function () {
            const prevChecked = !toggle.checked;
            toggle.disabled = true;

            fetch(toggle.dataset.url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': toggle.dataset.csrf,
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
                .then(res => {
                    if (!res.ok) throw new Error('Request failed');
                    return res.json();
                })
                .then(data => {
                    const value = Object.values(data)[0];
                    toggle.checked = value;
                    if (label) label.textContent = value ? onText : offText;
                })
                .catch(() => {
                    toggle.checked = prevChecked;
                })
                .finally(() => {
                    toggle.disabled = false;
                });
        });
    });
});


document.querySelectorAll('.icon-copy-btn[data-copy]').forEach(btn => {
    btn.addEventListener('click', () => {
        navigator.clipboard.writeText(btn.dataset.copy).then(() => {
            btn.classList.add('is-copied');
            btn.querySelector('.icon-copy').style.display = 'none';
            btn.querySelector('.icon-check').style.display = 'block';
            setTimeout(() => {
                btn.classList.remove('is-copied');
                btn.querySelector('.icon-copy').style.display = 'block';
                btn.querySelector('.icon-check').style.display = 'none';
            }, 1500);
        });
    });
});