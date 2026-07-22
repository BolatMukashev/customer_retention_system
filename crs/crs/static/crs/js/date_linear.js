(function () {
    var ITEM_HEIGHT = 40;
    var MONTHS = [
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
    ];

    function pad(n) {
        return String(n).padStart(2, '0');
    }

    function daysInMonth(month, year) {
        return new Date(year, month, 0).getDate();
    }

    function parseDMYDate(value) {
        var parts = (value || '').split('-');
        if (parts.length === 3) {
            return {
                day: parseInt(parts[0], 10),
                month: parseInt(parts[1], 10),
                year: parseInt(parts[2], 10)
            };
        }
        var today = new Date();
        return { day: today.getDate(), month: today.getMonth() + 1, year: today.getFullYear() };
    }

    function buildColumn(col, values, labels, initialValue, onChange) {
        var list = document.createElement('ul');
        list.className = 'wheel-list';

        values.forEach(function (value, i) {
            var li = document.createElement('li');
            li.className = 'wheel-item';
            li.textContent = labels[i];
            li.dataset.value = value;
            list.appendChild(li);
        });
        col.innerHTML = '';
        col.appendChild(list);

        var items = list.querySelectorAll('.wheel-item');

        function currentIndex() {
            return Math.max(0, Math.min(items.length - 1, Math.round(col.scrollTop / ITEM_HEIGHT)));
        }

        function paintActive(index) {
            items.forEach(function (it, i) {
                it.classList.toggle('is-selected', i === index);
            });
        }

        function selectIndex(index, smooth) {
            index = Math.max(0, Math.min(items.length - 1, index));
            col.scrollTo({ top: index * ITEM_HEIGHT, behavior: smooth ? 'smooth' : 'auto' });
            paintActive(index);
        }

        var settleTimer = null;
        col.addEventListener('scroll', function () {
            paintActive(currentIndex());
            if (settleTimer) clearTimeout(settleTimer);
            settleTimer = setTimeout(function () {
                var index = currentIndex();
                selectIndex(index, true);
                onChange(items[index].dataset.value);
            }, 120);
        });

        items.forEach(function (it, i) {
            it.addEventListener('click', function () {
                selectIndex(i, true);
                onChange(it.dataset.value);
            });
        });

        var startIndex = values.findIndex(function (v) { return String(v) === String(initialValue); });
        if (startIndex < 0) startIndex = 0;
        requestAnimationFrame(function () {
            selectIndex(startIndex, false);
        });
    }

    function initPicker(root) {
        var dateInput = document.getElementById(root.dataset.dateInput);
        var dayCol = root.querySelector('[data-role="day"]');
        var monthCol = root.querySelector('[data-role="month"]');
        var yearCol = root.querySelector('[data-role="year"]');

        var initial = parseDMYDate(dateInput.value);
        var state = { day: initial.day, month: initial.month, year: initial.year };

        function commit() {
            var maxDay = daysInMonth(state.month, state.year);
            if (state.day > maxDay) state.day = maxDay;
            dateInput.value = pad(state.day) + '-' + pad(state.month) + '-' + state.year;
        }

        function rebuildDayColumn() {
            var maxDay = daysInMonth(state.month, state.year);
            if (state.day > maxDay) state.day = maxDay;
            var days = [];
            for (var d = 1; d <= maxDay; d++) days.push(d);
            buildColumn(dayCol, days, days.map(String), state.day, function (value) {
                state.day = parseInt(value, 10);
                commit();
            });
        }

        var months = [];
        for (var m = 1; m <= 12; m++) months.push(m);
        buildColumn(monthCol, months, MONTHS, state.month, function (value) {
            state.month = parseInt(value, 10);
            rebuildDayColumn();
            commit();
        });

        var currentYear = new Date().getFullYear();
        var years = [];
        for (var y = currentYear + 1; y >= currentYear - 100; y--) years.push(y);
        buildColumn(yearCol, years, years.map(String), state.year, function (value) {
            state.year = parseInt(value, 10);
            rebuildDayColumn();
            commit();
        });

        rebuildDayColumn();
        commit();
    }

    document.querySelectorAll('.wheel-date-picker').forEach(initPicker);
})();