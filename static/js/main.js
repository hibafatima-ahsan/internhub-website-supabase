// InternHub Client JS Script
document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss alert banners after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        const closeBtn = alert.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 250);
            });
        }
        
        setTimeout(() => {
            if (alert && alert.parentNode) {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500);
            }
        }, 5000);
    });

    // Client-side confirmation for deletions
    const deleteButtons = document.querySelectorAll('.btn-confirm-delete');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            if (!confirm('Are you sure you want to proceed with this deletion? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
});
