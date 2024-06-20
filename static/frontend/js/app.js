const pageOne = document.querySelector('.all_first_page');
const pageTwo = document.querySelector('.wrapper__progress');
const pageThree = document.querySelector('.page__three');
const submitBtn = document.querySelector('#number_submit_btn');
const errMsg = document.querySelector('.error__message');
const phonePlacer = document.querySelector('.phone_number');
const phanePlacerTwo = document.querySelector('.phane_number2');
const countNav = document.querySelector('#page_three_count_nav');
const countBtn = document.querySelector('.page_three_count_btn');
const chargesText = document.querySelector('.found__charges');
const registerBtn = document.querySelector('.register-btn');
const spinnerNewMe = document.querySelector('.spinner_new_me');
const spinnerPercent = document.querySelector('.spinner_percent');
let input = document.querySelector("#phone");
const fetchUrl = "http://127.0.0.1:8000/api/ipapi-data/";


// hidding the spinner
hideLoader();

// Phone selector js script
if (window.location.pathname === "/"){

  var iti = window.intlTelInput(input, {
      initialCountry: "auto", 
      separateDialCode: true ,
      nationalMode: true,
      geoIpLookup: callback => {
          fetch(fetchUrl)
            .then(res => res.json())
            .then(data => callback(data.country_code))
            .catch(() => callback("us"));
      },
  });

  // hiding pages one to move to page two
  function hidePageOne() {
    pageOne.style.display = 'none';
    pageTwo.style.display = 'block';
    hideLoader();
  }

  // hiding page two to move to page three
  function hidePageTwo() {
    pageTwo.style.display = 'none';
    pageThree.style.display = 'block';
    hideLoader();
    countNumbers(1, 33);
    // setTimeout(showFoundCharges, 6500);
  }


  // funtion to take number from page one and move it to page two
  submitBtn.addEventListener("click", function(e) {

    e.preventDefault();
    var phoneNumber = input.value.trim();
    showLoader();

    if(!phoneNumber){
        setTimeout(hideLoader, 1000);
        errMsg.textContent = 'Phone number is required';
    }else{
        var isValid = iti.isValidNumber();
        if (isValid) {
            setTimeout(hidePageOne, 1000);
            animateProgressBar();
        }else{
            setTimeout(hideLoader, 1000);
            errMsg.textContent = 'Invalid phone number, please check the phone number and try again.';
        }
    }
  });


  // Function to update the progress bar
  function updateProgressBar(percent) {

    //getting phone number
    phoneNumber = input.value.trim();
    var selectedCountry = iti.getSelectedCountryData();
    var inputCountryCode = selectedCountry.dialCode;

    // updating progress bar
    var progressBar = document.getElementById('progressBar');
    var progressPercent = document.createElement('span');
    let progressInfo = document.querySelector('.progress__info');
    progressPercent.classList.add('progress-percent');
    progressBar.innerHTML = '';
    progressBar.appendChild(progressPercent);
    progressBar.style.width = percent + '%';
    progressPercent.textContent = percent + '%';
    progressInfo.textContent = percent + '%  Concluded';
    phonePlacer.textContent = `Number: +${inputCountryCode}${phoneNumber}`;
    phanePlacerTwo .textContent = `(+${inputCountryCode}${phoneNumber})`;
  }

  // Function to animate the progress bar and list items
  function animateProgressBar() {
    let spinnerCount = 0;
    let spinnerInterval = setInterval(() => {
      spinnerCount++;
      spinnerPercent.textContent = spinnerCount + '%';
      if (spinnerCount >= 100) {
        clearInterval(spinnerInterval);
        spinnerNewMe.style.display = 'none';
  
        // Animate the progress bar
        var percent = 1;
        var intervalId = setInterval(function() {
          updateProgressBar(percent);
          percent++;
          if (percent > 100) {
            clearInterval(intervalId);
            showLoader();
            setTimeout(hidePageTwo, 3000);
          }
        }, 500); 
      }
    }, 250);

  };

  // Function to animate a specific list item
  function animateListItem(index) {
    var listItem = document.querySelectorAll('.list-item')[index];
    setTimeout(function() {
      listItem.style.opacity = 1;
      listItem.style.transform = 'translateY(0)';
    }, 600); // Delay for appearance after progress update
  }

  // Start the progress bar animation
  // setTimeout(animateProgressBar, 5800);
  // animateProgressBar();




  // Function to show loader overlay
  function showLoader() {
    var overlay = document.getElementById('overlay');
    overlay.style.display = 'flex';
  }

  


  // count function for page three
  function countNumbers(start, end) {
    if (start <= end) {
        countNav.textContent = start;
        countBtn.textContent = start;
      setTimeout(function() {
        countNumbers(start + 1, end);
      }, 100); 
    }
    if(start >= 33){
        showFoundCharges();
    }
  }

  function showFoundCharges(){
    chargesText.style.display = 'block';
    registerBtn.style.display = 'block';
  }

}

// Function to hide loader overlay
function hideLoader() {
  var overlay = document.getElementById('overlay');
  overlay.style.display = 'none';
}








