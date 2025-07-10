// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    // Add active class to current navigation item
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('nav ul li a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.parentElement.classList.add('active');
        }
    });

    // Login form handling (for future Flask integration)
    const loginForm = document.querySelector('.login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(loginForm);
            const data = {
                cpf_number: formData.get('cpf_number'),
                password: formData.get('password')
            };

            try {
                // This will be replaced with actual Flask endpoint
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    const result = await response.json();
                    if (result.success) {
                        window.location.href = '/dashboard';
                    } else {
                        alert('Invalid credentials');
                    }
                } else {
                    throw new Error('Login failed');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Login failed. Please try again.');
            }
        });
    }
});