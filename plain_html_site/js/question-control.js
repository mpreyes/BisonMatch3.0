let children = [];
let questions = [];

window.onload = function() {
  let parent = document.getElementById("questions-progress-bar");
  for (let i=0; i < parent.children.length; i++) {
    children.push(parent.children[i]);
  }

  let otherParent = document.getElementById("questions-container");
  for (let i=0; i < otherParent.children.length; i++) {
    if (i > 1) {
      questions.push(otherParent.children[i]);
      otherParent.children[i].style.display = "none";
    } else if (i == 1) {
      questions.push(otherParent.children[i]);
    }
  }
}

function toggle_question(num) {
  for (let i=0; i < children.length; i++) {
    if (i < num) {
      children[i].className = "active";
    } else {
      children[i].className = "";
    }
  }

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

function next_question() {
  for (let i=0; i < questions.length; i++) {
    console.log(questions[i].className);
    if (questions[i].classList.contains("active")) {
      console.log("FoUND YOU!");
      questions[i].className = "form-container";
      questions[i + 1].className = "form-container active";
      toggle_question(i + 2);
      break;
    }
  }
}
