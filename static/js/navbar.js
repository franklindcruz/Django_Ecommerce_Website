document.addEventListener('DOMContentLoaded', () => {
  const toggler = document.querySelector('.navbar-toggler');
  const searchBar = document.querySelector('.search-bar');

  toggler.addEventListener('click', () => {
    if (window.innerWidth < 992) {
      searchBar.classList.toggle('show-search');
    }
  });
});
