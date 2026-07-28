
document.addEventListener('DOMContentLoaded', function () {
    var wrapper = document.querySelector('.status-select');
    if (!wrapper) return;

    var url = wrapper.dataset.url;
    var csrf = wrapper.dataset.csrf;

    wrapper.addEventListener('click', function (e) {
        var btn = e.target.closest('.status-option');
        if (!btn || btn.classList.contains('is-active')) return;

        var status = btn.dataset.status;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'status=' + encodeURIComponent(status),
        })
        .then(function (res) { return res.json(); })
        .then(function (data) {
            if (data.error) return;
            wrapper.querySelectorAll('.status-option').forEach(function (el) {
                el.classList.toggle('is-active', el.dataset.status === status);
            });
        })
        .catch(function () {
            // при ошибке сети просто оставляем как было
        });
    });
});