
// Define the function to handle the click event
function handlePhoneValidation() {
    var phoneNumber = input.value.trim();
    var isValid = iti.isValidNumber();
    if (isValid) {
        var selectedCountry = iti.getSelectedCountryData();
        var inputCountryCode = selectedCountry.dialCode;
        var inputCountryCodeLength = inputCountryCode.length;
        var phoneNumberWithoutCode = phoneNumber.slice(inputCountryCodeLength); // Remove the country code from the input phone number
        if (phoneNumber.startsWith(inputCountryCode) && phoneNumberWithoutCode.length === selectedCountry.dialCode.length) {
            console.log("Phone number matches selected country code and length:", phoneNumber);
            // Proceed with your further logic here
        } else {
            console.log("Phone number does not match selected country code or length");
            // Handle the case where the phone number does not match the selected country code or length
        }
    } else {
        console.log("Invalid phone number");
        // Handle the case where the phone number is invalid
    }
}

