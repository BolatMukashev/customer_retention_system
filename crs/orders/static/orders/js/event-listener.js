document.addEventListener('DOMContentLoaded', function () {
    var select = document.getElementById('days-filter');
    if (!select) return;

    select.addEventListener('change', function () {
        var params = new URLSearchParams();
        var status = select.dataset.status;
        if (status) params.set('status', status);
        if (select.value) params.set('days', select.value);
        var qs = params.toString();
        window.location.href = window.location.pathname + (qs ? '?' + qs : '');
    });
});