/**
 * Инициализировать чекбокс для фильтрации по строкам со статусом = 'prohibited'
 *
 * @param {object} table - таблица jquery DataTables
 *
 * @returns {null}
 */
function initFilterByStatus(table) {
    const select = document.getElementById('selectStatus');
    DataTable.ext.search.push(function (settings, data, dataIndex) {
        if (select.value === 'Статус') {
            return true;
        }

        if (data[7] === select.value) {
            return true;
        }
        return false;
    });

    select.addEventListener('change', function () {
        table.draw();
    });
};
