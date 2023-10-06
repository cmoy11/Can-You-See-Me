// Function to fetch HTML components and add them to the respective containers
async function fetchHTMLComponent(url, containerId) {
  const response = await fetch(url);
  const html = await response.text();
  document.getElementById(containerId).innerHTML = html;

  // Set the active tab based on the current page
  const currentPage = window.location.pathname.split('/').pop();
  const sidebarItems = document.querySelectorAll('#sidebar li');
  sidebarItems.forEach(item => {
    if (item.dataset.tab === currentPage) {
      item.classList.add('active');
    }
  });

  // Add the active class to the corresponding sidebar icons
//    const sidebarIcons = document.querySelectorAll('.sidebar-icons i');
//    sidebarItems.forEach(item => {
//    if (item.getAttribute('data-tab') === currentPage) {
//      item.classList.add('active');
//    } else {
//      item.classList.remove('active');
//    }
//  });

  // Call openTab function to display profile data on the profile page
  if (currentPage === 'profile') {
    openTab('profile');
  }
}

// Load the header component into the header-container
fetchHTMLComponent('static/pages/header.html', 'header-container');

// Load the sidebar component into the sidebar-container
fetchHTMLComponent('static/pages/sidebar.html', 'sidebar-container');

function openTab(tabName) {
  const tabContents = document.getElementsByClassName('tab-content');

  const activeTab = document.getElementById(tabName);
  activeTab.classList.add('active');

  const sidebarItems = document.getElementsByClassName('sidebar')[0].getElementsByTagName('li');
  for (const item of sidebarItems) {
    if (item.textContent.trim().toLowerCase() === tabName.toLowerCase()) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  }

//  const sidebarItemsIcons = document.getElementsByClassName('sidebar-icons')[0].getElementsByTagName('i');
//  for (const item of sidebarItemsIcons) {
//    if (item.textContent.trim().toLowerCase() === tabName.toLowerCase()) {
//      item.classList.add('active');
//    } else {
//      item.classList.remove('active');
//    }
//  }

if (tabName === 'profile') {
    const storedUsername = localStorage.getItem('username');
    const storedID = localStorage.getItem('user_id');
    const storedOrg = localStorage.getItem('org');
    const userDetailsDiv = document.getElementById('user-details');

    // Clear the existing content before adding the user details
    userDetailsDiv.innerHTML = '';

    // Create the input fields for user details
    const userDetailsFields = `
      <div class="input-field">
        <label for="user-id">User ID:</label>
        <input type="text" id="user-id" class="user-detail" value="${storedID || 'N/A'}" readonly>
      </div>
      <div class="input-field">
        <label for="username">Username:</label>
        <input type="text" id="username" class="user-detail" value="${storedUsername || 'N/A'}" readonly>
      </div>
      <div class="input-field">
        <label for="user-org">Organization:</label>
        <input type="text" id="user-org" class="user-detail" value="${storedOrg || 'N/A'}" readonly>
      </div>
    `;

    // Add the user details fields to the userDetailsDiv
    userDetailsDiv.innerHTML = userDetailsFields;
  }

  var imageData = localStorage.getItem('image');
  var imageElement = document.getElementById('image');
  imageElement.src = 'data:image/jpeg;base64,' + imageData;

  // Display the image preview when the user selects an image
  const userImageInput = document.getElementById('user-image');
  const previewContainer = document.getElementById('preview-container');
  userImageInput.addEventListener('change', (event) => {
    const imageFile = event.target.files[0];
    if (imageFile) {
      const imageURL = URL.createObjectURL(imageFile);
      previewContainer.innerHTML = `<img src="${imageURL}" alt="Profile Preview" width="150">`;
    } else {
      previewContainer.innerHTML = '';
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  openTab('profile'); // Set the Profile tab as active by default
});

document.addEventListener("DOMContentLoaded", function() {
  // Add an event listener to the logout button
  const logoutButton = document.getElementById("logoutButton");
  logoutButton.addEventListener("click", function(event) {
    event.preventDefault();
    localStorage.clear();
    window.location.href = "/login";
  });
});

document.getElementById('profile-form').addEventListener('submit', (event) => {
  event.preventDefault();
  const password = document.getElementById('password').value;
  const organization = document.getElementById('organization').value;
  // Send the updated password and organization to the server using fetch or other methods
  // Handle the response from the server if needed
  console.log('Password:', password);
  console.log('Organization:', organization);
});

function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  sidebar.classList.toggle('collapsed');
}
