// Auto-dismiss flash messages after 5 seconds
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".alert").forEach((el) => {
    setTimeout(() => el.remove(), 5000);
  });
});
