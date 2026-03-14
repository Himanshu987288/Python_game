const slider = document.getElementById("lightSlider");
const body = document.body;
const form = document.getElementById("loginForm");

slider.addEventListener("input", function () {
  body.setAttribute("data-light", this.value);
});

form.addEventListener("submit", function (e) {
  e.preventDefault();
  alert("Login Successful 🔐");
  form.reset();
});
