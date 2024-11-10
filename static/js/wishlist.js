
$(document).on('click', '.addToWishlist', function (e) {
  e.preventDefault()

  let $productData = $(this).closest('.product_data')
  let product_id = $productData.find('.product_id').val()
  let token = $('input[name=csrfmiddlewaretoken]').val()

  $.ajax({
    method: 'POST',
    url: addToWishlistUrl,
    data: {
      product_id: product_id,
      csrfmiddlewaretoken: token
    },
    success: function (response) {
      console.log(response)
      alertify.success(response.status)
      if (response.wishlist_items_count !== undefined) {
        $('#wishlist-badge').text(response.wishlist_items_count)
      }
    },
    error: function () {
      alertify.error('Failed to add to wishlist.')
    }
  })
})


$(document).on('click', '.removeWishlistItem', function (e) {
  e.preventDefault()

  let $productData = $(this).closest('.product_data')
  let product_id = $productData.find('.product_id').val()
  let token = $('input[name=csrfmiddlewaretoken]').val()

  $.ajax({
    method: 'POST',
    url: removeWishlistItemUrl,
    data: {
      product_id: product_id,
      csrfmiddlewaretoken: token
    },
    success: function (response) {
      console.log(response)
      alertify.success(response.status)
      if (response.wishlist_items_count !== undefined) {
        $('#wishlist-badge').text(response.wishlist_items_count)
      }
      // Refresh the cart items in the DOM after deletion
      setTimeout(() => {
        $('.wish-data').load(location.href + ' .wish-data')
      }, 100)
    },
    error: function (response) {
      console.log(response)
      alertify.error('An error occurred while trying to remove the item.')
    }
  })
})


