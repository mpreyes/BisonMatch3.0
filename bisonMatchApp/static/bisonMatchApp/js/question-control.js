let questions = [];

window.onload = function() {
  let otherParent = document.getElementById("questions-container");
  for (let i=0; i < otherParent.children.length; i++) {
    questions.push(otherParent.children[i]);
    otherParent.children[i].style.display = "none";
  }
  otherParent.style.display = "none";
}


// ===============================================================
// Controls the toggling of a specific question.
// ===============================================================
function toggle_question(num) {
  for (let i=0; i < questions.length; i++) {
    if (i == num - 1) {
      questions[i].style.display = "block";
      questions[i].className = "form-container active";
    } else {
      questions[i].style.display = "none";
      questions[i].className = "form-container";
    }
  }
}


// ===============================================================
// Controls the next button on the quiz form
// ===============================================================
function next_question() {
  let quiz = document.forms["form"];
  let i = 0;
  for (; i < questions.length; i++) {
    if (questions[i].classList.contains("active")) {
      if (quiz["question" + (i + 1)].value == "") {
        alert("Please select an answer before continuing to the next question.");
        return;
      }

      questions[i].className = "form-container";
      questions[i + 1].className = "form-container active";
      toggle_question(i + 2);
      break;
    }
  }
}

function previous_question() {
  for (let i=0; i < questions.length; i++) {
    if (questions[i].classList.contains("active")) {
      questions[i].className = "form-container";
      questions[i - 1].className = "form-container active";
      toggle_question(i);
      break;
    }
  }
}

// ===============================================================
// Controls next button from the image upload page
// ===============================================================
function next_profile_form() {
  let profile_upload = document.getElementById("profile-image-upload-form");
  profile_upload.style.display = "none";
  let profile_info = document.getElementById("profile-info-form");
  profile_info.style.display = "block";
}


// ===============================================================
// Shows the profile upload image form
// ===============================================================
function show_image_upload_form() {
  let profile_upload = document.getElementById("profile-image-upload-form");
  profile_upload.style.display = "";
  let profile_info = document.getElementById("profile-info-form");
  profile_info.style.display = "none";
}


// ===============================================================
// Shows the quiz
// ===============================================================
function show_quiz() {
  let bio_info = document.forms["form"];
  console.log(bio_info);
  if (bio_info["name"].value == "") {
    alert("Required Field.\nYou must enter your name.");
    return;
  }

  if (bio_info["l-number"].value == "") {
    alert("Required Field.\nYou must enter your L-Number.");
    return;
  }

  if (bio_info["email"].value == "") {
    alert("Required Field.\nYou must enter your Lipscomb email address");
    return;
  }

  if (bio_info["gender"].value == "") {
    alert("Required Field.\nYou must select your gender.");
    return;
  }

  let email = bio_info["email"].value;
  if (email.substr(email.length - 18, email.length - 1) != "@mail.lipscomb.edu") {
    alert("Invalid email.\nYou must enter your Lipscomb email address.");
    return;
  }

  if (bio_info["bio"].value == "") {
    alert("You do not need to fill out your bio, but we would highly recommend it. Doing so will greatly increase your chances of having your matches contact you.");
  }

  if (bio_info["idealdate"].value == "") {
    alert("You do not need to fill out your ideal date, but we would highly recommend it. Doing so will greatly increase your chances of having your matches contact you.");
  }

  let profile_info = document.getElementById("profile-info-form");
  profile_info.style.display = "none";
  let otherParent = document.getElementById("questions-container");
  otherParent.style.display = "block";
  toggle_question(1);
}

function edit_info_form() {
  let profile_info = document.getElementById("profile-info-form");
  profile_info.style.display = "block";
  let otherParent = document.getElementById("questions-container");
  otherParent.style.display = "none";
}


// ========================================================================
// These two functions handle the profile photo upload stuff...
// ========================================================================
function uploadPhoto() {
  document.getElementById("image-upload-button").click();
}

document.getElementById("image-upload-button").onchange = function () {
    let reader = new FileReader();
    let image = document.getElementById("profile-image");
    let default_icon = document.getElementById("profile-default-image");
    let overlay = document.getElementById("croppie-overlay");
    let btn = document.getElementById("submit-crop");
    let form = document.getElementById("dummy");

    overlay.style.display = "block";
    let el = document.getElementById("croppie");
    var croppie = new Croppie(el,
    {
      viewport: { width: 256, height: 256, type: 'circle' },
      showZoomer: true
    });

    btn.addEventListener("click", function() {
      croppie.result('base64').then(function(resp) {
        image.src = resp;
        form.value = resp;
      });
      croppie.destroy();
      overlay.style.display = "none";
    });

    reader.onload = function (e) {
        default_icon.style.display = "none";
        image.style.display = "inline-block";

        croppie.bind({
            url: e.target.result,
        });
    };

    // read the image file as a data URL.
    reader.readAsDataURL(this.files[0]);
};





function checkInput() {
  let parent = document.getElementById("lnumbers");
  let children = parent.children;
  let lnumbers = []
  let form = document.forms["form"];

  for (let i=0; i < children.length; i++) {
    let child = children[i];
    lnumbers.push(child.innerHTML);
  }

  let is_in = false
  for (let i=0; i < lnumbers.length; i++) {
    if (lnumbers[i] === form["invoice"].value) {is_in = true;}
  }

  if (is_in) {
    return true;
  } else {
    alert("We do not have the LNumber: " + form["invoice"].value + " in our database.");
    return false;
  }
};
