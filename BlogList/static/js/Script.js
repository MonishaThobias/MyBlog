
$(document).ready(function () {
    $('#subscribeForm').submit(function (e) {
        e.preventDefault();  // stop page refresh/scroll

        // Clear existing messages
        $('#email_error').text('');
        $('#subscribe_error').text('');
        $('#subscribe-messages').html('');

        $.ajax({
            url: "{% url 'subscribe_ajax' %}",
            method: "POST",
            data: $(this).serialize(),
            dataType: "json",
            success: function (data) {
                if (data.success) {
                    $('#subscribe-messages').html(
                        '<p class="small text-success">' + data.message + '</p>'
                    );
                    $('#subscribeForm')[0].reset();
                } else {
                    if (data.errors) {
                        const errors = JSON.parse(data.errors);
                        if (errors.email) {
                            $('#email_error').text(errors.email[0].message);
                        }
                        if (errors.subscribe) {
                            $('#subscribe_error').text(errors.subscribe[0].message);
                        }
                    } else if (data.message) {
                        $('#subscribe-messages').html(
                            '<p class="small text-danger">' + data.message + '</p>'
                        );
                    }
                }
            },
            error: function () {
                $('#subscribe-messages').html(
                    '<p class="small text-danger">Something went wrong. Please try again.</p>'
                );
            }
        });
    });
});

