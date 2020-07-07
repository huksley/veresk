function sayHello() {
  alert("Hello");
}

/**
 *
 * @param {HTMLFormElement} form
 * @param {Event} event
 * @param {string|undefined} id
 */
function saveUser(form, event, id) {
  fetch(id ? "/users/" + id : "/users", {
    method: id ? "PATCH" : "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      userName: form.userName.value,
    }),
  }).then((r) => {
    console.info(r.status);
    window.location = "?";
  });
  event.stopPropagation();
  return false;
}

/**
 * @param {HTMLAnchorElement} link
 */
function editUser(link) {
  document.editUserForm.objectId.value = link.getAttribute("data-id");
  document.editUserForm.userName.value = link.getAttribute("data-userName");
}

/**
 * @param {HTMLAnchorElement} link
 */
function deleteUser(link) {
  const id = link.getAttribute("data-id");
  fetch("/users/" + id, {
    method: "DELETE",
  }).then((r) => {
    console.info(r.status);
    window.location = "?";
  });
  event.stopPropagation();
  return false;
}
