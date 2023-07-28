function submitForm(){
  getSelectedOption()
  const form = document.querySelector('form');
  const code= document.getElementById('myTextarea');

  document.getElementById("code").value=code.value
  let coding=document.getElementById("code").value
  let language=document.getElementById("language").value

  if (coding.trim() !== '' && language.trim() !== '') {
    form.submit();
  } else {
      alert("Please select a language and provide code before submitting.");
  }

}

function getSelectedOption() {
  var selectElement = document.getElementById("selection");
  var selectedOption = selectElement.options[selectElement.selectedIndex].value;
  document.getElementById("language").value=selectedOption
}

const textarea = document.getElementById('myTextarea');
textarea.addEventListener('keydown', function(e) {
if (e.key === 'Tab') {
  e.preventDefault(); // Prevent the default Tab behavior
  const start = this.selectionStart;
  const end = this.selectionEnd;
  const value = this.value;
  this.value = value.substring(0, start) + '   ' + value.substring(end);
  this.selectionStart = this.selectionEnd = start + 3; // Set the cursor position
}
});