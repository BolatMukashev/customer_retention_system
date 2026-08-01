document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('notified-toggle');
    const label = document.getElementById('notified-label');

    toggle.addEventListener('change', function () {
        fetch(toggle.dataset.url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': toggle.dataset.csrf,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
        .then(res => res.json())
        .then(data => {
            label.textContent = data.notified ? 'Анкета отправлена' : 'Анкета не отправлена';
        })
        .catch(() => {
            toggle.checked = !toggle.checked;
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