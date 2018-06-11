/* TO DO:

shuffle randomly
add scrollama bs

*/

/* RANDOM ORDER */
function random(max) {
    return Math.floor(Math.random() * Math.floor(max))
}

function orderCards() {
    const cards = Array.from(document.getElementsByClassName('card'))

    cards.forEach( function (d,i) {
        var randomNumber = random(800)
        return document.getElementById(d.id).style.order = randomNumber;
});
}

// instantiate the scrollama
const scroller = scrollama();

//callback functions

function handleStepEnter(response) {
    response.element.classList.add('is-active');
}

function handleStepExit(response) {
    response.element.classList.remove('is-active');
}

function init() {

    orderCards();
    
    // setup the instance, pass callback functions
    scroller
    .setup({
        step: '.card',
        offset: .4
    })
    .onStepEnter(handleStepEnter)
    .onStepExit(handleStepExit);
}
init();