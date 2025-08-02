document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert.auto-dismiss');

  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.classList.remove('show');
      alert.classList.add('fade');

      setTimeout(() => {
        if (alert && alert.parentNode) {
          alert.parentNode.removeChild(alert);
        }
      }, 500);
    }, 4000);
  });
});
