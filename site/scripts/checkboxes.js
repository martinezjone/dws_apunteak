document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("input[type=checkbox]").forEach((checkbox, index) => {
      const key = "checkbox-" + index;
  
      // Recuperar estado guardado
      if (localStorage.getItem(key) === "true") {
        checkbox.checked = true;
      }
  
      // Guardar el estado cuando se marque/desmarque
      checkbox.addEventListener("change", () => {
        localStorage.setItem(key, checkbox.checked);
      });
    });
  });
  