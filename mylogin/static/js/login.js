let fontSize = 16;
document.getElementById('increase-font').addEventListener('click', () => {
  fontSize += 2;
  document.body.style.fontSize = fontSize + 'px';
});
document.getElementById('decrease-font').addEventListener('click', () => {
  fontSize -= 2;
  document.body.style.fontSize = fontSize + 'px';
});
document.getElementById('toggle-contrast').addEventListener('click', () => {
  document.body.classList.toggle('high-contrast');
});

document.getElementById('contact-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('name').value.trim();
  const email = document.getElementById('email').value.trim();
  const message = document.getElementById('message').value.trim();
  const response = document.getElementById('response');

  if (!name || !email || !message) {
    response.textContent = 'All fields are required.';
    response.style.color = 'red';
    return;
  }

  try {
    const res = await fetch('http://localhost:5000/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, message })
    });
    const data = await res.json();
    response.textContent = data.message;
    response.style.color = 'green';
  } catch {
    response.textContent = 'Error submitting form.';
    response.style.color = 'red';
  }
});
