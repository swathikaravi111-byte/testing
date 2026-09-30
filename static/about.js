// about.js — interactivity for the About page
document.addEventListener("DOMContentLoaded", () => {
    // Fade cards in on scroll
    const cards = document.querySelectorAll(".card");
    cards.forEach(card => {
        card.style.opacity = "0";
        card.style.transform = "translateY(16px)";
        card.style.transition = "opacity 0.5s ease, transform 0.5s ease";
    });

    const reveal = () => {
        cards.forEach(card => {
            const top = card.getBoundingClientRect().top;
            if (top < window.innerHeight - 40) {
                card.style.opacity = "1";
                card.style.transform = "translateY(0)";
            }
        });
    };
    reveal();
    window.addEventListener("scroll", reveal);

    // Current year in footer
    const year = document.querySelector("#year");
    if (year) year.textContent = new Date().getFullYear();

    // List item highlight on click
    document.querySelectorAll(".card ul li").forEach(li => {
        li.style.cursor = "default";
        li.addEventListener("click", () => {
            li.style.color = li.style.color ? "" : "#4f7cff";
        });
    });

    // Smooth scroll back to top when the header is clicked
    const header = document.querySelector("header h1");
    if (header) {
        header.style.cursor = "pointer";
        header.title = "Back to top";
        header.addEventListener("click", () => {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }
});
