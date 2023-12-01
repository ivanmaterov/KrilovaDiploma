/**
 * Инициализировать модальное окно для подтверждения удаления
 *
 * @param {string} modalId - id модального окна
 *
 * @returns {null}
 */
function initConfirmDeleteModalWindow(modalId) {
    const confirmDeleteModal = document.getElementById(modalId);
    let form = confirmDeleteModal.querySelector('form');
    let modalBody = confirmDeleteModal.querySelector('.modal-body');
    
    confirmDeleteModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;

        const rowId = button.getAttribute('data-bs-id');
        const computerName = button.getAttribute('data-bs-computer-name');
        const deviceDisplayName = button.getAttribute('data-bs-device-display-name')
        const status = button.getAttribute('data-bs-status')

        modalBody.querySelector('.computer_name').textContent = computerName
        modalBody.querySelector('.system_device_name').textContent = deviceDisplayName
        modalBody.querySelector('.status').textContent = status

        form.action = 'access-control-delete/' + rowId;
    });
};
