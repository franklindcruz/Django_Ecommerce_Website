$(document).ready(function () {
  $(document).on('click', '.addToCartBtn', function (e) {
    e.preventDefault()

    const $productData = $(this).closest('.product_data')
    const product_id = $productData.find('.product_id').val()
    const product_qty = $productData.find('.qty-input').val()
    const token = $('input[name=csrfmiddlewaretoken]').val()

    $.ajax({
      method: 'POST',
      url: addToCartUrl,
      data: {
        product_id: product_id,
        product_qty: product_qty,
        csrfmiddlewaretoken: token
      },
      success: function (response) {
        console.log(response)
        alertify.success(response.status)
        if (response.cart_items_count !== undefined) {
          $('#cart-badge').text(response.cart_items_count)
        }
      },
      error: function () {
        alertify.error('Failed to add to cart.')
      }
    })
  })
})
