document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.checkbox-btn').forEach(function (lbl) {
        lbl.addEventListener('click', function (e) {
            e.preventDefault();
            const forId = this.getAttribute('for') || this.htmlFor;
            if (!forId) return;
            const cb = document.getElementById(forId);
            if (!cb) return;
            cb.checked = !cb.checked;
            cb.value = cb.checked ? "true" : "false";
            if (cb.checked) {
                this.classList.add('cb-checked');
            } else {
                this.classList.remove('cb-checked');
            }
            cb.dispatchEvent(new Event('change', { bubbles: true }));
            cb.focus();
        });
    });

    document.querySelectorAll('.checkbox-input').forEach(function (cb) {
        const lbl = document.querySelector('label[for="' + cb.id + '"]');
        if (lbl) {
            if (cb.checked) lbl.classList.add('cb-checked');
            else lbl.classList.remove('cb-checked');
        }
        cb.addEventListener('change', function () {
            cb.value = cb.checked ? "true" : "false";
            if (lbl) {
                if (cb.checked) lbl.classList.add('cb-checked');
                else lbl.classList.remove('cb-checked');
            }
        });
    });

    const form = document.getElementById('assignForm');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const chosen = Array.from(document.querySelectorAll('.checkbox-input'))
                .filter(i => i.value === "true")
                .map(i => i.name);
            console.log('Selected directorates:', chosen);
            return false;
        });
    }
});
