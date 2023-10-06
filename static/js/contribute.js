document.addEventListener('DOMContentLoaded', () => {
  const addressInput = document.getElementById('address-input');
  const addressDropdown = document.getElementById('address');

  addressInput.addEventListener('input', (e) => {
    e.preventDefault();
    const address = addressInput.value;
    getAddressCandidates(address);
  });

  async function getAddressCandidates(address) {
    const apiKey = 'AAPK25e62d82cb4a4ac3b9447b31fb82a802Uo6y06ooWlcX3_-OYUDaON3BJcj7_S1Jv8SUVxMTif29guR4dhqq6Gj2U6ZL8PH5';
    const locatorUrl = 'https://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer';

    const requestOptions = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    };

     try {
      const response = await fetch(`${locatorUrl}/findAddressCandidates?f=json&singleLine=${encodeURIComponent(address)}&outFields=*&maxLocations=5&forStorage=false&outSR=4326&apiKey=${apiKey}`, requestOptions);
      const data = await response.json();


      if (data.candidates.length > 0) {
        populateDropdown(data.candidates);
      } else {
        addressDropdown.innerHTML = '<option value="">No results found.</option>';
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      addressDropdown.innerHTML = '<option value="">Error fetching data. Please try again later.</option>';
    }
  }

  function populateDropdown(candidates) {
    addressDropdown.innerHTML = '<option value="">Select an address from below...</option>';
    candidates.forEach((candidate) => {
      const option = document.createElement('option');
      option.value = '' + candidate.location.x + ' ' + candidate.location.y;
//      console.log(option.value)
      option.textContent = candidate.address;
      addressDropdown.appendChild(option);
    });
  }
});