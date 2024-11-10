document.addEventListener("DOMContentLoaded", function() {
  const alerts = document.querySelectorAll(".alert");
  
  alerts.forEach(alert => {
    // Trigger fade-in effect
    setTimeout(() => {
      alert.classList.add('show');
    }, 100); // Small delay to allow for smooth transition

    // Set auto-dismiss after 5 seconds
    setTimeout(() => {
      fadeOutAlert(alert);
    }, 5000);
  });

  function fadeOutAlert(alert) {
    alert.classList.remove('show'); // Start the fade-out animation
    setTimeout(() => {
      if (alert.parentElement) {
        alert.parentElement.removeChild(alert); // Remove from DOM after fading out
      }
    }, 600); // Delay for smooth transition before removal
  }
});
