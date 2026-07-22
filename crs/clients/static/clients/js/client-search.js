(function () {
    var MIN_LEN = 2;
    var DELAY = 250;

    var wrapper = document.querySelector('.client-autocomplete');
    if (!wrapper) return;

    var searchUrl = wrapper.dataset.searchUrl;
    var display = document.getElementById('client_search_display');
    var box = document.getElementById('client_search_suggestions');

    var debounceTimer = null;
    var currentController = null;
    var items = [];
    var activeIndex = -1;

    function closeBox() {
        box.style.display = 'none';
        box.innerHTML = '';
        activeIndex = -1;
    }

    function renderMessage(text) {
        box.innerHTML = '<div class="client-suggestion client-suggestion-empty">' + text + '</div>';
        box.style.display = 'block';
    }

    function renderResults(results) {
        items = results;
        activeIndex = -1;
        if (!results.length) {
            renderMessage('Ничего не найдено');
            return;
        }
        box.innerHTML = '';
        results.forEach(function (item, index) {
            var row = document.createElement('div');
            row.className = 'client-suggestion';
            row.textContent = item.text;
            row.dataset.index = index;
            row.addEventListener('mousedown', function (e) {
                // mousedown раньше blur — успеваем перейти до скрытия списка
                e.preventDefault();
                goToClient(item);
            });
            box.appendChild(row);
        });
        box.style.display = 'block';
    }

    function goToClient(item) {
        window.location.href = item.url;
    }

    function fetchResults(query) {
        if (currentController) {
            currentController.abort();
        }
        currentController = new AbortController();
        renderMessage('Поиск…');

        fetch(searchUrl + '?q=' + encodeURIComponent(query), {
            signal: currentController.signal,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                renderResults(data.results || []);
            })
            .catch(function (err) {
                if (err.name !== 'AbortError') {
                    renderMessage('Не удалось загрузить результаты');
                }
            });
    }

    display.addEventListener('input', function () {
        var query = display.value.trim();

        if (debounceTimer) clearTimeout(debounceTimer);

        if (query.length < MIN_LEN) {
            var remaining = MIN_LEN - query.length;
            if (query.length === 0) {
                closeBox();
            } else {
                renderMessage('Введите ещё хотя бы ' + remaining + ' символ(а)');
            }
            return;
        }

        debounceTimer = setTimeout(function () {
            fetchResults(query);
        }, DELAY);
    });

    display.addEventListener('keydown', function (e) {
        if (box.style.display !== 'block' || !items.length) return;

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            activeIndex = Math.min(activeIndex + 1, items.length - 1);
            highlight();
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            activeIndex = Math.max(activeIndex - 1, 0);
            highlight();
        } else if (e.key === 'Enter') {
            if (activeIndex >= 0) {
                e.preventDefault();
                goToClient(items[activeIndex]);
            }
        } else if (e.key === 'Escape') {
            closeBox();
        }
    });

    function highlight() {
        var rows = box.querySelectorAll('.client-suggestion');
        rows.forEach(function (row, index) {
            row.classList.toggle('is-active', index === activeIndex);
        });
    }

    display.addEventListener('blur', function () {
        setTimeout(closeBox, 100);
    });

    display.addEventListener('focus', function () {
        if (display.value.trim().length >= MIN_LEN && items.length) {
            box.style.display = 'block';
        }
    });
})();

