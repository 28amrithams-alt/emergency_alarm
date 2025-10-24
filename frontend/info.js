// Scroll reveal animation
window.addEventListener("scroll", () => {
  const elements = document.querySelectorAll("section");
  const scrollY = window.scrollY + window.innerHeight - 100;
  elements.forEach(el => {
    if (scrollY > el.offsetTop) {
      el.classList.add("visible");
    }
  });
});

// Fade animation
document.querySelectorAll("section").forEach(section => {
  section.style.opacity = "0";
  section.style.transition = "opacity 1s ease";
});
document.addEventListener("scroll", () => {
  document.querySelectorAll("section").forEach(section => {
    const position = section.getBoundingClientRect().top;
    if (position < window.innerHeight - 150) {
      section.style.opacity = "1";
    }
  });
});

// Redirect Start Button
document.querySelector(".start-btn").addEventListener("click", () => {
  window.location.href = "page3.html";
});
