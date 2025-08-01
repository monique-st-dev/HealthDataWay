document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert.auto-dismiss');

  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.classList.remove('show'); // ще активира fade-out чрез Bootstrap
      alert.classList.add('fade');

      setTimeout(() => {
        if (alert && alert.parentNode) {
          alert.parentNode.removeChild(alert);
        }
      }, 500); // време за анимацията
    }, 4000); // време преди да започне изчезване
  });
});
