const csrftoken = $('[name=csrfmiddlewaretoken]').val();

$(document).ready(function() {
    $('.cart_item_store').click(function() {
        $.ajax({
            url: cart_item_store_url,
            type: 'POST',
            contentType: 'application/json',
            dataType: "json",
            data: JSON.stringify({'course_id': course_id}),
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                $('.cart_item_destroy').removeClass('d-none');
                $('.cart_item_store').addClass('d-none');
                },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ': ' + xhr.responseText);
            }
        });
    });
    console.log(cart_item_destroy_url)
    $('.cart_item_destroy').click(function() {
        $.ajax({
            url: cart_item_destroy_url,
            type: 'DELETE',
            contentType: 'application/json',
            data: JSON.stringify({ 'course_id': course_id }),
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                $('.cart_item_store').removeClass('d-none');
                $('.cart_item_destroy').addClass('d-none');
                },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ': ' + xhr.responseText);
            }
        });
    });
});