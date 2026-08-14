// Определяем, стоит ли давать кастомную схему (whatsapp://, tg://)
// или официальную https-ссылку.
//
// На десктопе кастомная схема открывает приложение мгновенно, без
// промежуточной вкладки браузера. На мобильных и во встроенных
// WebView (Telegram-app, VK, и т.п.) кастомные схемы либо падают
// с ошибкой, либо игнорируются — там нужна https-ссылка.
//
// ВАЖНО: href у ссылок в разметке изначально указывает на
// https://wa.me / https://t.me — это рабочий вариант "по
// умолчанию", который сработает даже если этот скрипт не
// загрузится или упадёт с ошибкой. Скрипт ниже лишь улучшает
// поведение на десктопе, подменяя схему прямо в момент клика.
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
    setupContactLinks();

    document.querySelectorAll('.toggle-switch input[data-url]').forEach(function (toggle) {
        const row = toggle.closest('.bento-cell--status');
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