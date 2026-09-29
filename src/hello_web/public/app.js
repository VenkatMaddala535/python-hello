const form = document.querySelector('#greeting-form');
const output = document.querySelector('#greeting');
const button = form.querySelector('button');
const status = document.querySelector('#status');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  button.disabled = true;
  try {
    const name = new FormData(form).get('name');
    const response = await fetch(`/api/greet?${new URLSearchParams({ name })}`);
    const message = await response.text();
    if (!response.ok) throw new Error(message);
    output.textContent = message;
  } catch (error) {
    output.textContent = error.message || 'Could not reach the server. Try again.';
  } finally {
    button.disabled = false;
  }
});

async function checkHealth() {
  try {
    const response = await fetch('/health');
    if (!response.ok) throw new Error('Health check failed');
    const health = await response.json();
    if (health.status !== 'ok') throw new Error('App is not ready');
    status.dataset.state = 'ok';
    status.querySelector('span:last-child').textContent = 'App is running · /health is healthy';
  } catch {
    status.dataset.state = 'error';
    status.querySelector('span:last-child').textContent = 'App is unavailable · check the server';
  }
}
checkHealth();
