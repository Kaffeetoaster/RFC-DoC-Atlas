
function change_visibility(id, show) {
  document.getElementById(id).style.display = show ? "inline" : "none";
}

// Eventlistener for all checkboxes
document.querySelectorAll("input[type=checkbox]").forEach(cb => {
    
    cb.addEventListener("change", function () {

    const target = this.dataset.target;
    change_visibility(target, this.checked);

  });
});
