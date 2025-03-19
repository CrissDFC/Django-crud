function hideAlertAfterDelay() {
    const alert = document.getElementById('error-alert');
    if (alert) {
        setTimeout(() => {
            alert.classList.add('opacity-0', 'transition-opacity', 'duration-500');
            setTimeout(() => alert.remove(), 500); // Elimina el div tras la transición
        }, 5000); // Cambia el tiempo si lo deseas
    }
}

// Ejecuta cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', function () {
    hideAlertAfterDelay();
});