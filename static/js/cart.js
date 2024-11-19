$(document).on('click', '.changeQuantity', function (e) {
  e.preventDefault()

  let $productData = $(this).closest('.product_data')
  let product_id = $productData.find('.product_id').val()
  let product_qty = $productData.find('.qty-input').val()
  let token = $('input[name=csrfmiddlewaretoken]').val()

  $.ajax({
    method: 'POST',
    url: updateCartUrl,
    data: {
      product_id: product_id,
      product_qty: product_qty,
      csrfmiddlewaretoken: token
    },
    success: function (response) {
      console.log(response)
      //alertify.success(response.status);
      if (response.cart_items_count !== undefined) {
        $('#cart-badge').text(response.cart_items_count)
      }
    },
    error: function (response) {
      console.log(response)
      // alertify.error(response.responseJSON.error);
    }
  })
})

$(document).on('click', '.deleteCartItem', function (e) {
  e.preventDefault()

  let $productData = $(this).closest('.product_data')
  let product_id = $productData.find('.product_id').val()
  let token = $('input[name=csrfmiddlewaretoken]').val()

  $.ajax({
    method: 'POST',
    url: deleteCartItemUrl,
    data: {
      product_id: product_id,
      csrfmiddlewaretoken: token
    },
    success: function (response) {
      console.log(response)
      alertify.success(response.status)
      if (response.cart_items_count !== undefined) {
        $('#cart-badge').text(response.cart_items_count)
      }
      // Refresh the cart items in the DOM after deletion
      setTimeout(() => {
        $('.cart-data').load(location.href + ' .cart-data')
      }, 100)
    },
    error: function (response) {
      console.log(response)
      alertify.error('An error occurred while trying to delete the item.')
    }
  })
})
