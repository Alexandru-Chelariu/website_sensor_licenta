const toggleBtn = document.getElementById("toggleBtn");
const sidebar = document.getElementById("sidebar");
const mainContent = document.getElementById("mainContent");

if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("collapsed");
        mainContent.classList.toggle("expanded");
    });
}