function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    };

function cart_add(id, quantity) {
    var csrftoken = getCookie('csrftoken');
    if (!isNaN(quantity) && parseInt(quantity) === parseFloat(quantity)) {
        var msg = 'product_id=' + id + '&quantity=' + quantity;
    } else {
        var msg = 'product_id=' + id + '&quantity=1';
    }

    $.ajax({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        type: 'POST',
        url: '/cart_add/',
        data: msg,
        success: function (data) {
        },
    });
}


function cart_remove(button) {
    var product_id = $(button).data("product-id");
    var csrftoken = getCookie('csrftoken');
    var msg = 'product_id=' + product_id;

    $.ajax({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        type: 'POST',
        url: '/cart_remove/',
        data: msg,
        success: function (data) {
            if (data.success) {
                var productRow = $("#product_row" + product_id);
                productRow.remove();
                updateCartTotal(data.total_price, data.total_quantity);
            }
        },
    });
}


function cart_update(id, quantityChange) {
    var csrftoken = getCookie('csrftoken');
    let msg = 'product_id=' + id + '&quantity_change=' + quantityChange;

    $.ajax({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        type: 'POST',
        url: '/cart_update/',
        data: msg,
        success: function (data) {
            console.log(data)

            var quantityElement = $(".quantity[data-product-id='" + id + "']");
            var totalElement = $(".total-price[data-product-id='" + id + "']");

            quantityElement.text(data.product_quantity);
            totalElement.text(data.product_total_price + " руб.");

            document.getElementById("total-price").innerHTML = data.total_price;
            document.getElementById("total-quantity").innerHTML = data.total_quantity;


        },
    });
}

$(document).ready(function () {
    $('#clear-cart').click(function () {
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            type: 'POST',
            url: '/clear_cart/',
            success: function (data) {
                if (data.message === 'Cart cleared successfully') {
                    location.reload();
                } else {
                    alert('Ошибка при очистке корзины');
                }
            },
        });
    });
});



function create_order(){
    let form = document.forms.checkout_form;
    let msg = $(form).serialize();
    $.ajax({
        type: 'GET',
        url: '/create_order/',
        success: function (data) {
            document.location.href = '/orders';
        },
    });

}



