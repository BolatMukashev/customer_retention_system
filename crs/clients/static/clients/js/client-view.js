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