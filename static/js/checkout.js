$(document).on('click', '.payWithRazorpay', function (e) {
  e.preventDefault()

  let fname = $('#fname').val()
  let lname = $('#lname').val()
  let email = $('#email').val()
  let phone = $('#phone').val()
  let address = $('#address').val()
  let city = $('#city').val()
  let state = $('#state').val()
  let country = $('#country').val()
  let zipcode = $('#zipcode').val()
  let token = $('input[name=csrfmiddlewaretoken]').val()

  // Check if any required field is empty
  if (
    !fname ||
    !lname ||
    !email ||
    !phone ||
    !address ||
    !city ||
    !state ||
    !country ||
    !zipcode
  ) {
    swal({
      text: 'Please fill in all the required fields.',
      icon: 'warning'
    })
    return false
  } else {
    $.ajax({
      method: 'GET',
      url: proceedToPayUrl,
      success: function (response) {
        if (!response.total_price) {
          alertify.error('Failed to retrieve cart total.')
          return
        }
        console.log(response)
        var options = {
          key: razorpayKeyId, // Enter the Key ID generated from the Dashboard
          amount: response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
          currency: 'INR',
          name: 'SHOPEE',
          description: 'Test Transaction',
          image:
            'https://marketplace.canva.com/EAE72jfknRM/2/0/1600w/canva-yellow-and-black-online-shop-business-logo-AvRZNVCTIeg.jpg',
          // order_id: 'order_IluGWxBm9U8zJ8', //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
          handler: function (response_b) {
            // alert(response_b.razorpay_payment_id)

            let data = {
              fname: fname,
              lname: lname,
              email: email,
              phone: phone,
              address: address,
              city: city,
              state: state,
              country: country,
              zipcode: zipcode,
              payment_mode: 'Paid by Razorpay',
              payment_id: response_b.razorpay_payment_id,
              csrfmiddlewaretoken: token
            }
            $.ajax({
              method: 'POST',
              url: placeOrderUrl,
              data: data,
              success: function (response_c) {
                console.log(response_c)

                swal({
                  title: 'Congratulations!',
                  text: response_c.status,
                  icon: 'success'
                }).then(value => {
                  window.location.href = '/my_orders/'
                })
              },
              error: function (response_c) {
                swal({
                  title: 'Error!',
                  text: response_c.responseJSON.error,
                  icon: 'error'
                })
              }
            })
          },
          prefill: {
            name: fname + ' ' + lname,
            email: email,
            contact: phone
          },
          notes: {
            address: 'Razorpay Corporate Office'
          },
          theme: {
            color: '#3399cc'
          }
        }
        var rzp1 = new Razorpay(options)
        rzp1.open()
      }
    })
  }
})
