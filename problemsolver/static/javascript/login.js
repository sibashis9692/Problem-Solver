function getSelectedOption() {
    var selectElement = document.getElementById("mySelect");
    var selectedOption = selectElement.options[selectElement.selectedIndex].value;
    document.getElementById("select").value=selectedOption
}
  