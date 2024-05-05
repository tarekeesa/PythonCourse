$(document).ready(function() {
    // Delegate event handling for the add-to-cart button
    $('.product-actions').on('click', '.add-to-cart-btn', function(e) {
        e.preventDefault();
        let productId = $(this).data('product-id');
        let productActions = $(this).closest('.product-actions');
        addToCart(productId, productActions);
    });

    // Delegate event handling for the remove-item button
    $('.product-actions').on('click', '.remove-item-btn', function(e) {
        e.preventDefault();
        let productId = $(this).data('product-id');
        let productActions = $(this).closest('.product-actions');
        removeFromCart(productId, productActions);
    });

    function addToCart(productId, productActions) {
        $.ajax({
            type: 'POST',
            url: '/cart/add/',
            data: {
                product_id: productId,
                csrfmiddlewaretoken: generated_csrf_token
            },
            success: function(response) {
                productActions.html(`<a href="/cart/" class="btn border border-secondary rounded-pill px-3 text-primary">
                    <i class="fa fa-shopping-cart me-2 text-primary"></i> In Cart
                </a>
                <a href="#" class="btn btn-danger remove-item-btn" data-product-id="${productId}">
                    <i class="fa fa-trash"></i> Remove
                </a>`);
            },
            error: function() {
                alert('Error adding product to cart.');
            }
        });
    }

    function removeFromCart(productId, productActions) {
        $.ajax({
            type: 'POST',
            url: '/cart/remove/',
            data: {
                product_id: productId,
                csrfmiddlewaretoken: generated_csrf_token
            },
            success: function(response) {
                productActions.html(`<a href="#" class="btn border border-secondary rounded-pill px-3 text-primary add-to-cart-btn" data-product-id="${productId}">
                    <i class="fa fa-shopping-bag me-2 text-primary"></i> Add to Cart
                </a>`);
            },
            error: function() {
                alert('Error removing product from cart.');
            }
        });
    }
});
