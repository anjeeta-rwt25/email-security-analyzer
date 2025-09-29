// script.js

// Show toast notifications
function showToast(message, type = "info") {
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerText = message;
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 3000);
}

// Toggle password visibility
function togglePassword(id) {
  const input = document.getElementById(id);
  input.type = input.type === "password" ? "text" : "password";
}

// Animate form on load
window.onload = () => {
  const form = document.querySelector(".form-container");
  if (form) {
    form.classList.add("fade-in");
  }
};
