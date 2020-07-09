function cls(className) {
  const l = document.getElementsByClassName(className)
  const ll = []
  for (let i = 0; i < l.length; i++) {
    ll.push(l.item(i))
  }
  return ll
}

/**
 * Saves form as new or existing fractal, invoking the API.
 * 
 * @param {HTMLFormElement} form
 * @param {Event} event
 * @param {string|undefined} id
 */
function saveFractal(form, event, id) {
  fetch(id ? "fractals/" + id : "fractals", {
    method: id ? "PATCH" : "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      complex_real: parseFloat(form.complex_real.value),
      complex_imaginary: parseFloat(form.complex_imaginary.value),
    }),
  }).then((r) => {
    console.info(r.status);
    window.location = "?";
    cls("fractals").forEach(e => e.style.display = "block")
    cls("editFractalForm").forEach(e => e.style.display = "none")
    cls("addFractalForm").forEach(e => e.style.display = "none")
  });
  event.stopPropagation();
  return false;
}

function cancel() {
  cls("mainControls").forEach(e => e.style.display = "block")
  cls("fractals").forEach(e => e.style.display = "block")
  cls("editFractalForm").forEach(e => e.style.display = "none")
  cls("addFractalForm").forEach(e => e.style.display = "none")
}

function showAddFractalForm() {
  cls("mainControls").forEach(e => e.style.display = "none")
  cls("fractals").forEach(e => e.style.display = "none")
  cls("addFractalForm").forEach(e => e.style.display = "block")
  cls("editFractalForm").forEach(e => e.style.display = "none")
}


/**
 * Opens edit form for specified fractal.
 * 
 * @param {HTMLAnchorElement} link
 */
function editFractal(link) {
  document.editFractalForm.objectId.value = link.getAttribute("data-id");
  document.editFractalForm.complex_real.value = link.getAttribute("data-complex-real");
  document.editFractalForm.complex_imaginary.value = link.getAttribute("data-complex-imaginary");

  cls("mainControls").forEach(e => e.style.display = "none")
  cls("fractals").forEach(e => e.style.display = "none")
  cls("editFractalForm").forEach(e => e.style.display = "block")
  cls("addFractalForm").forEach(e => e.style.display = "none")
}

/**
 * @param {HTMLAnchorElement} link
 */
function deleteFractal(link) {
  const id = link.getAttribute("data-id");
  fetch("fractals/" + id, {
    method: "DELETE",
  }).then((r) => {
    console.info(r.status);
    window.location = "?";
  });
  event.stopPropagation();
  return false;
}
