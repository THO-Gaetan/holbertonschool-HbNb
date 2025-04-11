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
  if (document.getElementById('place-details-id')) {
    getPlaceDetails();
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

async function getPlaces() {
  const placesContainer = document.getElementById('places-list-id');
  if (!placesContainer) return;
  
  try {
    // Show loading indicator
    placesContainer.innerHTML = '<p>Loading places...</p>';
    
    // Fetch places from API
    const response = await fetch('http://127.0.0.1:5000/api/v1/places');
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const places = await response.json();
    
    // Clear the loading message
    placesContainer.innerHTML = '';
    
    if (places.length === 0) {
      placesContainer.innerHTML = '<p>No places available at this time.</p>';
      return;
    }
    
    // Create a card for each place
    places.forEach(place => {
      const placeCard = document.createElement('section');
      placeCard.className = 'place-card';
      
      placeCard.innerHTML = `
        <div class="place-card-info">
          <h2>${place.title}</h2>
          <p>${place.description || 'No description available'}</p>
          <p class="price"><strong>Price per night: </strong>$${place.price}</p>
          <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        </div>
      `;
      
      placesContainer.appendChild(placeCard);
    });
    
    // Re-apply price filter if it's already set
    if (document.getElementById('price-filter')) {
      filterPlacesByPrice();
    }
    
  } catch (error) {
    console.error('Error fetching places:', error);
    placesContainer.innerHTML = '<p>Error loading places. Please try again later.</p>';
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

// Function to get and display details for a specific place
async function getPlaceDetails() {
  const placeDetailsContainer = document.getElementById('place-details-id');
  console.log("getPlaceDetails called, container:", placeDetailsContainer);
  if (!placeDetailsContainer) return;
  
  try {
    // Extract place ID from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    
    if (!placeId) {
      placeDetailsContainer.innerHTML = '<p>Error: No place ID specified</p>';
      return;
    }
    
    // Show loading indicator
    placeDetailsContainer.innerHTML = '<p>Loading place details...</p>';
    
    // Fetch place details from API
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const place = await response.json();
    console.log("Place details:", place); // For debugging
    
    // Fetch user info for the host
    let hostName = "Unknown Host";
    if (place.owner && place.owner.id) {
      try {
        const userResponse = await fetch(`http://127.0.0.1:5000/api/v1/users/${place.owner.id}`);
        if (userResponse.ok) {
          const userData = await userResponse.json();
          hostName = userData.first_name + " " + userData.last_name;
        }
      } catch (userError) {
        console.error("Error fetching host details:", userError);
      }
    }
    
    // Fetch amenities for this place
    let amenitiesList = "None listed";
    try {
      const amenitiesResponse = await fetch(`http://127.0.0.1:5000/api/v1/places/places/${placeId}/amenities`);
      if (amenitiesResponse.ok) {
        const amenities = await amenitiesResponse.json();
        if (amenities.length > 0) {
          amenitiesList = amenities.map(amenity => amenity.name).join(", ");
        }
      }
    } catch (amenitiesError) {
      console.error("Error fetching amenities:", amenitiesError);
    }
    
    // Update the page with place details
    placeDetailsContainer.innerHTML = `
      <h1>${place.name || place.title || "Unnamed Place"}</h1>
      <div class="place-info">
        <p><strong>Host:</strong> ${hostName}</p>
        <p><strong>Price per night:</strong> $${place.price}</p>
        <p><strong>Description:</strong> ${place.description || "No description available"}</p>
        <p><strong>Amenities:</strong> ${amenitiesList}</p>
      </div>
    `;
    
    // Also fetch and display reviews for this place
    loadPlaceReviews(placeId);
    
  } catch (error) {
    console.error('Error fetching place details:', error);
    placeDetailsContainer.innerHTML = '<p>Error loading place details. Please try again later.</p>';
  }
}

// Function to load reviews for a specific place
async function loadPlaceReviews(placeId) {
  const reviewsContainer = document.getElementById('reviews');
  if (!reviewsContainer) return;
  
  // Keep the heading and the form
  const reviewsHeading = reviewsContainer.querySelector('h2');
  const addReviewSection = reviewsContainer.querySelector('#add-review');
  
  // Clear existing reviews (but keep the heading and form)
  reviewsContainer.innerHTML = '';
  reviewsContainer.appendChild(reviewsHeading);
  
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${placeId}/reviews`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const reviews = await response.json();
    
    if (reviews.length === 0) {
      const noReviews = document.createElement('article');
      noReviews.className = 'review-card';
      noReviews.textContent = 'No reviews yet. Be the first to review this place!';
      reviewsContainer.appendChild(noReviews);
    } else {
      // Display each review
      reviews.forEach(async review => {
        // Try to get user info
        let userName = "Anonymous";
        if (review.user_id) {
          try {
            const userResponse = await fetch(`http://127.0.0.1:5000/api/v1/users/${review.user_id}`);
            if (userResponse.ok) {
              const userData = await userResponse.json();
              userName = userData.first_name + " " + userData.last_name;
            }
          } catch (userError) {
            console.error("Error fetching review user details:", userError);
          }
        }
        
        const reviewCard = document.createElement('article');
        reviewCard.className = 'review-card';
        
        // Generate stars based on rating
        const rating = review.rating || 0;
        const stars = '★'.repeat(rating) + '☆'.repeat(5 - rating);
        
        reviewCard.innerHTML = `
          <p><strong>${userName}:</strong></p>
          <p>${review.text}</p>
          <p><strong>Rating:</strong> <span class="stars">${stars}</span></p>
          <p class="review-date">${new Date(review.created_at).toLocaleDateString()}</p>
        `;
        
        reviewsContainer.appendChild(reviewCard);
      });
    }
    
    // Add the review form back
    reviewsContainer.appendChild(addReviewSection);
    
  } catch (error) {
    console.error('Error fetching reviews:', error);
    const errorMsg = document.createElement('p');
    errorMsg.textContent = 'Error loading reviews. Please try again later.';
    reviewsContainer.appendChild(errorMsg);
    reviewsContainer.appendChild(addReviewSection);
  }
  
  // Setup review form submission
  setupReviewForm(placeId);
}

// Function to handle review form submission
function setupReviewForm(placeId) {
  const reviewForm = document.getElementById('review-form');
  if (!reviewForm) return;
  
  reviewForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    // Check if user is logged in (has token)
    const hasToken = document.cookie.split(';').some(item => item.trim().startsWith('token='));
    if (!hasToken) {
      alert('You must be logged in to submit a review');
      window.location.href = 'login.html';
      return;
    }
    
    const reviewText = document.getElementById('review-text').value;
    const rating = document.getElementById('rating').value;
    
    try {
      // Get token from cookie
      const token = document.cookie
        .split('; ')
        .find(row => row.startsWith('token='))
        .split('=')[1];
      
      const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${placeId}/reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          text: reviewText,
          rating: parseInt(rating)
        })
      });
      
      if (response.ok) {
        alert('Review submitted successfully!');
        // Reload reviews to show the new one
        loadPlaceReviews(placeId);
        // Clear form
        reviewForm.reset();
      } else {
        alert('Failed to submit review: ' + (response.statusText || 'Server error'));
      }
    } catch (error) {
      console.error('Error submitting review:', error);
      alert('Error submitting review. Please try again.');
    }
  });
}