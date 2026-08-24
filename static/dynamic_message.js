function showMessages(message,tags,duration=5000) {
    let div1 = document.createElement("div");
    let div2 = document.createElement("div");
    div1.className = "d-flex justify-content-end";

    div1.style.opacity = "0";
    div1.style.transform = "translateX(50px)";

    // 2. Add Transition: Smoothly animate all changes over 0.5 seconds
    div1.style.transition = "all 0.5s ease";

    div2.className = `alert alert-${tags} shadow`;
    div2.innerHTML = `<i class="bi bi-exclamation-circle-fill me-2"></i> ${message}`;
    div2.style.width = "350px";
    div2.classList.add(`text-${tags}`);
    div2.style.backgroundColor = "white";
    div1.appendChild(div2);
    toastContainer.appendChild(div1);

    setTimeout(() => {
        div1.style.opacity = "1";        // Make visible
        div1.style.transform = "translateX(0)"; // Move to original position
    }, 10);


    // --- TRIGGER EXIT ANIMATION ---
    const dismiss = () => {
        div1.style.opacity = "0";
        div1.style.transform = "translateX(50px)";

        // 2. Remove from HTML after animation finishes (0.5s)
        setTimeout(() => {
            div1.remove();
        }, 500);
    };

    if (duration > 0) {
        setTimeout(dismiss, duration);
    }

    return dismiss;
}