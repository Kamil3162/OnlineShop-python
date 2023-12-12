
let product_quantity = document.getElementsByName('element-quantity');

function quantity_modifier_add(){
    let number = product_quantity[0].value;
    console.log(typeof number);
    console.log(number);
    product_quantity[0].value = Number(number) + 1;
    console.log("You clicked minus");

}

function quantity_modifier_minus(){
    let number = product_quantity[0].value;
    console.log(number);
    product_quantity[0].value = number - 1;
    console.log("You clicked minus");
    //product_quantity.setAttribute('value',product_quantity[0].value);
}

function rate_from_active(){
    var bool = sessionStorage.getItem('rate_active');
    console.log(bool);
    if (bool){
        let form = document.getElementsByClassName('.opinion_form');
        form.style.visibility = "hidden";
    }
}

function checkFunction(){
    var door_pay = document.getElementById('door-payment');
    var card_form = document.getElementsByClassName('card-form');
    if (door_pay.checked || !door_pay.checked){
        door_pay.checked = false;
        if (card_form){
            console.log("detected");
            card_form[0].style.visibility = "visible";
        }
        console.log("esa click 1");
    }

}

function checkFunction1(){
    var door_pay = document.getElementById('door-payment');
    var card_pay = document.getElementById('card-payment');
    var card_form = document.getElementsByClassName('card-form');

    if (card_pay.checked || !card_pay.checked){
        card_pay.checked = false;
        door_pay.checked= true;
        console.log("esa click 2");
         if (card_form){
            console.log("detected");
            card_form[0].style.visibility = "hidden";
        }
    }
}

function paymentChoose(){
    var door_pay = document.getElementById('door-payment');
    var card_pay = document.getElementById('card-payment');
    const checkBoxes = document.querySelectorAll('input[type="checkbox"]');
    if (!door_pay.checked && !card_pay.checked){
        alert("Pls zaznacz cos gosciu kolorowy");
        return;
    }
}

function validation(){
    const form = document.querySelector('#form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const checkboxes = form.querySelectorAll('input[type="checkbox"]');
        if (!Array.from(checkboxes).some(checkbox => checkbox.checked)) {
            alert('Please select at least one checkbox.');
            location.reload();
      }
    });
}

function comments_limiter(){
    var comment_container = document.getElementsByName('.comment');
    console.log(comment_container);

}





