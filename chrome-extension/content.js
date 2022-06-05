//window.addEventListener('mouseup', wordSelected);
//window.addEventListener('load', selectAllText);

window.addEventListener('load', replaceText(document.body))
window.addEventListener('load', addPopupScript())

var _selectIndex = 0;
var countId = 0;

function wordSelected() {
  let selectedText = window
    .getSelection()
    .toString()
    .trim();
  console.log(selectedText);
  if (selectedText.length > 0) {
    let message = {
      text: selectedText
    };
    chrome.runtime.sendMessage(message);
  }
}

function selectAllText() {
  let allText = document.body.innerText;
  //let paragraphText = document.getElementsByTagName('p');
  console.log(allText);
  //console.log(paragraphText);
  //trim text 
  //pass to backend api 
}

function myFunction(popupId) {
  var popup = document.getElementById(popupId);
  popup.classList.toggle("show");
}

// simple helper function
function runFunctionInPageContext(fn) {
  var script = document.createElement('script');
  script.textContent = '(' + fn.toString() + '());';
  document.documentElement.appendChild(script);
  //document.documentElement.removeChild(script);
}

function addPopupScript(){
  const newElementScript = document.createElement('script')
  newElementScript.innerHTML = 'function myFunction(object) {console.log("in myFunction");console.log(object.lastChild.id);var popup = document.getElementById(object.lastChild.id);popup.classList.toggle("show");}'
  document.body.appendChild(newElementScript)
}

function replaceText(element) {
  console.log("attempting to change element")
  var test = 'hello'
  console.log(`checking a ${test}`)
  popupIdCount = ++countId
  console.log(`count ${popupIdCount}`)
  //var popupId = "popupId" + _selectIndex++
  var popupId = "popupId" + Math.random().toString(16).slice(2)
  if (element.hasChildNodes()) {
    element.childNodes.forEach(replaceText)
  } else if (element.nodeType === Text.TEXT_NODE) {
    if (element.textContent.match(/economy/gi)) {
      console.log("found economy text")
      const newElement = document.createElement('span')
      //newElement.innerHTML = element.textContent.replace(/(economy)/gi, '<span class="rainbow">$1</span>')
      //newElement.innerHTML = element.textContent.replace(/(economy)/gi, '<span style="background-color: black; color: black;">$1</span>')
      newElement.innerHTML = element.textContent.replace(/(economy)/gi, `<span class="popup" onclick="myFunction(this)">$1<span class="popuptext" id=${popupId}>yay popup text</span></span>`)
      element.replaceWith(newElement)
    }
  }
  //runFunctionInPageContext(myFunction())
}
