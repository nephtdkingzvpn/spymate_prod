let input = document.querySelector("#phone")


// JavaScript for toggling sidebar
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('toggleBtn').addEventListener('click', function() {
    document.getElementById('sidebar').classList.toggle('open');
    document.getElementById('toggleBtn').classList.toggle('open');
    document.getElementById('closeBtn').classList.toggle('open');
  });

  document.getElementById('closeBtn').addEventListener('click', function() {
    document.getElementById('sidebar').classList.remove('open');
    document.getElementById('toggleBtn').classList.remove('open');
    document.getElementById('closeBtn').classList.remove('open');
  });
});

var iti = window.intlTelInput(input, {
    initialCountry: "auto",
    separateDialCode: true,
    nationalMode: true,
    geoIpLookup: callback => {
      fetch("https://ipapi.co/json")
        .then(res => res.json())
        .then(data => callback(data.country_code))
        .catch(() => callback("us"));
      },
    utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
  });


function copyToClipboard() {
    /* Get the text field */
    var copyText = document.getElementById("copyInput");
  
    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /* For mobile devices */
  
    /* Copy the text inside the text field */
    document.execCommand("copy");
  
    /* Alert the copied text */
    alert("Copied the text: " + copyText.value);
}
  
