
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