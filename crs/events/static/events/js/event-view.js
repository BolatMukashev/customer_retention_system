function isDesktopBrowser() {
    try {
        var ua = navigator.userAgent || '';

        var mobileOS = /Android|iPhone|iPad|iPod|Mobile|Windows Phone/i.test(ua);
        if (mobileOS) return false;

        var inAppWebview =
            !!window.TelegramWebviewProxy ||
            !!(window.Telegram && window.Telegram.WebApp) ||
            /\bTelegram\b/i.test(ua) ||
            /\bwv\b/i.test(ua);
        if (inAppWebview) return false;

        var coarsePointer = window.matchMedia && window.matchMedia('(pointer: coarse)').matches;
        if (coarsePointer) return false;

        return true;
    } catch (e) {
        // Если детект сломался — остаёмся на безопасной https-ссылке
        return false;
    }
}

function setupContactLinks() {
    var desktop = isDesktopBrowser();
    if (!desktop) return; // на мобильных/WebView оставляем https-ссылку из разметки как есть

    document.querySelectorAll('.js-contact-link').forEach(function (link) {
        var appHref = link.dataset.appHref;
        if (!appHref) return;

        link.addEventListener('click', function (e) {
            e.preventDefault();
            window.location.href = appHref;
        });
        link.removeAttribute('target');
    });
}


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