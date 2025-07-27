document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert');

  alerts.forEach((alert) => {

    if (!alert.classList.contains('alert-dismissible')) return;

    setTimeout(() => {

      alert.style.transition = 'opacity 0.5s ease-out';
      alert.style.opacity = '0';


      setTimeout(() => {
        alert.remove();
      }, 500);
    }, 4000);
  });
});
