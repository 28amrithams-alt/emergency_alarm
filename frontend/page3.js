document.addEventListener('DOMContentLoaded', () => {
  const settingsBtn = document.getElementById('settingsBtn');
  const settingsMenu = document.getElementById('settingsMenu');
  const cameraFeed = document.getElementById('cameraFeed');
  const cameraStatus = document.getElementById('cameraStatus');
  const galleryBtn = document.getElementById('galleryBtn');

  /* ===== SETTINGS MENU TOGGLE ===== */
  settingsBtn.addEventListener('click', () => {
    settingsMenu.classList.toggle('active');
  });

  document.addEventListener('click', (e) => {
    if (!settingsMenu.contains(e.target) && !settingsBtn.contains(e.target)) {
      settingsMenu.classList.remove('active');
    }
  });

  /* ===== MENU ACTIONS ===== */
  settingsMenu.querySelectorAll('button').forEach((btn) => {
    btn.addEventListener('click', () => {
      const action = btn.dataset.action;
      switch (action) {
        case 'sender':
          window.location.href = 'senderhistory.html';
          break;
        case 'receiver':
          window.location.href = 'receiverhistory.html';
          break;
        case 'tutorial':
          window.location.href = 'tutorial.html';
          break;
        case 'signout':
          localStorage.removeItem('loggedIn');
          alert('Signed out successfully!');
          window.location.href = 'page1.html';
          break;
      }
      settingsMenu.classList.remove('active');
    });
  });

  /* ===== CAMERA PERMISSION ===== */
  async function startCamera() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      cameraFeed.srcObject = stream;
      cameraStatus.textContent = 'Connected';
      cameraStatus.classList.remove('disconnected');
      cameraStatus.classList.add('connected');
    } catch (err) {
      cameraStatus.textContent = 'Permission Denied';
      cameraStatus.classList.remove('connected');
      cameraStatus.classList.add('disconnected');
      alert('Camera permission denied. Please allow access.');
    }
  }

  startCamera();

  /* ===== GALLERY BUTTON ===== */
  galleryBtn.addEventListener('click', () => {
    window.location.href = 'gallery.html';
  });
});
