/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
  // Check if user is logged in and update login/logout button
  updateAuthButton();

  const loginForm = document.getElementById('login-form');
  // Handle login form if it exists on the page
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();  // Prevent normal form submission

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      
      try {
        console.log("Attempting login with:", email);
        const response = await fetch('http://127.0.0.1:5000/api/v1/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        // Handle the response
        if (response.ok) {
          const data = await response.json();
          console.log("Login successful:", data);
          document.cookie = `token=${data.access_token}; path=/`;
          window.location.href = 'index.html';
        } else {
          console.error("Login failed with status:", response.status);
          alert('Login failed: ' + (response.statusText || 'Invalid credentials'));
        }
      } catch (error) {
        console.error('Error during login:', error);
        alert('Login failed: Network error');
      }
    });
  }

  // Add price filtering functionality
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    // Initialize the filter on page load
    filterPlacesByPrice();
    
    // Listen for changes to the price filter
    priceFilter.addEventListener('change', filterPlacesByPrice);
  }
  
  // Call getPlaces on page load if we have a places list container
  const placesContainer = document.getElementById('places-list-id') || document.querySelector('.places-list');
  if (placesContainer) {
    getPlaces();
  }
});

// Function to check if user is logged in and update the auth button
function updateAuthButton() {
  const authButton = document.querySelector('.login-button');
  if (!authButton) return;
  
  // Check if user has a token
  const hasToken = document.cookie.split(';').some(item => item.trim().startsWith('token='));
  
  if (hasToken) {
    // User is logged in, show logout button
    authButton.textContent = 'Logout';
    authButton.href = '#';
    authButton.addEventListener('click', function(e) {
      e.preventDefault();
      // Clear the token cookie
      document.cookie = 'token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
      // Redirect to homepage
      window.location.href = 'index.html';
    });
  } else {
    // User is not logged in, ensure button shows Login
    authButton.textContent = 'Login';
    authButton.href = 'login.html';
  }
}

function filterPlacesByPrice() {
  const filterValue = document.getElementById('price-filter').value;
  const placeCards = document.querySelectorAll('.place-card');
  
  // Convert filter value to a maximum price
  let maxPrice;
  switch (filterValue) {
    case '2':
      maxPrice = 10;
      break;
    case '3':
      maxPrice = 50;
      break;
    case '4':
      maxPrice = 100;
      break;
    default:
      maxPrice = Number.MAX_SAFE_INTEGER; // "All" option
  }
  
  // Loop through all place cards
  placeCards.forEach(card => {
    // Extract the price from the card
    const priceText = card.querySelector('.price').textContent;
    const price = parseInt(priceText.match(/\$(\d+)/)[1]);
    
    // Show or hide based on the price
    if (price <= maxPrice || maxPrice === Number.MAX_SAFE_INTEGER) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}