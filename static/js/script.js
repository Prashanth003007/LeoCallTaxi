$(document).ready(function(){

    $('.navbar .menu li a').click(function(){
        // applying again smooth scroll on menu items click
        $('html').css("scrollBehavior", "smooth");
    });

    // toggle menu/navbar script
    $('.menu-btn').click(function(){
        $('.navbar .menu').toggleClass("active");
        $('.menu-btn i').toggleClass("active");
    });

});
document.addEventListener('DOMContentLoaded', function() {
    const datePicker = document.getElementById('bookingdate');

    // Get the current date
    const currentDate = new Date();

    // Calculate the maximum date by adding 6 months to the current date
    const maxDate = new Date(currentDate);
    maxDate.setMonth(currentDate.getMonth() + 6);

    // Format the dates as yyyy-mm-dd for HTML input element
    const currentDateFormatted = currentDate.toISOString().slice(0, 10);
    const maxDateFormatted = maxDate.toISOString().slice(0, 10);

    // Set the value and min/max attributes of the input element
    datePicker.value = currentDateFormatted;
    datePicker.setAttribute('min', currentDateFormatted);
    datePicker.setAttribute('max', maxDateFormatted);
});
//<script>
        document.addEventListener("DOMContentLoaded", function() {
          const form = document.getElementById("booking-form");

          // Listen for keypress events on the form
          form.addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
              event.preventDefault(); // Prevent the default form submission
              // Optionally, you can focus on the submit button or perform other actions here.
            }
          });
        }
        );
        function calculateDistance() {
            var origin = document.getElementById('origin').value;
            var destination = document.getElementById('destination').value;
            var type = document.getElementById("vtype").value;
            var twoway = document.getElementById("twoways").checked;

            var service = new google.maps.DistanceMatrixService();
            service.getDistanceMatrix({
                origins: [origin],
                destinations: [destination],
                travelMode: 'DRIVING',
                unitSystem: google.maps.UnitSystem.METRIC
            }, function(response, status) {
                if (status === 'OK') {
                    var distance = response.rows[0].elements[0].distance.text;

                    fetch('calculate_price', {
                        method: 'POST',
                        body: JSON.stringify({ type, distance, twoway }),
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Update the result elements with the calculated values
                        document.getElementById("estimatep").textContent = "ESTIMATED PRICE: " + data.cost;
                        document.getElementById("estimatet").textContent = "ESTIMATED TIME: " + data.time;
                        document.getElementById('result').textContent = "Distance: " + data.distance + "Km";
                    })
                    .catch(error => {
                        console.error('Error calculating distance:', error);
                    });
                } else {
                    document.getElementById('result').textContent = "Error calculating distance.";
                }
            });
        }

        // Autocomplete for origin and destination input fields
        var originInput = document.getElementById('origin');
        var destinationInput = document.getElementById('destination');
        var originAutocomplete = new google.maps.places.Autocomplete(originInput);
        var destinationAutocomplete = new google.maps.places.Autocomplete(destinationInput);
        // Function to get CSRF token from cookies
          function getCookie(name) {
            var value = "; " + document.cookie;
            var parts = value.split("; " + name + "=");
            if (parts.length === 2) return parts.pop().split(";").shift();
        }

     function validateForm() {
  // Reset error messages
  document.getElementById("phoneError").textContent = "";
  document.getElementById("emailError").textContent = "";

  // Get input values
  const phoneInput = document.getElementById("phone");
  const emailInput = document.getElementById("email");

  const phoneValue = phoneInput.value;
  const emailValue = emailInput.value;

  // Regular expression patterns for phone number and email validation
  const phonePattern = /^\d{10}$/;
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  // Validate phone number
  if (!phonePattern.test(phoneValue)) {
    document.getElementById("phoneError").textContent = "Invalid phone number";
    return false;
  }

  // Validate email address
  if (!emailPattern.test(emailValue)) {
    document.getElementById("emailError").textContent = "Invalid email address";
    return false;
  }

  // Form is valid
  calculateDistance();
  return true;
}

 //</script>


