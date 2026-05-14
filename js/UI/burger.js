const sidebar = document.getElementById("sidebar");
const burger = document.getElementById("burger");
const header = document.getElementById("sidebar-header");



export function initializeBurgerMenu() {
    // open on burger click
    burger.addEventListener("click", () => {
    sidebar.classList.remove("hidden");
    burger.classList.add("hidden");
    });

    // close on header click
    header.addEventListener("click", () => {
    sidebar.classList.add("hidden");
    burger.classList.remove("hidden");
    });
}