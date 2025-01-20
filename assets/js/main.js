// Global Ajax Setup
$.ajaxSetup({
    beforeSend: function() {
        $('#app-loader').removeClass('d-none');
    },
    complete: function() {
        $('#app-loader').addClass('d-none');
    },
    error: function(xhr, status, error) {
        showNotification('error', 'Bir hata oluştu: ' + error);
    }
});

// Notification function
function showNotification(type, message) {
    const toast = `
        <div class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-delay="5000">
            <div class="toast-header bg-${type}">
                <strong class="me-auto text-white">${type === 'success' ? 'Başarılı' : 'Hata'}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">${message}</div>
        </div>
    `;
    
    $('#toastContainer').append(toast);
    $('.toast').toast('show');
}

// Sidebar toggle
$(document).ready(function() {
    $('#sidebarCollapse').on('click', function() {
        $('#sidebar').toggleClass('active');
        $(this).toggleClass('active');
        
        // Save state
        localStorage.setItem('sidebarState', $('#sidebar').hasClass('active') ? 'collapsed' : 'expanded');
    });
    
    // Load saved state
    const sidebarState = localStorage.getItem('sidebarState');
    if (sidebarState === 'collapsed') {
        $('#sidebar').addClass('active');
        $('#sidebarCollapse').addClass('active');
    }
});

// Data table initialization
function initDataTable(selector, options = {}) {
    const defaultOptions = {
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/Turkish.json'
        },
        pageLength: 25,
        responsive: true,
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    };
    
    return $(selector).DataTable({...defaultOptions, ...options});
}

// Form validation
function validateForm(formSelector) {
    const form = $(formSelector);
    if (form.length === 0) return false;
    
    let isValid = true;
    form.find('[required]').each(function() {
        if (!$(this).val()) {
            isValid = false;
            $(this).addClass('is-invalid');
        } else {
            $(this).removeClass('is-invalid');
        }
    });
    
    return isValid;
}

// AJAX form submission
function submitForm(formSelector, successCallback = null) {
    const form = $(formSelector);
    if (!validateForm(formSelector)) {
        showNotification('error', 'Lütfen tüm zorunlu alanları doldurun.');
        return;
    }
    
    $.ajax({
        url: form.attr('action'),
        method: form.attr('method'),
        data: form.serialize(),
        success: function(response) {
            if (response.success) {
                showNotification('success', response.message);
                if (successCallback) successCallback(response);
            } else {
                showNotification('error', response.message);
            }
        }
    });
}

// Confirm dialog
function confirmDialog(message, callback) {
    const modal = `
        <div class="modal fade" id="confirmModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Onay</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">${message}</div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">İptal</button>
                        <button type="button" class="btn btn-primary" id="confirmBtn">Onay</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    $('body').append(modal);
    const modalElement = $('#confirmModal');
    const confirmModal = new bootstrap.Modal(modalElement);
    
    $('#confirmBtn').on('click', function() {
        callback();
        confirmModal.hide();
    });
    
    modalElement.on('hidden.bs.modal', function() {
        modalElement.remove();
    });
    
    confirmModal.show();
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('tr-TR', {
        style: 'currency',
        currency: 'TRY'
    }).format(amount);
}

// Format date
function formatDate(date) {
    return new Intl.DateTimeFormat('tr-TR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(new Date(date));
}
