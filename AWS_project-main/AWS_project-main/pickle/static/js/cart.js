// cart.js - Add this file to your js folder

document.addEventListener('DOMContentLoaded', function() {
    // Initialize cart and wishlist in localStorage if they don't exist
    if (!localStorage.getItem('cart')) {
        localStorage.setItem('cart', JSON.stringify([]));
    }
    if (!localStorage.getItem('wishlist')) {
        localStorage.setItem('wishlist', JSON.stringify([]));
    }

    // Add click handlers to all "Add to Cart" buttons (both regular and featured products)
    document.querySelectorAll('.btn, .add-to-cart').forEach(button => {
        if (button.textContent.trim() === 'Add to Cart' || button.classList.contains('add-to-cart')) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                addToCart(this);
            });
        }
    });

    // Function to add item to cart
    function addToCart(button) {
        let productCard, product;
        
        // Handle different card structures (featured products vs regular products)
        if (button.closest('.product-card')) {
            // Featured product card structure
            productCard = button.closest('.product-card');
            product = {
                name: productCard.querySelector('.product-title').textContent,
                description: productCard.querySelector('.product-category').textContent,
                price: productCard.querySelector('.current-price').textContent.replace('₹', ''),
                image: productCard.querySelector('.product-img img').src
            };
        } else if (button.closest('.pickle-card, .snack-card')) {
            // Regular product card structure
            productCard = button.closest('.pickle-card, .snack-card');
            product = {
                name: productCard.querySelector('h3').textContent,
                description: productCard.querySelector('p').textContent,
                price: productCard.querySelector('.price').textContent.replace('₹', ''),
                image: productCard.querySelector('.pickle-img, .snack-img').style.backgroundImage.match(/url\(["']?(.*?)["']?\)/)[1]
            };
        }

        let cart = JSON.parse(localStorage.getItem('cart'));
        cart.push(product);
        localStorage.setItem('cart', JSON.stringify(cart));

        // Update cart count in header
        updateCartCount();

        // Show confirmation
        alert(`${product.name} has been added to your cart!`);
    }

    // Function to update cart count in header
    function updateCartCount() {
        let cart = JSON.parse(localStorage.getItem('cart'));
        const cartCount = document.querySelector('.cart-count');
        
        if (cartCount) {
            cartCount.textContent = cart.length;
        }
    }

    // Function to add item to wishlist
    function addToWishlist(button) {
        const productCard = button.closest('.pickle-card, .snack-card');
        const product = {
            name: productCard.querySelector('h3').textContent,
            description: productCard.querySelector('p').textContent,
            price: productCard.querySelector('.price').textContent.replace('₹', ''),
            image: productCard.querySelector('.pickle-img, .snack-img').style.backgroundImage.match(/url\(["']?(.*?)["']?\)/)[1]
        };

        let wishlist = JSON.parse(localStorage.getItem('wishlist'));
        
        // Check if item already exists in wishlist
        if (!wishlist.some(item => item.name === product.name)) {
            wishlist.push(product);
            localStorage.setItem('wishlist', JSON.stringify(wishlist));
            alert(`${product.name} has been added to your wishlist!`);
        } else {
            alert(`${product.name} is already in your wishlist!`);
        }
    }

    // Create wishlist buttons if they don't exist
    function initializeWishlistButtons() {
        document.querySelectorAll('.pickle-card, .snack-card').forEach(card => {
            // Check if wishlist button already exists
            if (!card.querySelector('.wishlist-btn')) {
                const btn = document.createElement('button');
                btn.className = 'wishlist-btn btn';
                btn.textContent = 'Add to Wishlist';
                btn.style.backgroundColor = '#9C27B0'; // Purple color to match wishlist theme
                btn.style.marginLeft = '5px';
                
                btn.addEventListener('click', function(e) {
                    e.preventDefault();
                    addToWishlist(this);
                });
                
                card.querySelector('.pickle-info, .snack-info').appendChild(btn);
            }
        });
    }

    // Initialize wishlist buttons
    initializeWishlistButtons();
    
    // Initialize cart count on page load
    updateCartCount();
});