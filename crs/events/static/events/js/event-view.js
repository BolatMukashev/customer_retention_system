document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('proposal-toggle');
    const label = document.getElementById('proposal-label');
    if (!toggle) return;

    toggle.addEventListener('change', function () {
        const url = toggle.dataset.url;
        const csrf = toggle.dataset.csrf;
        const prevChecked = !toggle.checked;

        toggle.disabled = true;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf,
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
            .then(response => {
                if (!response.ok) throw new Error('Request failed');
                return response.json();
            })
            .then(data => {
                toggle.checked = data.proposal_sent;
                label.textContent = data.proposal_sent
                    ? 'Предложение отправлено'
                    : 'Предложение не отправлено';
            })
            .catch(() => {
                toggle.checked = prevChecked;
            })
            .finally(() => {
                toggle.disabled = false;
            });
    });
});