const csrftoken = $('[name=csrfmiddlewaretoken]').val();

import { price_text } from './layout'

$(document).ready(function() {
    function total(){
        let cart_total_price = 0
        courses.forEach(function (course) {
            cart_total_price += course.price
        });
        $('#cart_total_price').text(cart_total_price);
        price_text();
    }
    total();
    $('.cart_item_destroy').click(function() {
        $.ajax({
            url: $(this).data('url'),
            type: 'DELETE',
            contentType: 'application/json',
            data: JSON.stringify({ 'course_id': $(this).data('course_id') }),
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                if (response.cart_items === 0) {
                    window.location.href = empty_cart_url
                }
                $('#course' + response.course_id).remove();
                total();
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ': ' + xhr.responseText);
            }
        });
    });
});