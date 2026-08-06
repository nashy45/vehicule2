// Admin Panel JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Image preview for file upload
    const imageInput = document.getElementById('image');
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            const preview = document.getElementById('imagePreview');
            
            if (file) {
                // Check file size (max 16MB)
                const maxSize = 16 * 1024 * 1024; // 16MB in bytes
                if (file.size > maxSize) {
                    alert('File size must be less than 16MB');
                    e.target.value = '';
                    preview.innerHTML = '';
                    return;
                }
                
                // Check file type
                const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
                if (!allowedTypes.includes(file.type)) {
                    alert('Please upload a valid image file (JPEG, PNG, GIF, or WebP)');
                    e.target.value = '';
                    preview.innerHTML = '';
                    return;
                }
                
                // Show preview
                const reader = new FileReader();
                reader.onload = function(event) {
                    preview.innerHTML = `
                        <div class="mt-3">
                            <p class="text-muted mb-2">Preview:</p>
                            <img src="${event.target.result}" 
                                 class="image-preview" 
                                 alt="Preview">
                        </div>
                    `;
                };
                reader.readAsDataURL(file);
            } else {
                preview.innerHTML = '';
            }
        });
    }

    // Form validation
    const vehicleForm = document.getElementById('vehicleForm');
    if (vehicleForm) {
        vehicleForm.addEventListener('submit', function(e) {
            // VIN validation (17 characters)
            const vinInput = document.getElementById('vin');
            if (vinInput && vinInput.value.length !== 17) {
                e.preventDefault();
                alert('VIN must be exactly 17 characters');
                vinInput.focus();
                return false;
            }
            
            // Year validation
            const yearInput = document.getElementById('year');
            const currentYear = new Date().getFullYear();
            if (yearInput) {
                const year = parseInt(yearInput.value);
                if (year < 1990 || year > currentYear + 1) {
                    e.preventDefault();
                    alert(`Year must be between 1990 and ${currentYear + 1}`);
                    yearInput.focus();
                    return false;
                }
            }
            
            // Price validation
            const priceInput = document.getElementById('price');
            if (priceInput && parseFloat(priceInput.value) < 0) {
                e.preventDefault();
                alert('Price must be a positive number');
                priceInput.focus();
                return false;
            }
            
            // Mileage validation
            const mileageInput = document.getElementById('mileage');
            if (mileageInput && parseInt(mileageInput.value) < 0) {
                e.preventDefault();
                alert('Mileage must be a positive number');
                mileageInput.focus();
                return false;
            }
        });
    }

    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm delete actions
    const deleteLinks = document.querySelectorAll('a[href*="delete"]');
    deleteLinks.forEach(link => {
        if (!link.hasAttribute('onclick')) {
            link.addEventListener('click', function(e) {
                if (!confirm('Are you sure you want to delete this item?')) {
                    e.preventDefault();
                }
            });
        }
    });

    // Format number inputs with thousand separators
    const priceInput = document.getElementById('price');
    if (priceInput) {
        priceInput.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (!isNaN(value)) {
                this.value = value;
            }
        });
    }
});
