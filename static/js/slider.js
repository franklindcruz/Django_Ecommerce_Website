document.addEventListener('DOMContentLoaded', function() {
  let carouselElement = document.querySelector('#carouselExampleIndicators');
  let progressBar = document.getElementById('carouselProgressBar');
  let totalInterval = 5000; // 5-second interval
  let progressInterval; // Variable to hold progress interval timer

  let carouselInstance = new bootstrap.Carousel(carouselElement, {
    interval: totalInterval, // Set slide interval to 5000ms
    ride: 'carousel'
  });

  // Function to start the progress bar animation
  function startProgressBar() {
    progressBar.style.transition = 'none'; // Disable transition to reset
    progressBar.style.width = '0%'; // Reset progress bar to start
    setTimeout(function() {
      progressBar.style.transition = `width ${totalInterval}ms linear`; // Apply transition with the slide time
      progressBar.style.width = '100%'; // Progress the bar to 100% over the interval
    }, 100); // Delay to ensure the reset is visible
  }

  // Listen for when the slide changes and reset the progress bar
  carouselElement.addEventListener('slid.bs.carousel', function() {
    startProgressBar(); // Start progress for the next slide
  });

  // Initialize the progress bar when the page loads
  startProgressBar();
});
