// Определяем, стоит ли давать кастомную схему (whatsapp://, tg://)
// или официальную https-ссылку.
//
// На десктопе кастомная схема открывает приложение мгновенно, без
// промежуточной вкладки браузера. На мобильных и во встроенных
// WebView (Telegram-app, VK, и т.п.) кастомные схемы либо падают
// с ошибкой, либо игнорируются — там нужна https-ссылка.
function isDesktopBrowser() {
    var ua = navigator.userAgent || '';

    // Явные признаки мобильной ОС — вне зависимости от режима браузера
    var mobileOS = /Android|iPhone|iPad|iPod|Mobile|Windows Phone/i.test(ua);
    if (mobileOS) return false;

    // Явные признаки встроенных WebView (Telegram desktop-app тоже
    // рендерит страницы в своём WebView, а не в системном браузере)
    var inAppWebview =
        !!window.TelegramWebviewProxy ||               // Telegram WebView (iOS/Android)
        !!(window.Telegram && window.Telegram.WebApp) || // Telegram Mini App
        /\bTelegram\b/i.test(ua) ||                      // некоторые сборки светят это в UA
        /\bwv\b/i.test(ua);                              // Android "WebView" маркер в UA

    if (inAppWebview) return false;

    // Грубая эвристика: у десктопа обычно нет touch как основного
    // указателя и достаточно широкий экран
    var coarsePointer = window.matchMedia && window.matchMedia('(pointer: coarse)').matches;
    if (coarsePointer) return false;

    return true;
}

function setupContactLinks() {
    var desktop = isDesktopBrowser();
    document.querySelectorAll('.js-contact-link').forEach(function (link) {
        var appHref = link.dataset.appHref;
        var webHref = link.dataset.webHref;
        link.href = desktop ? appHref : webHref;

        // На десктопе кастомная схема не должна открывать новую вкладку —
        // это как раз то, что оставляет "мусорные" вкладки, если браузер
        // не находит обработчик и просто выводит страницу ошибки/уведомление
        if (desktop) {
            link.removeAttribute('target');
        }
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