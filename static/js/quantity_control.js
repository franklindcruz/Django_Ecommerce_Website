$(document).ready(function () {
  $(".incrementQuantityBtn").click(function (e) {
      e.preventDefault();

      const $productData = $(this).closest(".product_data");
      let value = parseInt($productData.find(".qty-input").val(), 10) || 0;

      if (value < 10) {
          value++;
          $productData.find(".qty-input").val(value).change();
      } else {
          alert("You can't add more than 10 items at a time.");
      }
  });

  $(".decrementQuantityBtn").click(function (e) {
      e.preventDefault();

      const $productData = $(this).closest(".product_data");
      let value = parseInt($productData.find(".qty-input").val(), 10) || 0;

      if (value > 1) {
          value--;
          $productData.find(".qty-input").val(value).change();
      }
  });
});
