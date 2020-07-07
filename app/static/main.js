function sayHello() {
  alert("Hello");
}

/**
 *
 * @param {HTMLFormElement} form
 * @param {Event} event
 */
function saveUser(form, event) {
  fetch("/users", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: form.userName.value,
    }),
  });
  event.stopPropagation();
  return false;
}
