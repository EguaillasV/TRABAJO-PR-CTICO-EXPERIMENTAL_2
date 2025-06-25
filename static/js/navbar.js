document.addEventListener('DOMContentLoaded', function() {
    // User dropdown functionality
    const userDropdown = document.getElementById('userDropdown');
    const userDropdownMenu = document.getElementById('userDropdownMenu');
    const userDropdownIcon = document.getElementById('userDropdownIcon');
    
    if (userDropdown && userDropdownMenu) {
        userDropdown.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const isVisible = !userDropdownMenu.classList.contains('opacity-0');
            
            if (isVisible) {
                // Hide dropdown
                userDropdownMenu.classList.add('opacity-0', 'invisible', 'scale-95');
                userDropdownMenu.classList.remove('opacity-100', 'visible', 'scale-100');
                if (userDropdownIcon) userDropdownIcon.classList.remove('rotate-180');
            } else {
                // Show dropdown
                userDropdownMenu.classList.remove('opacity-0', 'invisible', 'scale-95');
                userDropdownMenu.classList.add('opacity-100', 'visible', 'scale-100');
                if (userDropdownIcon) userDropdownIcon.classList.add('rotate-180');
            }
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!userDropdown.contains(e.target) && !userDropdownMenu.contains(e.target)) {
                userDropdownMenu.classList.add('opacity-0', 'invisible', 'scale-95');
                userDropdownMenu.classList.remove('opacity-100', 'visible', 'scale-100');
                if (userDropdownIcon) userDropdownIcon.classList.remove('rotate-180');
            }
        });

        // Prevent dropdown from closing when clicking inside
        userDropdownMenu.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }

    // Groups selector functionality (desktop and mobile)
    function handleGroupChange(selector) {
        if (selector) {
            selector.addEventListener('change', function() {
                const selectedGroup = this.value;
                const homeUrl = this.dataset.homeUrl || '/';
                
                if (selectedGroup) {
                    window.location.href = `${homeUrl}?gpid=${selectedGroup}`;
                } else {
                    window.location.href = homeUrl;
                }
            });
        }
    }

    // Add data attributes to selectors for URL handling
    const groupSelects = document.querySelectorAll('#groupSelect, #mobileGroupSelect');
    groupSelects.forEach(select => {
        handleGroupChange(select);
    });
});