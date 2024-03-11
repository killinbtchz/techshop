function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
//cart-----------------------------------------------------------------
function cart_add(id, quantity) {
    var csrftoken = getCookie('csrftoken');
    if (isNaN(quantity) || parseInt(quantity) !== parseFloat(quantity)) {
        quantity = 1;
    }

    var msg = 'product_id=' + id + '&quantity=' + quantity;

    $.ajax({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        type: 'POST',
        url: '/cart_add/',
        data: msg,
        success: function (data) {
            updateQuantity(id, quantity);
        },
    });
}

function updateQuantity(id, quantity) {
    $("#quantity" + id).text(quantity);
}

function cart_remove(product_id) {
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


function handleBuyClick(productId) {
    animateStar('anim' + productId);

    cart_add(productId);

    document.getElementById(`quantity-controls${productId}`).classList.remove('hidden');

    document.getElementById(`cartLink${productId}`).classList.remove('hidden');

    document.getElementById(`buyButton${productId}`).classList.add('hidden');
}

function animateStar(elementId) {
    let productIconClone = $('#' + elementId);

    let startPosition = productIconClone.offset();

    let finalPosition = {
        top: 0,
        left: $(window).width() - productIconClone.width(),
        opacity: 0
    };

    productIconClone.css({
        top: startPosition.top - $(window).scrollTop(),
        left: startPosition.left,
        position: 'fixed',
        zIndex: 1000
    });

    productIconClone.animate(finalPosition, {
        duration: 2000,
        complete: function() {
            productIconClone.remove();
        }
    });
}

function product_quantity_in_cart_change(id, quantityChange) {
    var csrftoken = getCookie('csrftoken');
    var msg = 'product_id=' + id + '&quantity_change=' + quantityChange;

    $.ajax({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        type: 'POST',
        url: '/cart_update/',
        data: msg,
        success: function (data) {
            var quantityElement = $("#quantity" + id);
            quantityElement.text(data.product_quantity);
            if (data.product_quantity==0){
                document.getElementById(`quantity-controls${id}`).classList.add('hidden');
                document.getElementById(`cartLink${id}`).classList.add('hidden');
                document.getElementById(`buyButton${id}`).classList.remove('hidden');
            }


        },
    });
}

function cart_update(id, quantityChange) {
    var csrftoken = getCookie('csrftoken');
    var msg = 'product_id=' + id + '&quantity_change=' + quantityChange;

    $.ajax({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        type: 'POST',
        url: '/cart_update/',
        data: msg,
        success: function (data) {
            if (data.product_quantity == 0){
                cart_remove(id);
            }
            var quantityElement = $("#quantity" + id);
            var totalElement = $(".total-price[data-product-id='" + id + "']");

            quantityElement.text(data.product_quantity);
            totalElement.text(data.product_total_price + " руб.");

            // Проверка, существуют ли элементы "total-price" и "total-quantity"
            var totalPriceElement = document.getElementById("total-price");
            var totalQuantityElement = document.getElementById("total-quantity");

            if (totalPriceElement !== null) {
                totalPriceElement.innerHTML = data.total_price;
            }

            if (totalQuantityElement !== null) {
                totalQuantityElement.innerHTML = data.total_quantity;
            }
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

//checkout----------------------------------------------------------------------------
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

//arm_op----------------------------------------------------------------------------
function changeButton(order_id){
    var button = document.getElementById('button' + order_id);
    let status = document.getElementById('status' + order_id);
    let status_dropdown = document.getElementById('status_dropdown' + order_id);
    if (button.innerHTML === 'Edit') {
        button.innerHTML = 'Save';
        status.classList.add('hidden');
        status_dropdown.classList.remove('hidden');
        for (let i=0; i<status_dropdown.options.length; i++){
            if(status_dropdown.options[i].innerText === status.innerText){
                status_dropdown.selectedIndex = i;
            }
        }
    } else{
        button.innerHTML = 'Edit';
        status.classList.remove('hidden');
        status_dropdown.classList.add('hidden');

    }
}

function updateOrderStatus(order_id, elem) {
    let msg = 'order_id=' + order_id;
    let new_status = elem.value;
    msg += '&new_status=' + new_status;
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        type: 'POST',
        url: '/update_order_status/',
        data: msg,
        success: function (data) {
           let status = document.getElementById('status' + order_id);
           status.innerText = data
        },
    });
}

    function showTextbox(element) {
    var textbox = element.nextElementSibling;
    textbox.classList.toggle("hidden");
    }

function filterOrders() {
    var filterInputs = document.querySelectorAll(".filter-input");
    var rows = document.querySelectorAll("tbody tr");

    rows.forEach(function(row) {
        var showRow = true;

        filterInputs.forEach(function(input) {
            var filterValue = input.value.trim().toLowerCase();
            var columnIndex = input.dataset.columnIndex;
            var cell = row.querySelector("td:nth-child(" + columnIndex + ")");
            var cellValue = (cell ? cell.textContent.trim().toLowerCase() : "");

            if (!cellValue.includes(filterValue)) {
                showRow = false;
            }
        });

        if (showRow) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}

function filterOrdersByStatus() {
    var filterStatusInput = document.getElementById("filterStatusInput").value.trim().toLowerCase();
    var rows = document.querySelectorAll("tbody tr");

    rows.forEach(function(row) {
        var orderStatusElement = row.querySelector("td:nth-child(6) span");
        if (orderStatusElement && orderStatusElement.textContent) {
            var orderStatus = orderStatusElement.textContent.trim().toLowerCase();
            if (orderStatus.includes(filterStatusInput)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        }
    });
}