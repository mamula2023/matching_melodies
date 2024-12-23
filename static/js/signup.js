const form = document.querySelector("#signup-form");

async function sendData() {
  const formData = new FormData(form);

  try {
    const response = await fetch("/api/user/", {
      method: "POST",
      body: formData,
    });
    console.log(await response.json());
    window.location='/';
  } catch (e) {
    console.error(e);
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendData();
});

