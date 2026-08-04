document.addEventListener('DOMContentLoaded', () => {
    const addBtn = document.getElementById('add-reward');
    const rows = document.getElementById('reward-rows');
    const totalForms = document.querySelector('#rewards-form [name="rewards-TOTAL_FORMS"]');

    addBtn.addEventListener('click', () => {
        const currentCount = parseInt(totalForms.value, 10);
        if (currentCount >= 10) {
            alert('Максимум 10 наград');
            return;
        }
        const template = rows.querySelector('.reward-row');
        const clone = template.cloneNode(true);

        clone.querySelectorAll('input').forEach(input => {
            const name = input.name.replace(/-\d+-/, `-${currentCount}-`);
            const id = input.id.replace(/-\d+-/, `-${currentCount}-`);
            input.name = name;
            input.id = id;
            if (input.type === 'checkbox') {
                input.checked = false;
            } else if (input.type !== 'hidden') {
                input.value = '';
            } else {
                input.value = '';
            }
        });
        clone.querySelectorAll('.field-error').forEach(el => el.remove());
        rows.appendChild(clone);
        totalForms.value = currentCount + 1;
    });
});